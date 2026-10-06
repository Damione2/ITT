# ITT Mathematical & Physical Claim Status Matrix

This document tracks the precise logical status of core ITT claims and keeps established mathematics, theory-specific postulates, completed derivations, negative results, and future physical targets explicitly separated.

## Taxonomy

- **M** — Established Mathematics (standard literature / proven theorem)
- **A** — ITT Axiom / Postulate (defining choice of the theory)
- **D** — Derivation / Completed mathematical result
- **N** — Negative Result / Obstruction (a proposed construction fails or is not determined by the specified data)
- **P** — Physical Prediction / Target (not yet established)

| ID | Claim / Feature | Type | Status | Target |
| :--- | :--- | :--- | :--- | :--- |
| **M-01** | $S^3$ gauge-orbit geometry | **M** | Established Mathematics | `papers/00_foundation` |
| **M-02** | BPST instanton $Q=1$ sector | **M** | Established Mathematics | `papers/00_foundation` |
| **M-03** | APS spectral-flow index theorem | **M** | Established Mathematics | `papers/00_foundation` |
| **M-04** | Lens-space topology $L(6,1)=S^3/\mathbb Z_6$ | **M** | Established Mathematics | `papers/00_foundation`, Paper 1 |
| **M-05** | Lens-space CS invariant $\mathrm{cs}(\rho_1)=-1/6$ | **M** | Derived for fixed conventions | `papers/00_foundation`, Paper 1 |
| **M-06** | Standard CS level quantization $k\in\mathbb Z$ | **M** | Established Mathematics | `papers/00_foundation`, Paper 1 |
| **D-01a** | $P_{\rho_1}$ and the $\mathbb Z_6$-equivariant connection groupoid | **D** | Completed construction | Paper 1 |
| **D-01b.1** | Differential-CS phase $Z_k=e^{-2\pi i k/6}$ | **D** | Completed derivation | Paper 1 |
| **D-01b.2** | Induced cyclic character $\chi_k^{\rm CS}(\zeta)=e^{-2\pi i k/6}$ | **D** | Completed derivation | Paper 1 |
| **N-01** | Canonical identification of $\chi_k^{\rm CS}$ with a 3D equivariant prequantum-fiber action from the present data | **N** | Obstructed by dimension/transgression and character ambiguity | Paper 1 |
| **A-01** | Densitized constraint / helicity alignment $\mathcal C_a^i\approx0$ | **A** | ITT Kinematic Postulate | `papers/00_foundation` |
| **A-02** | Timeless canonical gauge-orbit space $\mathcal C_{\rm ITT}$ | **A** | ITT Foundational Axiom | `papers/00_foundation` |
| **A-03** | Fundamental-sector phase triviality $Z_k(L(6,1),\rho_1)=1$ | **A** | ITT Level-Selection Postulate | Paper 1 / Foundation v2.1.4 |
| **D-02** | Minimal level selection $k_{\min}=6$ | **D** | Conditional on A-03 and integer CS quantization | Paper 1 |
| **P-01** | Soliton generational limit $N_{\rm gen}=3$ | **P** | Target dynamical proof | Paper 2 target |
| **P-02** | Fine-structure constant $\alpha^{-1}\approx137.035999$ | **P** | Preregistered Target | Paper 3 target |
| **P-03** | Absolute neutrino mass sum $\sum m_\nu$ | **P** | Under Calculation | Future lepton module |
| **P-04** | Tau anomaly discriminator $\Delta a_\tau^{\rm ITT}$ | **P** | Experimental Discriminator | Future magnetic-moment module |

## Release discipline

Claims marked **D**, **N**, or **P** are not to be presented as established physical results merely because they appear in a manuscript. In particular, the result $k_{\min}=6$ is a conditional consequence of the explicit ITT phase-triviality postulate A-03.

The negative result N-01 is a statement about the presently specified mathematical construction. It does not rule out a future, genuinely extended theory with additional equivariant or higher-geometric data that selects a canonical fiber character.

The prediction manifest remains the authoritative record for preregistered numerical targets. No retroactive parameter fitting is permitted in foundational modules.
