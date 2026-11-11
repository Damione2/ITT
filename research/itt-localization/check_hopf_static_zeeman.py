"""External-field energy test of stationary Hopf candidate, no rotor.

Polar profile is fixed. Spatial Maxwell self-field re-solves at each B.
Uniform external-source/background energy excluded; self-field Robin retained.
"""
import json
import numpy as np
from scipy.sparse.linalg import spsolve
from solve_joint_hopf_core import Joint,OUT
from check_joint_magnetic_projection import QEFF,N


def check(stage):
    ref=json.loads((OUT/'joint_hopf_controls.json').read_text())['stages'][stage]
    grid=ref['grid'];p=ref['final'];data=np.load(OUT/f'joint_hopf_control{stage}.npz')
    m=Joint(L=grid['L'],nc=grid['ncore'],no=grid['nout'],order=grid['order'],
        kappa=p['profile_kappa'],coulomb_eta=p['profile_coulomb_eta'],gauge_reg=1e-14)
    m.fg(data['y']);st=m.summary();hh=m.state['H'][m.nodes]
    mass=np.zeros((m.cells,4,4));rhs=np.zeros((m.cells,4));drhs=rhs.copy()
    first=second=0.
    for r,z,w,S,Sr,Sz,E,PN,PR,PZ in m.quads:
        s,co,br,bz,kr,kz=m.increment(m.base(r,z,m.state['t']),np.sum(hh*PN,1),np.sum(hh*PR,1),np.sum(hh*PZ,1))
        chi=s*s*(1+br*br+bz*bz)
        mass+=(m.q*m.q*w*chi*r*r)[:,None,None]*S[:,:,None]*S[:,None,:]
        rhs+=(m.q*w*chi)[:,None]*S
        drhs+=(.5*m.q*m.q*w*chi*r*r)[:,None]*S
        first+=.5*m.q*np.sum(w*chi)
        second+=m.q*m.q/8*np.sum(w*chi*r*r)
    B=m.Bgrad+m.mat(mass,m.nodes,m.nn)
    b=np.bincount(m.nodes.ravel(),weights=rhs.ravel(),minlength=m.nn)
    db=np.bincount(m.nodes.ravel(),weights=drhs.ravel(),minlength=m.nn)
    v0=spsolve(B,b);dv=spsolve(B,db)
    assert np.max(abs(v0-m.state['v']))<1e-10
    E0=st['energy'];mu0=st['raw_magnetic_moment']
    slope=first-float(db@v0)
    curvature=2*second-float(db@dv)
    samples=[]
    for field in [-1e-4,-5e-5,0.,5e-5,1e-4]:
        bb=b+field*db;v=spsolve(B,bb)
        energy=E0+first*field+second*field*field-.5*float(bb@v-b@v0)
        moment=-(first+2*second*field-float(db@v))
        samples.append(dict(B_model=field,energy=energy,moment_from_current=moment,
            relative_Maxwell_residual=float(np.linalg.norm(B@v-bb)/np.linalg.norm(bb))))
    fd=(samples[-1]['energy']-samples[0]['energy'])/2e-4
    fd_half=(samples[3]['energy']-samples[1]['energy'])/1e-4
    assert abs(slope+mu0)<1e-8
    assert abs(fd+mu0)<1e-6 and abs(fd-fd_half)<1e-6
    g_energy=2*E0*abs(fd)/(QEFF*N*N)
    return dict(stage=stage,grid=grid,energy0=E0,body_moment_integrated=mu0,
        energy_slope_analytic=slope,energy_slope_finite_difference=fd,
        energy_slope_half_step=fd_half,energy_curvature_frozen_polar=curvature,
        g_classical_from_energy=g_energy,conditional_projection_if_retained=g_energy/3,
        samples=samples)


def main():
    rows=[]
    for stage in [0,1,3]:
        row=check(stage);rows.append(row);print(json.dumps(row),flush=True)
    (OUT/'hopf_static_zeeman_audit.json').write_text(json.dumps(dict(
        scope='Stationary Hopf external magnetic energy response with re-solved Maxwell self-field; no collective rotation',
        conventions='Physical uniform B along z has A_cov,phi=-B*r/2; j follows previous code convention',
        rows=rows,limitations=['Polar matter shape fixed; self-Maxwell re-solves. At a stationary profile its relaxation affects energy at second order, not the first derivative.',
            'No new derivation of spin-half or factor 1/3; the latter is only a retained conditional benchmark.',
            'External source/background energy excluded; remote self-field boundary remains approximate.',
            'Energy derivative and current integral test numerical implementation, not empirical truth of the postulated action.']),indent=2)+'\n')


if __name__=='__main__':main()
