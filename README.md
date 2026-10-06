# Information-Topological Theory (ITT)

## Minimal Foundational Formulation and Level-Selection Research Note

Information-Topological Theory (ITT) is formulated as a **timeless canonical gauge framework** on the gauge-orbit configuration space

\[
\mathcal C_{\rm ITT}=\mathcal A(S^3)/\mathcal G(S^3).
\]

The repository deliberately separates standard mathematical results, ITT-specific postulates, completed intermediate derivations, negative mathematical results, and future physical targets.

## Current scientific status

### Paper 0 — Foundation

The foundational manuscript contains:

- $SU(2)$ gauge geometry on $S^3$;
- the densitized canonical ITT constraint;
- the commuting classical constraint algebra and differential Gauss identity;
- the formal Chern--Simons state;
- the unit BPST sector and APS net spectral-flow index;
- ordinary Chern--Simons quantization $k\in\mathbb Z$;
- the lens-space sector $L(6,1)=S^3/\mathbb Z_6$;
- the convention-fixed invariant $\mathrm{cs}(\rho_1)=-1/6$;
- the derived differential-CS phase $Z_k=e^{-2\pi i k/6}$;
- the explicit ITT phase-triviality postulate used for level selection.

The previous assumption of a canonical three-dimensional prequantum fiber character has been removed. The corresponding obstruction is now analyzed in Paper 1.

### Paper 1 — Level Selection

`papers/01_level_selection/ITT_Paper1_LevelSelection_v0.1.tex` is a research note with four main results:

1. the differential Chern--Simons phase of the fundamental $L(6,1)$ sector;
2. the induced cyclic character relative to the chosen $\mathbb Z_6$ generator;
3. a negative result showing why the presently specified data do not canonically identify that character with a three-dimensional equivariant prequantum-fiber action;
4. the revised ITT level-selection principle
   \[
   Z_k(L(6,1),\rho_1)=1,
   \]
   which gives
   \[
   k\in6\mathbb Z,
   \qquad
   k_{\min}=6.
   \]

The value $k_{\min}=6$ is therefore an **ITT-specific conditional consequence**, not a universal theorem of ordinary $SU(2)$ Chern--Simons theory.

### Future papers

- **Paper 2:** dynamical/soliton analysis of $N_{\rm gen}=3$.
- **Paper 3:** parameter-free fine-structure target.
- Later papers address masses, magnetic moments, and cosmological quantities.

These later targets are independent of the level-selection derivation and are not used to justify $k=6$.

## Claim audit

See [`CLAIM_STATUS.md`](CLAIM_STATUS.md) for the authoritative logical status matrix.

The current taxonomy is:

- **M** — established mathematics;
- **A** — ITT axiom or postulate;
- **D** — completed derivation;
- **N** — negative result / mathematical obstruction;
- **P** — physical prediction or preregistered target.

The numerical manifest remains at [`predictions/prediction_manifest.json`](predictions/prediction_manifest.json).

## Repository structure

```text
papers/
├── 00_foundation/
│   └── ITT_Foundation_v2.1.tex
└── 01_level_selection/
    ├── ITT_Paper1_LevelSelection_v0.1.tex
    └── README.md

predictions/
└── prediction_manifest.json

.github/
└── workflows/
    └── compile-latex.yml

CLAIM_STATUS.md
CHANGELOG.md
README.md
CITATION.cff
CONTRIBUTING.md
LICENSE
```

## Reproducibility

GitHub Actions compiles both Paper 0 and Paper 1. The generated PDFs are workflow artifacts; LaTeX sources remain the version-controlled reproducibility layer.

## Scientific boundary

This repository does **not** treat any of the following as established inputs to the level-selection argument:

- $N_{\rm gen}=3$;
- the heuristic product $3\times2$;
- Standard-Model anomaly counting as a derivation of $k$;
- a fractional ordinary $c_2$ number on $L(6,1)\times S^1$;
- phenomenological parameter fitting.

## Citation

Please use the metadata in [`CITATION.cff`](CITATION.cff) when citing the repository. The foundational manuscript remains the minimal ITT foundation; Paper 1 is a separate level-selection research note.

## License

Documentation and LaTeX sources are distributed under the repository's documentation license. Verification scripts and software components remain under their designated software license.
