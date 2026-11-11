"""Classical axial gyromagnetic audit and explicitly conditional rotor projection.
Not complete soliton quantization or a prediction of electron g-2.
"""
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.constants import alpha
OUT=Path(__file__).resolve().parent
GAMMA=14.078701034090827;N=99.10491140365505;QEFF=.04301847452239876
G_ELECTRON=2.00231930436 # rounded experimental comparison, magnitude convention

def main():
 src=json.loads((OUT/'joint_hopf_controls.json').read_text())
 # Spin-half Wigner D states: normalized Haar marginal in u=cos(beta).
 u,w=leggauss(100)
 plus=1-u  # j=1/2,m=+1/2,k=-1/2
 minus=1+u
 assert abs(.5*w@plus-1)<1e-13
 assert abs(.5*w@minus-1)<1e-13
 axis_plus=float(.5*w@(u*plus));axis_minus=float(.5*w@(u*minus))
 assert abs(axis_plus+1/3)<1e-13 and abs(axis_minus-1/3)<1e-13
 assert np.max(abs(.5*(plus+minus)-1))<1e-15
 # Nontrivial body charge kernels confirm unpolarized orientation averaging.
 kernels=[np.exp(.7*u),u*u,np.cos(2.3*u)+.4*u]
 orientation_errors=[float(abs(.5*w@(.5*(plus+minus)*f)-.5*w@f)) for f in kernels]
 assert max(orientation_errors)<1e-14
 rows=[]
 for idx,row in enumerate(src['stages']):
  s=row['final'];mass=s['energy']/GAMMA # arbitrary f=1, cancels in g
  mu=s['raw_magnetic_moment']/GAMMA**2
  charge=QEFF*N/GAMMA;J=-N/GAMMA**2
  classical=2*mass*mu/(charge*J)
  invariant=2*s['energy']*abs(s['raw_magnetic_moment'])/(QEFF*N*N)
  assert abs(classical/invariant-1)<1e-14
  projected_mu=mu*axis_plus;projected=2*mass*projected_mu/(charge*.5)
  assert abs(projected-classical/3)<1e-13
  saved=np.load(OUT/f'joint_hopf_control{idx}.npz')
  v=saved['v'].reshape(len(saved['r']),len(saved['z']));j=np.argmin(abs(saved['z']))
  dipole=-4*np.pi*saved['r'][-1]**3*v[-1,j]
  rows.append(dict(stage=idx,grid=row['grid'],g_classical=classical,conditional_body_projection_g=projected,
   conditional_relative_difference_from_electron_g=projected/G_ELECTRON-1,
   conditional_anomaly=projected/2-1,
   magnetic_moment_volume=s['raw_magnetic_moment'],magnetic_moment_leading_far_dipole=float(dipole),
   leading_far_dipole_relative_difference=float(dipole/s['raw_magnetic_moment']-1)))
 result=dict(normalization=dict(N_physical=N/GAMMA**2,Q_physical=QEFF*N/GAMMA,experimental_e_in_rationalized_units=float(np.sqrt(4*np.pi*alpha)),
  note='f=1 chosen only for cancelling dimensional factors; all constants and charge branch are inputs.'),
  formulas=dict(classical='g_cl=2 Ebar |mubar|/(q_eff Nbar^2), using J_z=-m Nbar/gamma^2, m=1.',
  projection='Assume j=1/2,k=-1/2,m_spin=+1/2 and pure body magnetic operator: <axis_z>=m_spin*k/[j(j+1)]=-1/3; g_body_projection=g_cl/3.'),
  rotor_orientation_check=dict(axis_expectation_plus=axis_plus,axis_expectation_minus=axis_minus,unpolarized_weight_max_error=float(np.max(abs(.5*(plus+minus)-1))),charge_kernel_errors=orientation_errors),
  electron_comparison_g=G_ELECTRON,rows=rows,
  scope=['No derivation of fermionic quantization: j=1/2 sector and charge branch are assumptions.',
   'Quantum rotational energy, profile backreaction, induced collective current and boosts not computed.',
   'Projection result is only a body-current diagnostic; it is not the full quantum magnetic moment.',
   'Unpolarized charge statement is for leading rigid orientation averaging, not a full relativistic F1.',
   'Nearness to g=2 is not independent validation of prechosen parameters.'])
 (OUT/'joint_magnetic_projection.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
