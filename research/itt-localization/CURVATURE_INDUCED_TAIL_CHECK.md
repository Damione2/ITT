# Can spatial curvature make the field tail finite?

Date: 2026-11-14. This derives the simplest curvature-coupled tail equation and checks whether curvature generated only near a localized core can confine the field. It is a conditional effective-field test, not a metric dynamics derived from ITT.

## 1. Minimal geometric coupling

Represent one small field amplitude outside the core by a real scalar `u`. In natural units, use

With signature `(+−−−)`, choose

`S_u=(1/2)∫d⁴x√(−g)[g^{μν}∂_μu∂_νu−ξ ℛ u²]`.

Varying `u` gives

`□_g u+ξℛu=0`.

For a static, spherically symmetric tail in a nearly Euclidean region, neglecting small metric corrections to the radial Laplacian at first order:

`u''+(2/r)u'−ξℛ(r)u=0`.  (1)

This is the least additional assumption needed to translate “curvature resists the tail” into an equation. `ξ` is a coupling, not derived by the geometry alone.

## 2. A nonzero asymptotic curvature gives an exponential tail

If the far vacuum has constant `ℛ→ℛ∞>0`, then (1) becomes

`u''+(2/r)u'−m_eff²u=0`, `m_eff²=ξℛ∞`.

For `ξℛ∞>0`, the decaying solution is

`u(r)=A exp(−m_eff r)/r`, `L_tail=1/m_eff=1/√(ξℛ∞)`.

This is a derivation of a finite decay length from curvature, **conditional on a nonzero asymptotic curvature and positive coupling**. For `ξℛ∞=0`, the solutions are `A+B/r`; for negative `ξℛ∞`, they oscillate asymptotically rather than decay exponentially.

If one identifies `L_tail` with the reduced Compton length of the electron, the required curvature is

`ξℛ∞=(m_ec/ħ)²=1/(λ̄_C)²≈6.70×10²⁴ m⁻²`.

For `ξ≈1`, this means a universal spacetime curvature radius `1/√ℛ∞≈3.86×10⁻¹³ m`. Its curvature is roughly `10⁷⁷` times the observed cosmological curvature scale (`~10⁻⁵² m⁻²`), so it cannot be the nearly flat spacetime vacuum we observe far from particles. To avoid that, `ℛ` would need to be an **internal vacuum/geometric field** that couples to this mode but is not the ordinary spacetime Ricci curvature. That is a new field and needs its own action and observed couplings.

## 3. Curvature confined to the core does not by itself give an exponential tail

Suppose instead the geometry is asymptotically flat and its local curvature tends to zero, for example `ℛ(r)=O(r^{−p})` with `p>2`. At large `r`, the curvature term falls faster than `1/r²`, the scale of the radial Laplacian. The leading solutions of (1) therefore remain a constant and `1/r`; imposing `u(∞)=0` leaves the power tail `u∼B/r`, not `exp(−r/L)/r`.

This distinction matters: a power tail can have finite gradient energy in three spatial dimensions but it has no finite support and its norm can diverge. “Finite total energy” and “finite spatial extent” are different conditions.

There is also a simple self-consistency check for ordinary General Relativity. Its trace equation has `ℛ∼G T/c⁴` (up to convention-dependent sign). In a weak tail, stress `T` is at least quadratic in the small field `u`; hence `ξℛu` is cubic in `u`. It cannot act as a nonzero linear mass term around the flat vacuum `u=0`. Self-generated local curvature can distort the core and its power tail, but it does not create a constant far-field gap in this approximation. Known electron self-gravity is separately tiny: `Gm_e²/(ħc)≈1.75×10⁻⁴⁵`.

## 4. What would make the idea a closed mechanism?

There are two logically distinct candidates:

1. **Spacetime curvature:** add a specified metric action and solve it with the field. A local curvature source that dies away does not produce an asymptotic mass gap. A nonzero universal background curvature large enough to set the electron tail conflicts with the observed nearly flat far vacuum.
2. **Internal vacuum geometry:** introduce a field `χ` describing the vacuum's local geometric stiffness, for example, with the same `(+−−−)` signature, `Sχ=∫√(−g)[Z g^{μν}∂_μχ∂_νχ/2−V(χ)−gχu²/2]`. Its vacuum value can give `m_eff²=gχ₀`, but then `χ₀`, `Z`, `V`, and `g` must be derived from a more basic ITT variable. Calling `χ` “curvature” is not yet a derivation.

Thus the most economical next equation is the coupled system for `u`, `χ`, and, if `χ` is actual spacetime geometry, `g_{μν}`. The required checks are: a stable vacuum, a positive `m_eff²`, a regular localized core, a finite-energy tail, and recovery of weak gravity far away. This check supplies the tail condition; it does not yet supply the toroidal electron, its charge, spin, or mass.
