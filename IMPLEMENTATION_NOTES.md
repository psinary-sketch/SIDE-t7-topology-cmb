# t7_arc_search.py — Implementation Notes (v0.2, registration-conformed)

Dated implementation record for the T₇ matched-arc pipeline, conformed to
`T7_CMB_PIPELINE_PREREGISTRATION_v0_1.md` (frozen, May 2026). Author ruling
2026-07-18: **Option A — conform in place, geometry switched to the registered
incidence method.**

## Heritage

The pre-registration-era pipeline (April 2026) is preserved **unmodified** at
`PLACE-papers/phase2/physics-speculative/heritage/t7_arc_search_2026-04_original.py`
(md5 `4c6508c222ca027d1e2e87dc5f611857`). It used a heuristic golden-ratio axis
placement, MC = 100, seed = 42, annulus = 2°, an L-in-Gpc scan (5–28, step 1.0),
CSV output, and a Gaussian z-score. All six of those diverged from the frozen
spec; v0.2 conforms them. The heritage copy retains the old realization for audit.

## Frozen parameters conformed (prereg §4/§8)

| Parameter | Frozen value | Where |
|:--|:--|:--|
| MC seed | **770411** | `SEED_FROZEN`; `--seed` defaults to it; logged into JSON `frozen.seed` |
| MC trials | **1000** | `N_MC` |
| Annulus δθ | **1.0°** | `ANNULUS_DEG` |
| Nside | **64** | `NSIDE`; SMICA down-graded via `healpy.ud_grade` |
| Scan | **θ_min 5.0°→90.0° step 0.5°** | `THETA_MIN_LO/HI/STEP` (172 points) |
| Output | **JSON** (signal, per-θ_min p, scan array, best) | `run(..., out_json)` |
| Polarization | Stokes U sign flip on one map of each pair | `compute_signal` (`U[p0]·(−U[p1])`) |
| Toolchain | HEALPix + Healpy, NumPy, SciPy | hard imports |

A command-line override of seed/MC/Nside prints a **non-conformant** warning (§9).

## §5 significance realization (documented)

The prereg §5 requires an empirical MC p-value with a look-elsewhere correction
"applied to the L scan" over the one free parameter. Realized as the
**max-statistic over the θ_min scan within each MC trial**: each of the 1000
random-rotation nulls yields a full S(θ_min) scan; the null distribution of
`max_θ_min S` gives the global look-elsewhere-corrected p-value for the observed
best. Per-θ_min empirical p-values are also reported (from the per-column null),
with +1 smoothing so no p is exactly zero. The §5 decision table is applied to
the **global** look-elsewhere p.

## Environment (ruled §4/§8 freeze)

§4 ("the pipeline uses HEALPix and Healpy") and §8 (frozen software environment
names Healpy) make **Healpy a frozen choice**. Recon route (b) astropy-healpix is
therefore **ruled out** for the registered run — substituting the map-operations
library changes a frozen element. On Windows (no WSL, no conda present) the
registration-faithful route is **conda-forge healpy** (`conda install -c
conda-forge healpy`), installed at run-time. The pipeline logs
`healpy/numpy/scipy` versions into the JSON `environment_frozen` field at first
successful import — the §8 "software environment frozen" line, recorded at the
run rather than pre-pinned.

## Geometry — DOCUMENTED REALIZATION, author-confirm before the confirmatory run

The frozen documents delegate the seven predicted separations to "the Fano
incidence geometry" (prereg §3 step 2) and give the angle formula (T7_CMB.md
§82–86) `θ_ij = arccos(1 − (d_ij/R_LSS)²/2)`, R_LSS ≈ 14.1 Gpc, but **do not close
the seven d_ij in a single formula**. v0.2 realizes them from the incidence
structure verified in `SIDE-t7-topology-cmb v0.1` (Basic.lean §1, §6):

1. The 7 Fano points are embedded as the 7 non-zero vectors of 𝔽₂³, lifted to ℝ³
   and normalized to the unit sphere — the incidence embedding that **replaces**
   the heritage golden-ratio heuristic axes (author ruling, step 3).
2. The 7 identifications are the 7 Fano lines; each line's characteristic
   dimensionless chord `δ_ℓ` (mean pairwise chord of its 3 embedded points) fixes
   its separation via the formula.
3. The `δ_ℓ` fix the **ratios** of the seven separations (the "not equally spaced,
   follow the Fano geometry" structure, §80); the θ_min scan slides the overall
   physical scale so the smallest separation equals θ_min.

**This embedding + per-line δ_ℓ construction is the registered realization of the
"Fano incidence geometry" — RATIFIED BY THE AUTHOR 2026-07-18.** It — and the
inherited reflection-through-axis identification/arc-position model — were the one
place where the frozen spec delegated to a geometry it did not close in code; the
author has now ratified this realization as the registered geometry (tagged v0.2.1;
code logic identical to v0.2). The frozen *numerical* parameters above were
conformed exactly and were never in question. The geometry is now part of the
frozen method — no change after data are touched.

## Data (verify at intake; STOP on mismatch)

`--map COM_CMB_IQU-smica_2048_R3.00_full.fits`; `--mask` the Planck 2018 **UT78
union mask** (§2 — exact filename to be verified at intake, do not assume the
common-mask file); cross-checks NILC/SEVEM/Commander (§9). Intake protocol in
`D:\PLANCK-DATA\README.txt`: md5 each, record filename+size+md5, verify against
prereg §2/§10, STOP on any mismatch.
