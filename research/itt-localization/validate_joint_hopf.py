"""Independent first/second variations, tail and static density diagnostics."""
import json
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.special import hyperu
from scipy.constants import hbar,m_e,c
from solve_joint_hopf_core import Joint,OUT,GAMMA

def load(idx):
 row=json.loads((OUT/'joint_hopf_controls.json').read_text())['stages'][idx];g=row['grid'];p=row['final']
 m=Joint(L=g['L'],nc=g['ncore'],no=g['nout'],order=g['order'],kappa=p['profile_kappa'],coulomb_eta=p['profile_coulomb_eta'],gauge_reg=p['gauge_reg'])
 saved=np.load(OUT/f'joint_hopf_control{idx}.npz');y=saved['y'];m.fg(y)
 return m,y

def tail(m):
 rr=np.linspace(8,min(17,m.L*.65),100);zz=np.zeros_like(rr)
 H=RegularGridInterpolator((m.r,m.z),m.state['H'].reshape(m.nr+1,m.nz+1))(np.column_stack([rr,zz]))
 ff=m.base(rr,zz,m.state['t']);ss,cc,*_=m.increment(ff,H,np.zeros_like(H),np.zeros_like(H))
 eta=m.state['required_coulomb_eta'];k=m.state['required_kappa']
 adjusted=np.log(ss)+np.log(rr)+eta*np.log(rr)
 fit=np.polyfit(rr,adjusted,1)
 x=2*k*rr
 reference=np.exp(-k*rr)*x*x*hyperu(2+eta,4,x)/rr
 logratio=np.log(ss/reference)
 linear_tail=dict(log_amplitude_ratio_slope=float(np.polyfit(rr,logratio,1)[0]),amplitude_ratio_max_over_min=float(np.exp(logratio.max()-logratio.min())),reference='Whittaker W_{-eta,3/2}(2 kappa r)/r, axial l=1 Coulomb-Yukawa tail.')
 far=m.base(np.array([m.L]),np.array([0.]),m.state['t'])[0][0]
 return dict(full_linear_tail_comparison=linear_tail,fit_range=[float(rr[0]),float(rr[-1])],fitted_effective_exponential_rate=float(-fit[0]),required_asymptotic_rate=k,eta=eta,boundary_matter_amplitude=float(far),warning='Finite-radius fit includes subleading angular multipoles and boundary errors, not an exact asymptotic measurement.')

def diagnostics(m):
 st=m.state;hh=st['H'][m.nodes];uu=st['u'][m.nodes];weights=[];radii=[]
 for r,z,w,N,Nr,Nz,E,PN,PR,PZ in m.quads:
  ff=m.increment(m.base(r,z,st['t']),np.sum(hh*PN,1),np.sum(hh*PR,1),np.sum(hh*PZ,1));s,co,br,bz,*_=ff
  weights.append(w*s*s*(1+br*br+bz*bz)*(1-np.sum(uu*N,1))/st['I']);radii.append(np.sqrt(r*r+z*z))
 ww=np.concatenate(weights);rr=np.concatenate(radii);assert abs(ww.sum()-1)<1e-10
 lam=hbar/(m_e*c);mr=st['energy']/GAMMA**2*st['charge_rms']
 return dict(M_times_charge_rms=mr,conditional_charge_rms_m_if_mass_fitted_to_electron=mr*lam,
  static_density_F_at_p_over_M={str(x):float(ww@np.sinc(x*st['energy']/GAMMA**2*rr/np.pi)) for x in [.01,.1,.5,1.]},
  caveat='Static orientation-averaged density Fourier transform; no quantum relativistic F1/F2 calculation. Electron mass used only for a conditional scale calibration.')

def main():
 results=[]
 for idx in [2,3]:
  m,y=load(idx);base=m.summary();E,g=m.fg(y)
  result=dict(stage=idx,summary=base,tail_check=tail(m),charge_diagnostics=diagnostics(m))
  if idx==3:
   rr,zz=np.meshgrid(m.r,m.z,indexing='ij');rad2=rr*rr+zz*zz
   fields=[np.exp(-rad2/4),(rr*rr-2*zz*zz)*np.exp(-rad2/4),zz*np.exp(-rad2/4),rad2*np.exp(-rad2/4)]
   variations=[]
   for ff in fields:
    H=ff.ravel()[m.pfree];H/=np.max(abs(H));d=np.r_[0.,m.chol.T@H]
    first=float(g@d);checks=[]
    for h in [1e-3,5e-4]:
     ep=m.fg(y+h*d)[0];em=m.fg(y-h*d)[0]
     checks.append(dict(step=h,first_fd=float((ep-em)/(2*h)),second_fd=float((ep-2*E+em)/h**2)))
    assert abs(first-checks[-1]['first_fd'])<3e-4
    assert checks[-1]['second_fd']>0
    variations.append(dict(first_analytic=first,checks=checks))
   result['four_smooth_polar_variations']=variations;m.fg(y)
  results.append(result);print(json.dumps(result),flush=True)
 (OUT/'joint_hopf_validation.json').write_text(json.dumps(dict(results=results),indent=2)+'\n')
if __name__=='__main__':main()
