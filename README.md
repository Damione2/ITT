# Information-Topological Theory (ITT)

## Minimal Foundation, Structural Closure, and Level Selection

Information-Topological Theory (ITT) is formulated as a **timeless canonical gauge framework** on the gauge-orbit configuration space

\[
\mathcal C_{\rm ITT}=\mathcal A(S^3)/\mathcal G(S^3).
\]

The repository separates standard mathematics, ITT-specific physical postulates, completed derivations, negative mathematical results, and future physical targets.

## Current scientific status

### Paper 0 — Foundation

The foundational manuscript contains:

- $SU(2)$ gauge geometry on $S^3$;
- the densitized canonical ITT constraint;
- the commuting classical constraint algebra and differential Gauss identity;
- the formal Chern--Simons state;
- the unit BPST sector and APS net spectral-flow index;
- ordinary Chern--Simons quantization $k\in\mathbb Z$;
- the ITT closed-wave physical postulate;
- the ITT unit scale-ratio self-similarity postulate $\ell/R=1$;
- the derived sixfold regular cyclic closure $N=6$;
- the explicit free diagonal $\mathbb Z_6$ realization on $S^3$ and the quotient $L(6,1)$;
- the convention-fixed invariant $\mathrm{cs}(\rho_1)=-1/6$;
- the derived differential-CS phase $Z_k=e^{-2\pi i k/6}$;
- the explicit ITT phase-triviality postulate used for level selection.

The structural-closure result removes the **order six** as an independent numerical input: under A-05,
\[
\ell_N=2R\sin\left(\frac{\pi}{N}\right),\qquad \ell_N=R
\]
has the unique regular cyclic solution
\[
N=6.
\]

The theorem selects the cyclic order. The concrete diagonal action on $S^3$ is the ITT geometric realization of that order; the theorem alone is not claimed to derive a unique free action or the lens-space parameter $q=1$.

### Paper 1 — Level Selection

`papers/01_level_selection/ITT_Paper1_LevelSelection_v0.1.tex` establishes the level-selection analysis based on the $L(6,1)$ sector:

1. the differential Chern--Simons phase;
2. the induced cyclic character relative to the chosen $\mathbb Z_6$ generator;
3. the obstruction to canonically identifying that character with a three-dimensional equivariant prequantum-fiber action from the presently specified data;
4. the ITT phase-triviality selection principle
   \[
   Z_k(L(6,1),\rho_1)=1,
   \]
   which gives
   \[
   k\in6\mathbb Z,\qquad k_{\min}=6.
   \]

The value $k_{\min}=6$ remains an **ITT-specific conditional consequence**, not a universal theorem of ordinary $SU(2)$ Chern--Simons theory.

## Foundational logical chain

The current ITT architecture is

\[
\text{closed coherent excitation (A-04)}
\longrightarrow
\text{regular cyclic closure}
\]

together with

\[
\frac{\ell}{R}=1\quad\text{(A-05)}
\longrightarrow
N=6\quad\text{(D-03)}.
\]

ITT then realizes the derived cyclic order by the free diagonal action
\[
(z_1,z_2)\mapsto
\left(e^{2\pi i/6}z_1,e^{2\pi i/6}z_2\right)
\]
on $S^3\subset\mathbb C^2$, giving
\[
L(6,1)=S^3/\mathbb Z_6.
\]

For the fundamental flat sector,
\[
\mathrm{cs}(\rho_1)=-\frac16,\qquad
Z_k=e^{-2\pi i k/6}.
\]

With A-03,
\[
Z_k=1
\quad\Longrightarrow\quad
k\in6\mathbb Z
\quad\Longrightarrow\quad
k_{\min}=6.
\]

## Future papers

- **Paper 2:** dynamical/soliton analysis of $N_{\rm gen}=3$.
- **Paper 3:** parameter-free fine-structure target.
- Later papers address masses, magnetic moments, and cosmological quantities.

These later targets are not used to justify either $N=6$ or $k=6$.

## Claim audit

See [`CLAIM_STATUS.md`](CLAIM_STATUS.md) for the authoritative logical status matrix.

The taxonomy is:

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

GitHub Actions compiles both Paper 0 and Paper 1. LaTeX sources are the version-controlled reproducibility layer; release commits may also retain rendered PDF snapshots for direct inspection.

## Scientific boundary

This repository does **not** present the following as results of standard mathematics:

- the physical ontology A-04;
- the unit scale-ratio postulate A-05;
- the phase-triviality postulate A-03;
- $N_{\rm gen}=3$;
- the heuristic product $3\times2$;
- Standard-Model anomaly counting as a derivation of $k$;
- a fractional ordinary $c_2$ number on $L(6,1)\times S^1$;
- phenomenological parameter fitting.

The role of the structural-closure module is deliberately limited: **A-05 implies the integer $N=6$ geometrically.** Experimental success or failure of later parameter-free predictions is what can ultimately test whether the ITT postulates are physically useful.

## Citation

Please use the metadata in [`CITATION.cff`](CITATION.cff) when citing the repository. The foundational manuscript remains the minimal ITT foundation; Paper 1 is a separate level-selection research note.

## License

Documentation and LaTeX sources are distributed under the repository's documentation license. Verification scripts and software components remain under their designated software license.
