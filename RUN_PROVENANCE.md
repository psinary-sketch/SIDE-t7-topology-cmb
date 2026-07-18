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

## PRE-SIGNAL AMENDMENT 2 — surviving-signature run (author ruling 2026-07-18, v0.3)

**Ruling.** The seven-DISTINCT-scale discriminator is **corpus-underdetermined** and is
FILED as a finding (no metric realization stated anywhere; the abstract-incidence
realization is provably near-degenerate by GL(3,𝔽₂) transitivity). **No length ratio is
supplied at the instrument** — any ratio now would be a post-hoc free parameter, declined.

**What today's run tests.** The REGISTERED **SURVIVING SIGNATURE**: matched arc pairs with
the **Stokes-U sign flip** — the non-orientability discriminator, **scale-independent**,
unique to 𝕋₇ in the §1 table (3-torus / dodecahedron / infinite-flat all lack it) — at the
common Fano scale, over the frozen θ_min scan. The **seven-scale COUNT discriminator is
marked UNTESTED-AS-UNDERDETERMINED, not null.** §5 thresholds apply unchanged to the MC null
of the statistic actually computed. The verdict sentence is scoped to "matched-arc +
polarization-reflection at common scale," never to the untested seven-scale claim.

Pipeline re-tagged **v0.3** (numerics unchanged from the conformed form; the geometry stays
the ratified incidence realization, now honestly labeled the common-scale realization).

## Run — executed 2026-07-18 (single, frozen, seed 770411)

Pipeline `t7_arc_search.py` at **v0.3 = `8eb0d5a`**. Env: healpy 1.19.0 / numpy 2.5.1 /
scipy 1.18.0. Inputs: SMICA `ee2fc49a…` + common Int mask `b607003f…`. Output
`t7_results.json` (md5 `a340fabf74c720f39cdcbd994177fc47`).

**Platform note (no numeric effect, code untouched).** The first invocation crashed on a
Windows cp1252 console `UnicodeEncodeError` printing a status line with `θ/∈/°` —
**before any correlation was computed** (crash at the pre-scan status print; no statistic
seen). Re-run with `PYTHONIOENCODING=utf-8` set at the environment level; the frozen v0.3
code is byte-identical. Seed 770411 is deterministic, so this is the one registered
analysis, not a variation re-run.

**Result (surviving-signature test — matched arc + Stokes-U sign flip at the common Fano scale):**
- Best `θ_min = 54.0°`; signal `S = 7.10e-09` (map-unit², effectively zero in absolute terms).
- **Global look-elsewhere p = 0.04595** (max-statistic over the 171-point θ_min scan; 45 of
  1000 rotated-sky nulls matched/exceeded the real-sky max, 46/1001).
- Scan: 171 points (θ_min 5.0°–90.0° step 0.5°); 40/171 per-θ_min p<0.05, 23 p<0.01; per-θ_min p floor 0.000999.
- **§5 verdict letter: D — MARGINAL** (0.01 ≤ p < 0.05). Per §6 Outcome D: **published as null,
  flagged for higher-resolution follow-up.** NOT a detection, NOT suggestive.

**Scope (honest).** This verdict is on the **surviving signature at the common Fano scale**,
never on the seven-distinct-scale count (which is UNTESTED-AS-UNDERDETERMINED, filed as a
finding). The absolute signal is ~zero; the marginal p sits on a weakened (single-scale)
discriminator and is well within reach of the residual foreground / ISW modulation §4.1
flags. Route-#1 falsifier (§12: "zero signal across all candidate L") is **not cleanly met**
(a marginal excess at θ_min = 54°) and **not a detection** — the pre-committed reading is the
Marginal band. The result NOTE is drafted in the empirical grammar and **HELD for author
review before any keystone / census / cosmology-constellation edits.**
