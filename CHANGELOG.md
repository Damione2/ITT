# Changelog

## [2.1.3] - 2026-10-05
### Fixed
- Synchronized `main` with the corrected Paper 0 foundation used in the `v2.1.2` tag.
- Fixed the LaTeX CI path so `root_file` is resolved relative to `working_directory`.
- Updated `actions/checkout` from `@v4` to `@v5`.

### Changed
- Added explicit literature citations in Paper 0 for BPST, APS, ordinary Chern--Simons quantization, lens-space Chern--Simons invariants, and the prequantum line-bundle framework.
- Corrected the claim matrix so P-02 is classified as a **Preregistered Target**, not an established prediction.
- Removed references to untracked/future files from the repository description and marked later papers as targets rather than completed modules.
- Synchronized `CITATION.cff` with repository release `2.1.3`.
- Kept the $k_{\min}=6$ result explicitly conditional on the unfinished $\mathbb Z_6$-equivariant lift.

### Scientific scope
- No new phenomenological parameter fitting or new physical claim is introduced in this release.

## [2.1.2] - 2026-10-05
### Changed
- Clarified Abstract in Paper 0: level selection $k_{\min}=6$ framed as a conditional descent mechanism awaiting explicit $\mathbb Z_6$-equivariant lift.
- Formalized density weight/metric convention for Hamiltonian density $\mathcal{H}_{\rm ITT} = \frac{1}{2\sqrt{g}} g_{ij} \mathcal{C}_a^i \mathcal{C}^{ja}$.
- Populated `predictions/prediction_manifest.json` with preregistered parameter-free targets.
- Added Axiom category (`A`) to `CLAIM_STATUS.md`.

## [2.1.1] - 2026-10-04
### Fixed
- Updated `CITATION.cff` schema and synchronized repository DOI metadata.

## [2.1.0] - 2026-10-04
### Added
- Complete minimal foundational formulation (`papers/00_foundation/ITT_Foundation_v2.1.tex`).
- Automated LaTeX build pipeline via GitHub Actions.
