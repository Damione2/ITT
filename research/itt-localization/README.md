# ITT localization research snapshot

**Updated 12 November 2026.** This directory preserves selected working calculations and a small numerical control from the cloud workspace. These are exploratory results, not additions to the established claims in [CLAIM_STATUS.md](../../CLAIM_STATUS.md) and not parameter-free electron predictions. The full scratch archive, uploaded source documents, temporary plots, and intermediate runs are excluded.

## Current results

| Question | Result and status |
| --- | --- |
| Does the ITT `SU(2)` unit sector already make a physical Hopf particle? | A unit map projects to `Q_H=1`, but an explicit companion `SU(2)` connection is flat for every radius. The pure-gauge projection supplies neither an energy minimum nor electric charge. [Derivation](ITT_SU2_TO_HOPF_DYNAMICS_CHECK.md), [check](check_su2_hopf_reduction.py). |
| Can the selected lens-space groupoid preserve the knot label? | Equivariant large gauge maps have degree divisible by six on the cover. The absolute integer `Q_H` can change; a residue modulo six can survive. This is a mathematical candidate for a discrete label, not a particle or a derived charge. [Review](REVIEW_OF_PROPOSED_N02_AND_LENS_GROUP.md). |
| What action can select a size? | Treating `n` as a physical `S²` field gives the *trial-family* balance `E(R)=16π²(f²R+κ/R)` and `R*=√κ/f`. The coefficients and the physical status of `n` remain additional inputs. [Derivation](ITT_SU2_TO_HOPF_DYNAMICS_CHECK.md), [field action](MINIMAL_FIELD_ACTION_DERIVATION.md). |
| What does the charged numerical candidate show? | A stationary gauged `S²+Maxwell` control has dimensionless `Ē≈334.185576` and `μ̄≈−3.732299`. Its classical `g≈5.904`; `g≈1.968` requires a separate spin-half body-current projection. The electron charge and mass scale are calibration inputs; full dynamical stability and physical form factors are open. [Baseline](HOPF_BASELINE_RESET.md), [model and limitations](JOINT_HOPF_SOLUTION.md), [charge audit](HOPF_GEOMETRY_CHARGE_AUDIT.md). |
| Can a vacuum minimum supply the missing restoring force? | A soft Gaussian vacuum mode lowers the Hopf bending energy when relaxed; a separate two-stiffness connection model can leave a positive `1/R` cost. Neither is derived from quantum gravity. [Calculation](VACUUM_RESPONSE_HOPF_SCALE_CHECK.md), [check](check_vacuum_response_hopf.py), [gravity scale test](QUANTUM_GRAVITY_VACUUM_STIFFNESS_CHECK.md). |
| Does threefold internal twist explain the electron? | Fixed threefold framing can select a trial radius, while planar three-lobe deformation raises bending energy; threefold shape, charge, and spin do not follow automatically. [Calculation](THREEFOLD_FRAMED_RING_CHECK.md), [check](check_threefold_elastic_ring.py). |
| Can a closed spring select both ring size and core thickness? | A conditional flux plus positive core-energy model has a two-scale minimum, provided its coefficients and conserved flux are independently justified. It has not yet produced electron observables. [Calculation](TOROIDAL_SPRING_TWO_SCALE_CHECK.md). |

The [literature map](GEOMETRIC_UNIFICATION_LITERATURE_MAP.md) links the verified primary sources relevant to the `SU(2) → S²+U(1) → Hopf` route. The physical bridge from the foundational gauge theory to the gauged soliton action remains open.

## Reproducing the included checks

The scripts were checked with Python 3.12.14, NumPy 2.3.5, and SciPy 1.17.0. From this directory, install [requirements.txt](requirements.txt) in an isolated environment and run:

```bash
python check_su2_hopf_reduction.py
python check_threefold_elastic_ring.py
python check_vacuum_response_hopf.py
python check_joint_magnetic_projection.py
python validate_joint_hopf.py
python check_hopf_static_zeeman.py
```

The four `joint_hopf_control*.npz` checkpoints and companion JSON files are included so the last three audits can inspect the frozen numerical controls without repeating the costly optimization. Their finite-domain and fixed-action limitations are documented in [JOINT_HOPF_SOLUTION.md](JOINT_HOPF_SOLUTION.md). Running the audit scripts may refresh the companion JSON files; they do not alter the foundational papers. The full optimization history and scratch output remain outside this selected snapshot.

The repository [LICENSE](../../LICENSE) applies: research prose and numerical snapshots are CC-BY-4.0; scripts are MIT-licensed.
