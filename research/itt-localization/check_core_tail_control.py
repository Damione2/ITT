"""Independent restricted trial test of the same gauged S2 action.
Spatial A_i=0 is an explicit variational restriction, NOT a Maxwell solution.
Only electrostatic Gauss is solved. Not a recovered previous checkpoint.
"""
import json
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import spsolve
from scipy.optimize import minimize
from scipy.integrate import quad
OUT=Path(__file__).resolve().parent
NU=.6636668952678496; NCHARGE=99.10491140365505; Q=.04301847452239876; GAMMA=14.078701034090827
class Control:
 def __init__(self,nr=180,nt=48,L=24):
  self.nr=nr;self.nt=nt;self.L=L
  re=L*np.linspace(0,1,nr+1)**2;te=np.linspace(0,np.pi,nt+1)
  r=(re[:-1]+re[1:])/2;th=(te[:-1]+te[1:])/2
  self.r=r[:,None];self.th=th[None,:]
  dr=np.diff(re);dt=np.diff(te);dc=np.cos(te[:-1])-np.cos(te[1:])
  self.vol=(2*np.pi/3)*np.diff(re**3)[:,None]*dc[None,:]
  ids=np.arange(nr*nt).reshape(nr,nt);rows=[];cols=[];vals=[]
  def edges(a,b,v):
   a=np.broadcast_to(a,v.shape).ravel();b=np.broadcast_to(b,v.shape).ravel();v=v.ravel()
   rows.extend(np.r_[a,b,a,b]);cols.extend(np.r_[a,b,b,a]);vals.extend(np.r_[v,v,-v,-v])
  gr=2*np.pi*re[1:-1,None]**2*dc[None,:]/np.diff(r)[:,None]
  edges(ids[:-1],ids[1:],gr)
  gt=2*np.pi*dr[:,None]*np.sin(te[None,1:-1])/np.diff(th)[None,:]
  edges(ids[:,:-1],ids[:,1:],gt)
  outer=2*np.pi*L**2*dc/(L+(L-r[-1]))
  rows.extend(ids[-1]);cols.extend(ids[-1]);vals.extend(outer)
  self.K=coo_matrix((vals,(rows,cols)),shape=(nr*nt,nr*nt)).tocsr()
  # Manufactured radial monopole boundary agrees with outer vacuum convention.
  self.boundary=outer
 def evaluate(self,y):
  R,kappa=np.exp(y);r=self.r;th=self.th;ss=np.sin(th);cc=np.cos(th)
  logt=np.log(R/r)-kappa*(np.sqrt(r*r+R*R)-R)
  F=2*np.arctan(np.exp(logt));s=np.sin(F);co=np.cos(F)
  Fr=s*(-1/r-kappa*r/np.sqrt(r*r+R*R))
  w=2*s*ss*(s*cc+1j*co)
  wr=2*Fr*ss*(2*s*co*cc+1j*(co*co-s*s))
  wt=2*s*(s*(cc*cc-ss*ss)+1j*co*cc)
  z=np.broadcast_to(1-2*s*s*ss*ss,w.shape)
  nv=np.stack([w.real,w.imag,z],axis=-1)
  nr=np.stack([wr.real,wr.imag,np.broadcast_to(-4*s*co*Fr*ss*ss,w.shape)],axis=-1)
  nth=np.stack([wt.real,wt.imag,np.broadcast_to(-4*s*s*ss*cc,w.shape)],axis=-1)/r[:,:,None]
  nph=np.stack([-w.imag,w.real,np.zeros_like(w.real)],axis=-1)/(r*ss)[:,:,None]
  X=np.stack([-w.imag,w.real,np.zeros_like(w.real)],axis=-1)
  norm=lambda a:np.sum(a*a,axis=-1)
  E2=.5*np.sum(self.vol*(norm(nr)+norm(nth)+norm(nph)))
  E4=.5*np.sum(self.vol*(norm(np.cross(nr,nth))+norm(np.cross(nr,nph))+norm(np.cross(nth,nph))))
  V=NU**2*np.sum(self.vol*(1-z))
  chi=norm(X)+norm(np.cross(X,nr))+norm(np.cross(X,nth))
  b=(self.vol*chi).ravel();M=self.K+diags(Q*Q*b)
  u=spsolve(M,Q*Q*b)
  I=float(b@(1-u));omega=NCHARGE/I
  charge=NCHARGE**2/(2*I);energy=float(E2+E4+V+charge)
  weights=b*(1-u)/I
  rms=float(np.sqrt(weights@(np.broadcast_to(r*r,w.shape).ravel())))
  tailrmsfrac=float(weights[np.broadcast_to(r>3*R,w.shape).ravel()].sum())
  assert abs(weights.sum()-1)<1e-12 and np.max(abs(norm(nv)-1))<1e-12
  ff={str(x):float(weights@np.sinc(x*energy/GAMMA**2*np.broadcast_to(r,w.shape).ravel()/np.pi)) for x in [.1,.5,1.]}
  return dict(static_orientation_averaged_form_factor=ff,R=float(R),trial_kappa=float(kappa),energy=energy,E2=float(E2),E4=float(E4),potential=float(V),charge_energy=float(charge),I=I,omega=omega,
    tail_compatible=bool(omega<NU),required_kappa=float(np.sqrt(max(0,NU**2-omega**2))),
    charge_rms=rms,M_times_charge_rms=energy*rms/GAMMA**2,
    charge_outside_3R_fraction=tailrmsfrac,
    gauss_residual=float(np.linalg.norm(M@u-Q*Q*b)/np.linalg.norm(Q*Q*b)),
    flux_relative_error=float(abs(float(self.boundary@u.reshape(self.nr,self.nt)[-1])/(Q*Q*I)-1)),
    trial_field_at_outer_boundary=float(np.max(abs(w[-1]))))
 def optimize(self,penalty,initial):
  def fun(y):
   d=self.evaluate(y)
   return d['energy']+penalty*d['charge_rms']**2
  opt=minimize(fun,initial,method='L-BFGS-B',bounds=[(np.log(.2),np.log(4)),(np.log(.12),np.log(2.5))],options={'ftol':1e-11,'gtol':1e-6,'maxiter':100})
  row=self.evaluate(opt.x);row.update(penalty=penalty,optimizer_success=bool(opt.success),optimizer_message=str(opt.message),evaluations=opt.nfev)
  return opt.x,row
 def controls(self):
  # K annihilates constants except the outer Robin term.
  one=np.ones(self.nr*self.nt);v=self.K@one;target=np.zeros((self.nr,self.nt));target[-1]=self.boundary
  assert np.max(abs(v-target.ravel()))<1e-10
  return float(np.max(abs(v-target.ravel())))
def main():
 m=Control();m.controls()
 canonical=m.evaluate(np.log([1.,1e-12]))
 e2exact=quad(lambda r:4*np.pi*r*r*16/(1+r*r)**2,0,m.L)[0]
 e4exact=quad(lambda r:4*np.pi*r*r*128/(1+r*r)**4,0,m.L)[0]
 canonical_errors=[canonical['E2']/e2exact-1,canonical['E4']/e4exact-1]
 assert max(abs(v) for v in canonical_errors)<.002
 y=np.log([1.,.35]);rows=[]
 for p in [0.,1.,3.,10.,30.,100.]:
  y,row=m.optimize(p,y);rows.append(row);print(json.dumps(row),flush=True)
 fine=Control(nr=260,nt=72,L=32);fine.controls()
 refined=[]
 for row in [rows[0],rows[-1]]:
  _,d=fine.optimize(row['penalty'],np.log([row['R'],row['trial_kappa']]));refined.append(d);print('REFINED',json.dumps(d),flush=True)
 assert max(d['gauss_residual'] for d in refined)<1e-9
 base=np.log([refined[0]['R'],refined[0]['trial_kappa']]);h=1e-3
 fun=lambda z:fine.evaluate(z)['energy']
 f0=fun(base);H=np.zeros((2,2))
 for i in range(2):
  ei=np.eye(2)[i]*h
  H[i,i]=(fun(base+ei)-2*f0+fun(base-ei))/h**2
 ei=np.array([h,0]);ej=np.array([0,h])
 H[0,1]=H[1,0]=(fun(base+ei+ej)-fun(base+ei-ej)-fun(base-ei+ej)+fun(base-ei-ej))/(4*h*h)
 eig=np.linalg.eigvalsh(H)
 assert min(eig)>0
 data=dict(canonical_finite_domain_relative_errors=canonical_errors,baseline_log_parameter_hessian_eigenvalues=eig.tolist(),model='Independent two-parameter Hopf trial of same classical S2 gauged Faddeev-Skyrme action; Gauss solved, A_i set to zero as a trial restriction.',
  profile='F(r)=2 atan[(R/r) exp(-kappa(sqrt(r^2+R^2)-R))]; Z=(cosF+i sinF cos(theta), i sinF sin(theta) exp(i phi)); n=Zdagger sigma Z.',
  fixed_parameters=dict(nu=NU,N=NCHARGE,q_effective=Q,gamma=GAMMA),grid=dict(nr=180,nt=48,L=24),fine_grid=dict(nr=260,nt=72,L=32),
  penalty_definition='Minimize E+penalty*r_charge_rms^2. Penalty is a constrained-search device, not an added physical interaction; only penalty=0 is energy minimization in this family.',
  scan=rows,refined=refined,
  limitations=['Not the lost old optimized profile, and not an exact coupled solution.','A_i=0 omits magnetic relaxation: spatial Maxwell equations are not satisfied.','Two radial profile parameters cannot establish full stationarity or stability.','Trial kappa need not equal required asymptotic kappa; discrepancy diagnoses ansatz error.','Positive charge and positive classical energy retain the previously derived electrostatic size bound.'])
 (OUT/'core_tail_control.json').write_text(json.dumps(data,indent=2)+'\n')
if __name__=='__main__':main()
