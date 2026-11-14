# Tail decay and internal winding: a profile-family scan

Date: 2026-11-14. This is a variational scan inside the thin-tube approximation to the ungauged `S²` plus quartic `H²` energy. It tests whether changing the cross-sectional profile can make the internal twist energy finite and lower the trial energy. It is not a solved Hopf soliton or an electron fit.

## Smooth trial family

Use local tube coordinates `(r,θ,s)` and

`n=(sin F_p(x) cos(θ+Ns/R), sin F_p(x) sin(θ+Ns/R), cos F_p(x))`, `x=r/a`,

with

`F_p(x)=2 atan[x⁻¹(1+x²)^{−(p−1)/2}]`, `p≥1`.

Near `x=0`, `F_p≈π−2x`, so the `m=1` field is smooth at the tube axis. Far away, `F_p≈2x⁻ᵖ`. The phase winding is `N`; the intended Hopf label is `Q_H=N` for this `m=1` tube ansatz, subject to verification in a global nonsingular toroidal map.

For a massless transverse profile, the phase norm contains `I_phase=∫sin²F_p d²x`. Since `sin F_p≈2x⁻ᵖ`, its tail behaves as `∫x^{1−2p}dx`. It diverges logarithmically at `p=1` and is finite for `p>1`. Thus the standard `p=1` algebraic tail makes nonzero internal winding infinitely costly in the infinite cross-section approximation; a faster tail removes that particular divergence.

## Profile integrals and energy

Define dimensionless cross-sectional integrals

`I₂⊥=∫[F'²+sin²F/x²]d²x`,

`I_phase=∫sin²F d²x`,

`I₄⊥=∫(F' sin F/x)²d²x`,

`I₄mix=∫(F' sin F)²d²x`.

Integrating the same positive two- and four-derivative terms as in [the two-scale Hopf estimate](HOPF_TUBE_TWO_SCALE_SCALING.md) gives

`E(R,a)=A R+B R/a²+C N²a²/R+D N²/R`,

`A=π f² I₂⊥`, `B=πκ I₄⊥`, `C=π f² I_phase`, `D=πκ I₄mix`.

At fixed `p,N`, both scale variables minimize analytically:

`R*=|N|√(D/A)`, `a*²=R*√(B/C)`,

`E*=2|N|[√(AD)+√(BC)]`.

The script [scan_profile_tail.py](scan_profile_tail.py) evaluates the integrals by changing variables to `t=ln x`, then scans `p` and minimizes these scale formulas. For the illustrative normalization `f²=κ=N=1`, the results are:

| Tail exponent `p` | `E*` (arbitrary natural units) | `a*/R*` |
| ---: | ---: | ---: |
| 1 | divergent phase integral | — |
| 1.1 | 377.96 | 0.814 |
| 1.2 | 296.50 | 0.986 |
| 2 | 210.23 | 1.611 |
| 3 | 206.84 | 2.053 |
| 5 | 217.89 | 2.687 |
| 7 | 229.30 | 3.181 |

The scan's formal minimum is near `p≈2.62`, `E*≈206.14`, `a*/R*≈1.90`. In this family, increasing `p` first reduces the cost of the distant phase tail. It also steepens the profile near the core and raises the transverse gradient and `H²` costs, so the total stops falling and turns upward. This illustrates a real competition, not a free energy reduction from linking alone.

## What failed and what this suggests

Every listed minimum has `a*/R*` of order one or larger; none satisfies the required `a≪R`. The formal optimum has `a*>R*`, so the torus is fatter than its major radius. Consequently the approximation used to derive the energy is not self-consistent anywhere near its minimum. The finite integrals and trend are useful diagnostics, but the quoted minimum is **not** evidence of a stable 3D ring. Curvature corrections and overlap of the core must be included in a full toroidal-coordinate field before trusting the result.

All energy values above use arbitrary normalized `f²=κ=1`; no electron mass was inserted or predicted. The couplings set the dimensional scales, and the chosen profile is not known to solve the field equations. The assumed `Q_H=N` must also be confirmed for the global field, and `N` must be protected against unwinding. Charge, spin, magnetic moment, and the observed electron mass remain unaccounted for.

The next useful calculation is a full finite-thickness toroidal ansatz with its exact metric/Jacobian and a mass or nonlinear vacuum response that determines the tail from the same action. Then compare its total energy and fluctuation modes against the sphere and the thinner Hopf candidates without imposing `a/R≪1` at the outset.
