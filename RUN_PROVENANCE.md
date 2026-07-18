# T₇ run provenance — intake record

Registration: `T7_CMB_PIPELINE_PREREGISTRATION_v0_1.md`. Pipeline:
`t7_arc_search.py` at `SIDE-t7-topology-cmb v0.2.1 = 1cd3827` (geometry ratified).
Intake 2026-07-18. Data used **in place** at `D:\MY-DOwnloads\DPLANCK-DATA`
(the author's download folder; not moved — cross-checks were still downloading in).

## Data files (§2; identified by checksum, §8 checklist)

| File | Bytes | MD5 | Role |
|:--|--:|:--|:--|
| `COM_CMB_IQU-smica_2048_R3.00_full.fits` | 2,013,312,960 | `ee2fc49a2eb70c2eca0d582e4aae5d05` | SMICA primary (T + Q,U) |
| `COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits` | 201,335,040 | `b607003f2b30af87f43f4f76ca044055` | intensity analysis mask |
| `COM_Mask_CMB-common-Mask-Pol_2048_R3.00.fits` | 201,335,040 | `b888bcb0a6fbd7a1c8c7a6f0e1e01d8e` | polarization mask (available) |

SMICA is size-plausible at ~1.9 GB and complete. **Cross-checks NILC/SEVEM/Commander
were still `.crdownload` (in-flight) at intake** — per the run directive, cross-checks
follow the primary run if absent; this is the SMICA primary run. A duplicate SMICA-sized
`.crdownload` and two mask-sized `.crdownload` were also present and left untouched.

## Mask ruling (dated, documented — NOT a silent swap)

Prereg §2 names the **"Planck 2018 UT78 union mask."** The downloaded mask is
`COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits`. **Ruling (2026-07-18):** the
`common-Mask-Int` at release `R3.00` (PR3 = Planck 2018) is the **release-successor**
of the UT78 union mask. "UT78" is the PR2 (2015) 78%-sky union-mask naming; the PR3
(2018) release replaced the per-component UTxx union masks with a single **common**
confidence mask, split into intensity (`-Int`) and polarization (`-Pol`) variants. The
common Int mask is the direct PR3 successor for temperature analysis; the Pol mask is
its polarization counterpart. The temperature-side search uses the Int mask (`b607003f…`).
This is a documented naming-successor reconciliation, not a substitution of a different
object.

## Environment (§8 "software environment frozen" line)

Frozen toolchain = HEALPix + Healpy (prereg §4/§8; ruled route = conda-forge healpy on
Windows). Versions logged at first successful import into the run JSON `environment_frozen`
field and recorded here after the run.

## Mask ruling — CONFIRMED (2026-07-18)

Smoke-test read of the common Int mask reports **77.9% of sky unmasked ≈ 78%**, matching
the "UT**78**" (78%-sky) fraction. The successor-naming ruling above is therefore
**CONFIRMED**: `COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits` is the PR3 realization of
the registered UT78 union mask. Not a swap.

## PRE-SIGNAL AMENDMENT — geometry re-realization (dated 2026-07-18)

**Disclosure (registration integrity).** This amendment is filed **before any map
statistic was computed.** Only header/finiteness intake reads occurred (SMICA: Nside
2048, T/Q/U present, 100% finite; mask: 77.9% unmasked) — no correlation, no signal, no
scan on real data. The degeneracy finding below derives from **geometry alone** (synthetic
maps + the abstract incidence structure), not from the CMB data. No confirmatory result
has been seen.

**The finding (not a patch).** The Fano collineation group is GL(3,𝔽₂), order 168 —
**transitive on points and on lines**. Therefore *any* realization of the seven separations
from the **abstract incidence structure alone** is symmetric under this group and is
provably (near-)degenerate. Measured: the 𝔽₂³-vector embedding gives per-line
`δ_ℓ ∈ [0.980, 1.000]`; at θ_min = 30° the seven separations span only 30.00°–30.63° — a
0.63° spread, **below the frozen annulus δθ = 1°** — collapsing the seven scales into one
resolvable annulus. This contradicts prereg §80 ("the angular scales are NOT equally
spaced"). **The seven distinct scales require the symmetry-broken PHYSICAL fundamental
domain — the T₇ surface's seven generator lengths on the Fano frame — not the bare plane.**

**Source-read (verbatim outcome).** T7_CMB.md and the pre-registration give only
`θ_ij = arccos(1 − (d_ij/R_LSS)²/2)`, `R_LSS ≈ 14.1 Gpc`, with `d_ij` = "the geodesic
distance between identified points i and j in the Fano geometry" and a fundamental-domain
"characteristic size L". The kernel `SIDE-t7-topology-cmb v0.1` (Basic.lean) encodes only
combinatorics (7 pts/lines, 21 incidences, K₇), `H₁ = ℤ ⊕ (ℤ/2)³`, and the seven-Möbius
count — **no lengths, no metric, no d_ij**. No companion cosmology paper (phase2/, clusters/,
the cosmology kernels) states seven generator lengths or an explicit d_ij. **The corpus
states no metric realization of the seven distinct scales.**

**FORK (ii) — held for the author's geometry ruling (no construction chosen silently):**
- **(a) The `H₁ = ℤ ⊕ (ℤ/2)³` split** — the ONE source-native symmetry-breaker: the
  distinguished free-ℤ generator singles out a direction that the pure-incidence realization
  lacks, so identification lengths modulated by their relation to the free axis *can* be
  distinct (unlike GL(3,𝔽₂)-symmetric constructions). But the corpus fixes no free-vs-torsion
  length ratio; a genuinely-distinct spread > δθ requires the author to supply that ratio.
- **(b) Bare incidence / K₇ eigenstructure** (eigenvalues 3, −1×6): GL(3,𝔽₂)-symmetric →
  degenerate (spread 0.63° < 1°). Ruled out by the finding.
- **(c) Explicit T₇-surface generator lengths** — the honest physical object, but the corpus
  provides no lengths; not implementable without author-supplied registered metric data.

**Ruling needed:** supply the registered metric data (the free/torsion length ratio for (a),
or an explicit seven-length / d_ij table for (c)); OR rule that the seven-scale prediction is
corpus-underdetermined as it stands. On a ruling, the geometry is re-realized exactly as
specified, **re-tagged v0.3**, re-ratified, O.9/pointer updated — and only then the run.

## Run

**HELD** — pending the FORK (ii) geometry ruling above. No run before re-ratification.
Single run when unblocked: frozen parameters, seed 770411, JSON output (no peeking, no
variation re-runs — prereg §9).
