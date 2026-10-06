# Changelog

## [Unreleased] — 2026-10-06

### Scientific changes
- Added **A-04**, the ITT closed-wave physical postulate: stable elementary excitations are modeled as globally phase-coherent closed field modes with a non-trivial fundamental winding.
- Added **A-05**, the ITT unit scale-ratio self-similarity postulate:
  \[
  \frac{\ell}{R}=1.
  \]
- Added **D-03**, the sixfold structural-closure derivation. For a regular $N$-fold cyclic closure,
  \[
  \ell_N=2R\sin\left(\frac{\pi}{N}\right),
  \]
  so A-05 gives the unique integer solution $N=6$ for $N\ge3$.
- Clarified that D-03 derives the cyclic **order** six, while the free diagonal $\mathbb Z_6$ action on $S^3$ is the explicit ITT geometric realization; the theorem alone does not claim uniqueness of the free action or independently derive the lens-space parameter $q=1$.
- Updated the foundational logical chain so the order six is no longer treated as an unexplained numerical input.

### Repository changes
- Updated `CLAIM_STATUS.md` with A-04, A-05, and D-03.
- Updated the root `README.md` with the structural-closure module and explicit logical boundaries.
- Prepared Foundation v2.1.5 structural-closure insertion.
- Synchronized `CITATION.cff` for the planned 2.1.5 repository release.

## [2.1.4] - 2026-10-06

### Added
- Added **Paper 1** research note at `papers/01_level_selection/ITT_Paper1_LevelSelection_v0.1.tex`.
- Added Paper 1 documentation at `papers/01_level_selection/README.md`.

### Scientific changes
- Completed D-01b.1: the differential Chern--Simons phase
  \[
  Z_k(L(6,1),\rho_1)=e^{-2\pi i k/6}.
  \]
- Completed D-01b.2: the induced cyclic character
  \[
  \chi_k^{\rm CS}(\zeta)=e^{-2\pi i k/6}.
  \]
- Reclassified the original canonical three-dimensional equivariant-fiber identification as **N-01**, a negative result/obstruction for the presently specified data.
- Replaced the earlier equivariant-lift postulate with the explicit ITT **fundamental-sector phase-triviality postulate**
  \[
  Z_k(L(6,1),\rho_1)=1.
  \]
- Updated the level-selection chain so that $k_{\min}=6$ is a conditional ITT consequence of A-03 together with ordinary integer CS quantization.
- Updated Foundation to remove the obsolete claim that a three-dimensional prequantum line-bundle lift has already been specified.

### Repository changes
- Updated `CLAIM_STATUS.md` with the new `D` and `N` categories and split D-01 into completed sub-results plus the negative identification result.
- Updated root `README.md` to reflect the actual Paper 1 research-note status.
- Updated GitHub Actions to compile both Paper 0 and Paper 1.
- Updated `actions/checkout` to `@v5`.

## [2.1.3] - 2026-10-05

### Fixed
- Replaced non-portable operator macros with portable `\mathrm{...}` forms to support restricted math renderers/validators.
- Synchronized `main` with the corrected Paper 0 foundation used in the `v2.1.2` tag.
- Fixed the LaTeX CI path so `root_file` is resolved relative to `working_directory`.
- Updated `actions/checkout` from `@v4` to `@v5` in the intended repository state.

### Changed
- Added explicit literature citations in Paper 0 for BPST, APS, ordinary Chern--Simons quantization, lens-space Chern--Simons invariants, and the prequantum line-bundle framework.
- Corrected the claim matrix so P-02 is classified as a **Preregistered Target**, not an established prediction.
- Removed references to untracked/future files from the repository description and marked later papers as targets rather than completed modules.
- Synchronized `CITATION.cff` with repository release `2.1.3`.
- Kept the $k_{\min}=6$ result explicitly conditional on the then-unfinished $\mathbb Z_6$-equivariant lift.

## [2.1.2] - 2026-10-05

### Changed
- Clarified Abstract in Paper 0: level selection $k_{\min}=6$ framed as a conditional descent mechanism.
- Formalized density weight/metric convention for the Hamiltonian density.
- Populated `predictions/prediction_manifest.json` with preregistered parameter-free targets.
- Added Axiom category (`A`) to `CLAIM_STATUS.md`.

## [2.1.1] - 2026-10-04

### Fixed
- Updated `CITATION.cff` schema and synchronized repository DOI metadata.

## [2.1.0] - 2026-10-04

### Added
- Complete minimal foundational formulation (`papers/00_foundation/ITT_Foundation_v2.1.tex`).
- Automated LaTeX build pipeline via GitHub Actions.
- Preregistered prediction manifest.
- Mathematical claim status matrix.
