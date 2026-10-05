# Information-Topological Theory (ITT)
## Minimal Foundational Formulation — Repository Release 2.1.3

Information-Topological Theory (ITT) is formulated here as a **timeless canonical gauge framework** on the gauge-orbit configuration space

\[
\mathcal C_{\rm ITT}=\mathcal A(S^3)/\mathcal G(S^3).
\]

The repository deliberately separates standard mathematical results from ITT-specific postulates, open mathematical derivations, and future physical targets.

## Current scientific status

### Paper 0 — Foundation

The foundational manuscript establishes and documents the following standard or explicitly defined ingredients:

- $SU(2)$ gauge geometry on $S^3$.
- The densitized canonical ITT constraint
  \[
  \mathcal C_a^i=E_a^i+\frac{k}{4\pi}B_a^i.
  \]
- The commuting classical constraint algebra and the differential Gauss identity.
- The formal Chern--Simons state solving the canonical constraint.
- The unit BPST sector and its APS net spectral-flow index.
- Ordinary Chern--Simons quantization $k\in\mathbb Z$.
- The lens-space sector $L(6,1)=S^3/\mathbb Z_6$ and the convention-fixed rational invariant $\mathrm{cs}(\rho_1)=-1/6$.

ITT then adds a **theory-specific equivariant descent postulate**. Under an explicit construction of the corresponding $\mathbb Z_6$-equivariant lift, the descent condition gives

\[
k\in6\mathbb Z,\qquad k_{\min}=6.
\]

This last step is **conditional**. It is not claimed to be a universal quantization theorem of ordinary $SU(2)$ Chern--Simons theory.

## Open mathematical programme

The principal next result is the explicit construction of the $\mathbb Z_6$-equivariant prequantum lift and its fiber character. Until that construction is completed, $k_{\min}=6$ remains a conditional ITT selection rule.

The independent soliton problem asks for a dynamical stability theorem selecting $N_{\rm gen}=3$ without using the generation count to justify $k=6$.

Later numerical modules, including $\alpha^{-1}$, neutrino masses, magnetic moments, and cosmological quantities, remain future targets and are not part of the foundational proof.

## Claim audit

The authoritative logical status is maintained in [`CLAIM_STATUS.md`](CLAIM_STATUS.md). The main categories are:

- **M** — established mathematics.
- **A** — ITT axiom or postulate.
- **D** — open derivation / mathematical proof.
- **P** — physical prediction or preregistered target.

The numerical manifest is maintained in [`predictions/prediction_manifest.json`](predictions/prediction_manifest.json). Retroactive parameter fitting is not permitted in foundational modules.

## Repository structure

```text
papers/
└── 00_foundation/
    ├── ITT_Foundation_v2.1.tex
    └── ITT_Foundation_v2.1.pdf

predictions/
└── prediction_manifest.json

.github/
└── workflows/
    └── compile-latex.yml

CLAIM_STATUS.md
CHANGELOG.md
CITATION.cff
CONTRIBUTING.md
README.md
```

Later papers are tracked as research targets and are not described here as completed derivations.

## Reproducibility

Paper 0 is compiled automatically by GitHub Actions. The workflow is intentionally scoped to the currently implemented foundation manuscript. The generated PDF is uploaded as a workflow artifact.

## Citation

Please use the metadata in `CITATION.cff` when citing this repository. The foundational manuscript is:

> Damyan Damyanov, *Information-Topological Theory (ITT): Minimal Foundational Formulation*, repository release 2.1.3, 2026.

## License

Documentation, papers, and LaTeX source are distributed under the repository's documentation license. Verification scripts and software components remain under their designated software license.
