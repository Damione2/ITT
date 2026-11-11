"""Axial gauged Faddeev-Skyrme core: polar field relaxation + nested full Maxwell.
Dimensionless, fixed charge. Finite cylinder, remote matter Dirichlet and
leading electromagnetic Robin boundaries. Not a full-space exact solution.
"""
import json,time,argparse
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import spsolve
from scipy.linalg import cholesky,solve_triangular
from scipy.optimize import minimize
from numpy.polynomial.legendre import leggauss
from check_core_tail_control import NU,NCHARGE,Q,GAMMA
OUT=Path(__file__).resolve().parent
class Joint:
 def __init__(self,L=14.,nc=16,no=10,kappa=.34,order=3,coulomb_eta=0.,gauge_reg=0.,grid_scale=1.):
  self.grid_scale=grid_scale;self.gauge_reg=gauge_reg;self.coulomb_eta=coulomb_eta;self.L=L*grid_scale;self.nc=nc;self.no=no;self.kappa=kappa;self.order=order;self.q=Q;self.N=NCHARGE
  self.r=grid_scale*np.r_[np.linspace(0,3,nc+1),np.geomspace(3,L,no+1)[1:]]
  self.z=np.r_[-self.r[:0:-1],self.r];self.nr=len(self.r)-1;self.nz=len(self.z)-1
  ii,jj=np.meshgrid(np.arange(self.nr),np.arange(self.nz),indexing='ij');self.i=ii.ravel();self.j=jj.ravel();self.cells=len(self.i)
  self.r0=self.r[self.i];self.z0=self.z[self.j];self.hr=np.diff(self.r)[self.i];self.hz=np.diff(self.z)[self.j]
  ir=np.arange(self.nr*(self.nz+1)).reshape(self.nr,self.nz+1);iz=ir.size+np.arange((self.nr+1)*self.nz).reshape(self.nr+1,self.nz)
  self.ne=ir.size+iz.size;self.edges=np.column_stack([ir[self.i,self.j],ir[self.i,self.j+1],iz[self.i,self.j],iz[self.i+1,self.j]])
  self.efree=np.setdiff1d(np.arange(self.ne),np.r_[ir[:,0],ir[:,-1],iz[-1,:]])
  ids=np.arange((self.nr+1)*(self.nz+1)).reshape(self.nr+1,self.nz+1);self.nn=ids.size;self.ids=ids
  self.nodes=np.column_stack([ids[self.i,self.j],ids[self.i+1,self.j],ids[self.i,self.j+1],ids[self.i+1,self.j+1]])
  self.pfree=np.setdiff1d(np.arange(self.nn),np.unique(np.r_[ids[:,0],ids[:,-1],ids[-1,:]]))
  ug,wg=leggauss(order);self.quads=[]
  K=np.zeros((self.cells,4,4));B=K.copy();G=K.copy();P=K.copy()
  for x,wx in zip((ug+1)/2,wg/2):
   for y,wy in zip((ug+1)/2,wg/2):
    r=self.r0+self.hr*x;z=self.z0+self.hz*y;w=2*np.pi*r*self.hr*self.hz*wx*wy
    N=np.broadcast_to([(1-x)*(1-y),x*(1-y),(1-x)*y,x*y],(self.cells,4))
    Nr=np.column_stack([-(1-y)/self.hr,(1-y)/self.hr,-y/self.hr,y/self.hr]);Nz=np.column_stack([-(1-x)/self.hz,-x/self.hz,(1-x)/self.hz,x/self.hz])
    E=np.zeros((self.cells,4,2));E[:,0,0]=(1-y)/self.hr;E[:,1,0]=y/self.hr;E[:,2,1]=(1-x)/self.hz;E[:,3,1]=x/self.hz
    curl=np.array([-1,1,1,-1])[None,:]/(self.hr*self.hz)[:,None]
    a=(r*r-self.r0**2)/(self.hr*(2*self.r0+self.hr));da=2*r/(self.hr*(2*self.r0+self.hr))
    PN=np.column_stack([(1-a)*(1-y),a*(1-y),(1-a)*y,a*y]);PR=np.column_stack([-(1-y)*da,(1-y)*da,-y*da,y*da]);PZ=np.column_stack([-(1-a)/self.hz,-a/self.hz,(1-a)/self.hz,a/self.hz])
    self.quads.append((r,z,w,N,Nr,Nz,E,PN,PR,PZ))
    K+=w[:,None,None]*curl[:,:,None]*curl[:,None,:]
    grad=Nr[:,:,None]*Nr[:,None,:]+Nz[:,:,None]*Nz[:,None,:]
    B+=(w*r*r)[:,None,None]*grad;G+=w[:,None,None]*grad
    s,c,br,bz,kr,kz=self.base(r,z,0)
    stiff=s*s*(1+kr*kr+kz*kz+1/r**2);mass=s*s*(1+br*br+bz*bz)
    P+=w[:,None,None]*(stiff[:,None,None]*(PR[:,:,None]*PR[:,None,:]+PZ[:,:,None]*PZ[:,None,:])+mass[:,None,None]*PN[:,:,None]*PN[:,None,:])
  self.Kcurl=self.mat(K,self.edges,self.ne);self.Bgrad=self.mat(B,self.nodes,self.nn)+self.boundary(3,2)
  self.Gboundary=self.boundary(1,0);self.Ggrad=self.mat(G,self.nodes,self.nn)+self.Gboundary
  pre=self.mat(P,self.nodes,self.nn)[self.pfree][:,self.pfree].toarray();self.chol=cholesky(pre,lower=True,check_finite=False)
  self.last=None;self.calls=0;self.tscale=.07
 @staticmethod
 def mat(local,ids,size):
  a=np.broadcast_to(ids[:,:,None],local.shape).ravel();b=np.broadcast_to(ids[:,None,:],local.shape).ravel()
  return coo_matrix((local.ravel(),(a,b)),shape=(size,size)).tocsr()
 def boundary(self,multipole,power):
  rows=[];cols=[];vals=[];u,w=leggauss(self.order);segments=[]
  for j in range(self.nz):segments.append((self.ids[-1,j:j+2],self.L,self.z[j],self.z[j+1]-self.z[j],False))
  for i in range(self.nr):
   for j in [0,-1]:segments.append((self.ids[i:i+2,j],self.r[i],self.z[j],self.r[i+1]-self.r[i],True))
  for ids,r0,z0,h,horizontal in segments:
   M=np.zeros((2,2))
   for t,wt in zip((u+1)/2,w/2):
    r=r0+h*t if horizontal else r0;z=z0 if horizontal else z0+h*t
    beta=multipole*self.L/(r*r+z*z);N=np.array([1-t,t]);M+=2*np.pi*r**(1+power)*beta*h*wt*np.outer(N,N)
   rows.extend(np.repeat(ids,2));cols.extend(np.tile(ids,2));vals.extend(M.ravel())
  return coo_matrix((vals,(rows,cols)),shape=(self.nn,self.nn)).tocsr()
 def base(self,r,z,t):
  r=r/self.grid_scale;z=z/self.grid_scale
  R=np.exp(t);h=np.sqrt(r*r+z*z);sn=r/h;cs=z/h
  d=np.maximum(h-3,0);ds=d**3/(1+d*d);dp=d*d*(3+d*d)/(1+d*d)**2
  F=2*np.arctan(R/h*np.exp(-self.kappa*ds-self.coulomb_eta*np.log1p(ds/3)));s=np.sin(F);c=np.cos(F);Fp=s*(-1/h-self.kappa*dp-self.coulomb_eta*dp/(3+ds))
  w=2*s*sn*(s*cs+1j*c);wh=2*Fp*sn*(2*s*c*cs+1j*(c*c-s*s));wt=2*s*(s*(cs*cs-sn*sn)+1j*c*cs)/h
  wr=wh*sn+wt*cs;wz=wh*cs-wt*sn
  cz=1-2*s*s*sn*sn;ch=-4*s*c*Fp*sn*sn;ct=-4*s*s*sn*cs/h
  cr=ch*sn+ct*cs;czd=ch*cs-ct*sn
  pol=np.maximum(abs(w),1e-300);br=-cr/pol;bz=-czd/pol
  kr=(w.conjugate()*wr).imag/(pol*pol);kz=(w.conjugate()*wz).imag/(pol*pol)
  return pol,cz,br/self.grid_scale,bz/self.grid_scale,kr/self.grid_scale,kz/self.grid_scale
 @staticmethod
 def increment(ff,H,Hr,Hz):
  s,c,br,bz,kr,kz=ff;den=np.cosh(H)-c*np.sinh(H);ss=s/den;cc=(c*np.cosh(H)-np.sinh(H))/den
  return ss,cc,ss*(br/np.maximum(s,1e-300)+Hr),ss*(bz/np.maximum(s,1e-300)+Hz),kr,kz
 def physical(self,y):
  H=np.zeros(self.nn);H[self.pfree]=solve_triangular(self.chol,y[1:],trans='T',lower=True,check_finite=False)
  return y[0]*self.tscale,H
 def fg(self,y):
  key=np.asarray(y).tobytes()
  if key==self.last:return self.value
  t,H=self.physical(y);hh=H[self.nodes];q=self.q
  Km=np.zeros((self.cells,4,4));Bm=Km.copy();Gm=Km.copy();rhs=np.zeros((self.cells,4));arhs=rhs.copy();grhs=rhs.copy()
  bare=e2=potential=phase0=0.;fields=[]
  for r,z,w,N,Nr,Nz,E,PN,PR,PZ in self.quads:
   HV=np.sum(hh*PN,axis=1);Hr=np.sum(hh*PR,axis=1);Hz=np.sum(hh*PZ,axis=1)
   ff=self.increment(self.base(r,z,t),HV,Hr,Hz);fields.append((ff,HV,Hr,Hz))
   s,c,br,bz,kr,kz=ff;bs=br*br+bz*bz;chi=s*s*(1+bs)
   MM=np.zeros((self.cells,2,2));MM[:,0,0]=s*s*(1+bz*bz);MM[:,1,1]=s*s*(1+br*br);MM[:,0,1]=MM[:,1,0]=-s*s*br*bz
   k=np.column_stack([kr,kz]);src=np.einsum('cij,cj->ci',MM,k)
   Km+=q*q*w[:,None,None]*np.einsum('cai,cij,cbj->cab',E,MM,E)
   rhs+=q*w[:,None]*np.einsum('cai,ci->ca',E,src)
   Bm+=(q*q*w*chi*r*r)[:,None,None]*N[:,:,None]*N[:,None,:];arhs+=(q*w*chi)[:,None]*N
   Gm+=(q*q*w*chi)[:,None,None]*N[:,:,None]*N[:,None,:];grhs+=(w*chi)[:,None]*N
   bare+=np.sum(w*chi);e2+=.5*np.sum(w*bs);potential+=NU**2*np.sum(w*np.where(c>0,s*s/np.maximum(1+c,1e-300),1-c))
   phase0+=.5*np.sum(w*(np.sum(k*src,axis=1)+chi/r**2))
  Kphysical=self.Kcurl+self.mat(Km,self.edges,self.ne);Kreg=diags(self.gauge_reg*self.Kcurl.diagonal());K=Kphysical+Kreg;B=self.Bgrad+self.mat(Bm,self.nodes,self.nn);G=self.Ggrad+self.mat(Gm,self.nodes,self.nn)
  rhs=np.bincount(self.edges.ravel(),weights=rhs.ravel(),minlength=self.ne);arhs=np.bincount(self.nodes.ravel(),weights=arhs.ravel(),minlength=self.nn);b=np.bincount(self.nodes.ravel(),weights=grhs.ravel(),minlength=self.nn)
  x=np.zeros(self.ne);x[self.efree]=spsolve(K[self.efree][:,self.efree],rhs[self.efree]);v=spsolve(B,arhs);u=spsolve(G,q*q*b)
  I=bare-float(b@u);assert I>0
  omega=self.N/I;phase=phase0-.5*float(rhs@x+arhs@v);charge=self.N**2/(2*I);energy=float(e2+potential+phase+charge)
  xx=x[self.edges];vv=v[self.nodes];uu=u[self.nodes];gradlocal=np.zeros((self.cells,4));gt=0.;dt=2e-5
  directphase=0.;E2total=E4total=0.;T2=T4=moment=r2q=normq=0.;phase_weak=np.zeros((self.cells,4))
  for (r,z,w,N,Nr,Nz,E,PN,PR,PZ),(ff,HV,Hr,Hz) in zip(self.quads,fields):
   s,c,br,bz,kr,kz=ff;a=np.einsum('ca,cai->ci',xx,E);av=r*np.sum(vv*N,axis=1);us=np.sum(uu*N,axis=1)
   k1=kr-q*a[:,0];k2=kz-q*a[:,1];k3=1/r-q*av;bs=br*br+bz*bz;ks=k1*k1+k2*k2+k3*k3;bk=br*k1+bz*k2;wl2=omega**2*(1-us)**2
   directphase+=.5*np.sum(w*s*s*(ks+bs*ks-bk*bk))
   E2total+=.5*np.sum(w*(bs+s*s*ks));E4total+=.5*np.sum(w*s*s*(bs*ks-bk*bk))
   C1=s*s*((1+bs)*k1-bk*br);C2=s*s*((1+bs)*k2-bk*bz)
   phase_weak+=w[:,None]*(C1[:,None]*Nr+C2[:,None]*Nz)
   T2+=.5*np.sum(w*wl2*s*s);T4+=.5*np.sum(w*wl2*s*s*bs)
   weight=w*s*s*(1+bs)*(1-us);normq+=np.sum(weight);r2q+=np.sum(weight*(r*r+z*z))
   moment+=-.5*q*np.sum(w*s*s*(1+bs)*(1-q*r*av))
   source=s*c*(ks+bs*ks-bk*bk)+NU**2*s-wl2*s*c*(1+bs)
   P1=br+s*s*(ks*br-bk*k1)-wl2*s*s*br;P2=bz+s*s*(ks*bz-bk*k2)-wl2*s*s*bz
   FH=s*source+c*(br*P1+bz*P2)
   gradlocal+=w[:,None]*(FH[:,None]*PN+(s*P1)[:,None]*PR+(s*P2)[:,None]*PZ)
   vals=[]
   for sign in [-1,1]:
    ss,cc,b1,b2,z1,z2=self.increment(self.base(r,z,t+sign*dt),HV,Hr,Hz);z1-=q*a[:,0];z2-=q*a[:,1]
    bb=b1*b1+b2*b2;kk=z1*z1+z2*z2+k3*k3;bk2=b1*z1+b2*z2
    vals.append(.5*bb+.5*ss*ss*(kk+bb*kk-bk2*bk2)+NU**2*np.where(cc>0,ss*ss/np.maximum(1+cc,1e-300),1-cc)-.5*wl2*ss*ss*(1+bb))
   gt+=np.sum(w*(vals[1]-vals[0]))/(2*dt)
  gh=np.bincount(self.nodes.ravel(),weights=gradlocal.ravel(),minlength=self.nn)[self.pfree]
  gy=np.r_[self.tscale*gt,solve_triangular(self.chol,gh,lower=True,check_finite=False)]
  EB=.5*float(x@(self.Kcurl@x)+v@(self.Bgrad@v));EE=.5*omega**2*float(u@(self.Ggrad@u))/q**2
  Ereg=.5*float(x@(Kreg@x))
  assert abs(directphase+EB+Ereg-phase)<1e-7
  assert abs(T2+T4+EE-charge)<1e-7
  phase_weak_global=np.bincount(self.nodes.ravel(),weights=phase_weak.ravel(),minlength=self.nn)
  phase_res=float(np.max(abs(phase_weak_global[self.pfree])))
  virial=float(E2total-E4total+3*potential-EB-3*T2-T4-EE)
  self.state=dict(E2=float(E2total),E4=float(E4total),scale_virial=virial,phase_weak_max=phase_res,energy=energy,t=float(t),R=float(np.exp(t)),H=H,x=x,v=v,u=u,I=float(I),omega=float(omega),required_kappa=float(np.sqrt(max(NU**2-omega**2,0))),
   profile_kappa=self.kappa/self.grid_scale,profile_coulomb_eta=self.coulomb_eta,required_coulomb_eta=float(q*q*self.N*omega/(4*np.pi*np.sqrt(max(NU**2-omega**2,1e-30)))),polar_gradient=float(e2),potential=float(potential),phase_magnetic=float(phase),charge_energy=float(charge),magnetic_energy=EB,electric_energy=EE,numerical_gauge_energy=Ereg,gauge_reg=self.gauge_reg,T2=float(T2),T4=float(T4),charge_rms=float(np.sqrt(r2q/normq)),raw_magnetic_moment=float(moment),
   gauss_residual=float(np.linalg.norm(G@u-q*q*b)/np.linalg.norm(q*q*b)),meridional_Maxwell_residual=float(np.linalg.norm((Kphysical@x-rhs)[self.efree])/np.linalg.norm(rhs[self.efree])),azimuthal_Maxwell_residual=float(np.linalg.norm(B@v-arhs)/np.linalg.norm(arhs)),
   charge_flux_relative_error=float(abs(omega/q*np.ones(self.nn)@(self.Gboundary@u)/(q*self.N)-1)),max_gradient=float(np.max(abs(gy))),gradient_norm=float(np.linalg.norm(gy)),max_H=float(np.max(abs(H))))
  self.last=key;self.value=energy,gy;self.calls+=1
  return self.value
 def summary(self):return {k:v for k,v in self.state.items() if k not in ['H','x','v','u']}
 def start(self,other=None):
  if other is None:return np.zeros(1+len(self.pfree))
  from scipy.interpolate import RegularGridInterpolator
  vals=RegularGridInterpolator((other.r,other.z),other.state['H'].reshape(other.nr+1,other.nz+1),bounds_error=False,fill_value=0)
  rr,zz=np.meshgrid(self.r,self.z,indexing='ij');H=vals(np.column_stack([rr.ravel(),zz.ravel()]))
  return np.r_[other.state['t']/self.tscale,self.chol.T@H[self.pfree]]
 def run(self,y,maxiter=130):
  E,g=self.fg(y);rng=np.random.default_rng(43);d=rng.normal(size=len(y));d/=np.linalg.norm(d);eps=1e-5
  fd=(self.fg(y+eps*d)[0]-self.fg(y-eps*d)[0])/(2*eps);an=float(g@d)
  assert abs(fd-an)<3e-5,(fd,an)
  ds=np.zeros(len(y));ds[0]=1;fdscale=(self.fg(y+eps*ds)[0]-self.fg(y-eps*ds)[0])/(2*eps)
  assert abs(fdscale-g[0])<3e-4,(fdscale,g[0])
  history=[]
  def cb(yy):
   self.fg(yy);history.append(self.summary())
   if len(history)%20==0:print('ITER',len(history),json.dumps(self.summary()),flush=True)
  opt=minimize(self.fg,y,jac=True,method='L-BFGS-B',bounds=[(-.7/self.tscale,.7/self.tscale)]+[(None,None)]*(len(y)-1),callback=cb,options={'maxiter':maxiter,'gtol':3e-5,'ftol':2e-12,'maxcor':15,'maxls':25})
  self.fg(opt.x)
  return dict(grid=dict(L=self.L,ncore=self.nc,nout=self.no,order=self.order),variables=len(y),initial_energy=E,final=self.summary(),iterations=opt.nit,success=bool(opt.success),message=str(opt.message),gradient_check=[an,float(fd)],scale_gradient_check=[float(g[0]),float(fdscale)],calls=self.calls),opt.x
 def save(self,y,name):
  np.savez_compressed(OUT/(name+'.npz'),y=y,r=self.r,z=self.z,H=self.state['H'],x=self.state['x'],v=self.state['v'],u=self.state['u'],t=self.state['t'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--fine',action='store_true');args=p.parse_args();started=time.monotonic();rows=[];prev=None
 configs=[(14,16,10,.34),(14,16,10,None),(18,20,12,None)]
 if args.fine:configs.append((18,28,16,None))
 for idx,(L,nc,no,k) in enumerate(configs):
  if k is None:k=prev.state['required_kappa']
  m=Joint(L=L,nc=nc,no=no,kappa=k);y=m.start(prev);row,y=m.run(y)
  name=f'joint_hopf_stage{idx}';m.save(y,name);rows.append(row)
  (OUT/'joint_hopf_results.json').write_text(json.dumps(dict(stages=rows,seconds=time.monotonic()-started),indent=2)+'\n')
  print('STAGE',idx,json.dumps(row),flush=True);prev=m
if __name__=='__main__':main()
