#!/usr/bin/env python3
"""
T₇ MATCHED-ARC SEARCH IN PLANCK SMICA DATA — registration-conformed pipeline
============================================================================

Version:  v0.2 (registration-conformed, 2026-07-18)
Conforms: T7_CMB_PIPELINE_PREREGISTRATION_v0_1.md (frozen, May 2026)
Heritage: the pre-registration-era realization (April 2026, heuristic axis
          placement, MC=100, seed=42, CSV out) is preserved unmodified at
          PLACE-papers phase2/physics-speculative/heritage/
          t7_arc_search_2026-04_original.py  (md5 4c6508c222ca027d1e2e87dc5f611857).

WHAT IS FROZEN (conformed here exactly — do not change after data are touched):
  - seed            = 770411            (§8; logged into the JSON output)
  - MC trials       = 1000              (§4)
  - annulus δθ      = 1.0°              (§4)
  - Nside           = 64                (§4; SMICA downsampled via healpy.ud_grade)
  - scan parameter  = θ_min, 5.0°..90.0° step 0.5°   (§4; the one free parameter)
  - output          = JSON (signal, p-value, candidate-L/θ_min array, full scan) (§8)
  - significance    = empirical MC p-value; look-elsewhere over the scan realized
                      as the MAX-STATISTIC over the θ_min scan within each MC trial
                      (global p over the one free parameter).  [§5 realization — see
                      IMPLEMENTATION_NOTES.md]
  - polarization    = Stokes U sign flip on one map of each matched pair (§4)
  - toolchain       = HEALPix + Healpy (§4/§8; Windows: conda-forge healpy).
                      NumPy for cross-correlation, SciPy for statistics.

GEOMETRY — COMMON-SCALE REALIZATION; the seven-distinct-scale discriminator is
  CORPUS-UNDERDETERMINED (pre-signal amendment, author ruling 2026-07-18, v0.3).
  Finding: GL(3,𝔽₂) (order 168) is transitive on the Fano lines, so any realization
  of the seven separations from the ABSTRACT incidence alone is provably (near-)
  degenerate; the seven distinct scales require the physical fundamental domain's
  seven generator lengths, which the corpus states NOWHERE (source-read verbatim:
  θ_ij formula + "d_ij geodesic distance in the Fano geometry" + "characteristic
  size L", no lengths/metric). No length ratio is supplied at the instrument (a
  post-hoc free parameter — declined). This run therefore tests the REGISTERED
  SURVIVING SIGNATURE: matched arc pairs with the Stokes-U sign flip (the non-
  orientability discriminator — scale-independent, unique to 𝕋₇ in the §1 table)
  at the common Fano scale, over the frozen θ_min scan. The seven-scale COUNT
  discriminator is UNTESTED-AS-UNDERDETERMINED (not null). §5 thresholds apply
  unchanged to the MC null of the statistic actually computed. The realization below
  is the ratified incidence embedding, honestly relabeled as the common-scale form.
  The frozen documents delegate the seven predicted separations to "the Fano
  incidence geometry" (prereg §3) and give the angle formula (T7_CMB.md §82-86)
      θ_ij = arccos(1 − (d_ij / R_LSS)² / 2),   R_LSS ≈ 14.1 Gpc,
  but do not close the seven d_ij in a single formula.  This pipeline realizes
  them from the incidence structure verified in SIDE-t7-topology-cmb v0.1:
    - The 7 Fano points are embedded as the 7 non-zero vectors of 𝔽₂³, lifted to
      ℝ³ and normalized to the unit sphere — the incidence embedding, REPLACING
      the heritage golden-ratio heuristic axis placement (author ruling, step 3).
    - The 7 identifications are the 7 Fano lines (PG(2,𝔽₂)); each line's
      characteristic dimensionless chord δ_ℓ = mean pairwise chord of its 3
      embedded points gives, via the formula, its predicted separation.
    - The seven δ_ℓ fix the RATIOS of the separations (the "not equally spaced,
      follow the Fano geometry" structure, §80); the scan slides the overall
      physical scale so that the SMALLEST separation equals θ_min.
  The embedding + per-line δ_ℓ construction is the registered realization of the
  "Fano incidence geometry" — RATIFIED by the author 2026-07-18 (unchanged from
  v0.2; the geometry is now part of the frozen method).  The heritage copy retains
  the old heuristic realization.

Sources cited (docstring + IMPLEMENTATION_NOTES.md):
  - SIDE-t7-topology-cmb v0.1 (Basic.lean §1,§6): Fano PG(2,𝔽₂), K₇ collinearity.
  - T7_CMB.md §3.3, §82-86: θ_ij = arccos(1 − (d_ij/R_LSS)²/2); "7 primary scales".
  - T7_CMB_PIPELINE_PREREGISTRATION_v0_1.md: the frozen spec.

DATA (verify filenames at intake against prereg §2/§10; STOP on mismatch):
  --map    COM_CMB_IQU-smica_2048_R3.00_full.fits   (T + Q,U extensions)
  --mask   the Planck 2018 UT78 union mask           (§2; exact filename TBV at intake)
  cross-checks: NILC / SEVEM / Commander (§9).

Author: J. York Seale (ORCID 0009-0008-7993-0310).  A PLACE TO STAND — Phase 2.
"""

import argparse
import json
import sys

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy required.")
    sys.exit(1)

try:
    import healpy as hp
except ImportError:
    print("ERROR: healpy required (frozen toolchain, prereg §4/§8).")
    print("On Windows install via conda-forge:  conda install -c conda-forge healpy")
    print("(astropy-healpix is NOT a substitute — it would change a frozen choice.)")
    sys.exit(1)

try:
    import scipy
    from scipy import stats  # noqa: F401  (kept for parity; p-values are empirical)
except ImportError:
    print("ERROR: scipy required (frozen toolchain, prereg §8).")
    sys.exit(1)

# ============================================================
# FROZEN PARAMETERS (prereg §4/§8) — DO NOT CHANGE AFTER DATA
# ============================================================
SEED_FROZEN      = 770411          # §8  (77 = 7×11, × 4/81)
N_MC             = 1000            # §4
ANNULUS_DEG      = 1.0             # §4
NSIDE            = 64              # §4
THETA_MIN_LO     = 5.0            # §4  degrees
THETA_MIN_HI     = 90.0           # §4  degrees
THETA_MIN_STEP   = 0.5            # §4  degrees
R_LSS_GPC        = 14.1           # T7_CMB.md §86

# ============================================================
# FANO PLANE PG(2, 𝔽₂) — incidence structure (kernel §1)
# ============================================================
# 7 non-zero vectors of 𝔽₂³, in a fixed order = the 7 Fano points.
_F2_POINTS = [(0, 0, 1), (0, 1, 0), (0, 1, 1),
              (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]

def _fano_lines(points):
    """The 7 lines of PG(2,𝔽₂): triples {a,b,c} with a XOR b XOR c = 0."""
    idx = {v: i for i, v in enumerate(points)}
    lines = []
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = points[i], points[j]
            c = tuple(x ^ y for x, y in zip(a, b))
            k = idx[c]
            if k > j:
                lines.append((i, j, k))
    return lines

FANO_LINES = _fano_lines(_F2_POINTS)          # 7 lines
assert len(FANO_LINES) == 7, "Fano line count must be 7"

def fano_axes():
    """7 Fano points embedded as unit vectors (non-zero 𝔽₂³ lifted to ℝ³)."""
    v = np.array(_F2_POINTS, dtype=float)
    return v / np.linalg.norm(v, axis=1, keepdims=True)

def _line_delta(axes):
    """Per-line characteristic dimensionless chord δ_ℓ = mean pairwise chord."""
    deltas = []
    for (i, j, k) in FANO_LINES:
        pij = np.linalg.norm(axes[i] - axes[j])
        pik = np.linalg.norm(axes[i] - axes[k])
        pjk = np.linalg.norm(axes[j] - axes[k])
        deltas.append((pij + pik + pjk) / 3.0)
    return np.array(deltas)

def predicted_separations(theta_min_deg, axes, deltas):
    """
    The seven Fano-predicted separations for a given θ_min (the scan variable).

    Physical chord of a separation θ on the last-scattering sphere:
        c(θ) = R_LSS · sqrt(2 (1 − cos θ))          (inverse of the §86 formula)
    The δ_ℓ fix the ratios; scale so the SMALLEST separation equals θ_min:
        scale = c(θ_min) / min_ℓ δ_ℓ
        θ_ℓ   = arccos(1 − (scale · δ_ℓ / R_LSS)² / 2)     (clipped to ≤ π)
    Returns an array of 7 separations (radians), one per Fano line.
    """
    th_min = np.radians(theta_min_deg)
    c_min = R_LSS_GPC * np.sqrt(max(2.0 * (1.0 - np.cos(th_min)), 0.0))
    scale = c_min / deltas.min()
    x = np.clip(1.0 - (scale * deltas / R_LSS_GPC) ** 2 / 2.0, -1.0, 1.0)
    return np.arccos(x)

# ============================================================
# IDENTIFICATION + CORRELATION
# ============================================================
def _reflect_through_axis(vecs, axis):
    """Orientation-reversing Möbius reflection v ↦ v − 2(v·n)n."""
    dots = vecs @ axis
    return vecs - 2.0 * np.outer(dots, axis)

def compute_signal(T, Q, U, nside, separations, axes, annulus_rad, pix_step):
    """
    Combined matched-arc signal S = S_T + S_P over the seven Fano identifications.

    For each Fano line ℓ (axis = its polar point) and its predicted separation
    θ_ℓ: reflect each sampled pixel through the axis, keep pairs whose actual
    angular separation is within δθ of θ_ℓ, accumulate temperature cross-correlation
    and Stokes-U sign-flipped correlation.
    """
    npix = hp.nside2npix(nside)
    pix = np.arange(0, npix, pix_step)
    vecs = np.array(hp.pix2vec(nside, pix)).T            # (Npix_s, 3)

    S_T = 0.0
    S_P = 0.0
    for li, (i, j, k) in enumerate(FANO_LINES):
        axis = axes[i]                                   # line's incidence axis
        theta_l = separations[li]
        refl = _reflect_through_axis(vecs, axis)
        refl /= np.linalg.norm(refl, axis=1, keepdims=True)
        partner = hp.vec2pix(nside, refl[:, 0], refl[:, 1], refl[:, 2])
        cos_sep = np.clip(np.einsum('ij,ij->i', vecs,
                                    np.array(hp.pix2vec(nside, partner)).T), -1, 1)
        ang = np.arccos(cos_sep)
        sel = np.abs(ang - theta_l) < annulus_rad
        if not np.any(sel):
            continue
        p0 = pix[sel]
        p1 = partner[sel]
        n = p0.size
        S_T += np.sum(T[p0] * T[p1]) / n
        S_P += np.sum(U[p0] * (-U[p1])) / n              # Möbius U sign flip
    return S_T + S_P, S_T, S_P

def scan_signal(T, Q, U, nside, axes, deltas, theta_grid, annulus_rad, pix_step):
    """Signal S(θ_min) across the full frozen θ_min scan."""
    out = np.empty(theta_grid.size)
    for m, tm in enumerate(theta_grid):
        seps = predicted_separations(tm, axes, deltas)
        out[m], _, _ = compute_signal(T, Q, U, nside, seps, axes,
                                      annulus_rad, pix_step)
    return out

# ============================================================
# MAIN
# ============================================================
def run(map_file, mask_file=None, nside_out=NSIDE, n_mc=N_MC, seed=SEED_FROZEN,
        pix_step=None, out_json="t7_results.json"):
    versions = {"healpy": hp.__version__, "numpy": np.__version__,
                "scipy": scipy.__version__}
    print("Frozen environment (prereg §8):", versions)

    theta_grid = np.arange(THETA_MIN_LO, THETA_MIN_HI + THETA_MIN_STEP / 2,
                           THETA_MIN_STEP)
    annulus_rad = np.radians(ANNULUS_DEG)
    axes = fano_axes()
    deltas = _line_delta(axes)

    print("Loading SMICA map (T,Q,U)...")
    T, Q, U = hp.read_map(map_file, field=(0, 1, 2))
    nside_in = hp.get_nside(T)
    if nside_in != nside_out:
        T = hp.ud_grade(T, nside_out)
        Q = hp.ud_grade(Q, nside_out)
        U = hp.ud_grade(U, nside_out)
    npix = hp.nside2npix(nside_out)

    if mask_file:
        mask = hp.read_map(mask_file)
        if hp.get_nside(mask) != nside_out:
            mask = hp.ud_grade(mask, nside_out)
        mask = mask > 0.5
        for mp in (T, Q, U):
            mp[~mask] = hp.UNSEEN
        T = np.where(mask, T, 0.0); Q = np.where(mask, Q, 0.0); U = np.where(mask, U, 0.0)

    if pix_step is None:
        pix_step = max(1, npix // 5000)

    print("Observed scan over θ_min ∈ [%.1f, %.1f]° step %.1f° (%d points)..."
          % (THETA_MIN_LO, THETA_MIN_HI, THETA_MIN_STEP, theta_grid.size))
    obs = scan_signal(T, Q, U, nside_out, axes, deltas, theta_grid,
                      annulus_rad, pix_step)
    obs_max = float(np.max(obs))
    obs_argmax = int(np.argmax(obs))

    print("Monte Carlo null: %d random rotations (seed %d)..." % (n_mc, seed))
    rng = np.random.RandomState(seed)
    null_scan = np.empty((n_mc, theta_grid.size))
    for t in range(n_mc):
        a = rng.uniform(0, 2 * np.pi)
        b = np.arccos(rng.uniform(-1, 1))
        g = rng.uniform(0, 2 * np.pi)
        rot = hp.rotator.Rotator(rot=[a, b, g], eulertype='ZYZ')
        Tr = rot.rotate_map_pixel(T)
        Qr = rot.rotate_map_pixel(Q)
        Ur = rot.rotate_map_pixel(U)
        null_scan[t] = scan_signal(Tr, Qr, Ur, nside_out, axes, deltas,
                                   theta_grid, annulus_rad, pix_step)
        if (t + 1) % 50 == 0:
            print("  MC %d/%d" % (t + 1, n_mc))

    # Per-θ_min empirical p-values (one-sided, +1 smoothing).
    p_per = [(1 + int(np.sum(null_scan[:, m] >= obs[m]))) / (n_mc + 1)
             for m in range(theta_grid.size)]
    # Look-elsewhere global p: max-statistic over the scan within each MC trial (§5).
    null_max = np.max(null_scan, axis=1)
    p_global = (1 + int(np.sum(null_max >= obs_max))) / (n_mc + 1)

    def _interpret(p):
        if p < 0.001: return "A_detection"
        if p < 0.01:  return "B_suggestive"
        if p < 0.05:  return "D_marginal"
        return "C_null"

    result = {
        "pipeline": "t7_arc_search.py v0.2 (registration-conformed)",
        "preregistration": "T7_CMB_PIPELINE_PREREGISTRATION_v0_1.md",
        "frozen": {"seed": seed, "n_mc": n_mc, "nside": nside_out,
                   "annulus_deg": ANNULUS_DEG,
                   "theta_min_scan_deg": [THETA_MIN_LO, THETA_MIN_HI, THETA_MIN_STEP]},
        "environment_frozen": versions,          # §8 "environment frozen" line
        "test_scope": ("SURVIVING SIGNATURE (matched-arc + Stokes-U sign flip at the "
                       "common Fano scale). Seven-distinct-scale COUNT discriminator is "
                       "UNTESTED-AS-UNDERDETERMINED (corpus specifies no generator "
                       "lengths; GL(3,F2) transitivity forces near-degeneracy). v0.3."),
        "geometry": "common-scale Fano-incidence realization (v0.3; see docstring amendment)",
        "inputs": {"map": map_file, "mask": mask_file},
        "theta_min_deg": [float(x) for x in theta_grid],
        "signal_scan": [float(x) for x in obs],
        "p_value_per_theta_min": [float(x) for x in p_per],
        "best": {"theta_min_deg": float(theta_grid[obs_argmax]),
                 "signal": obs_max,
                 "p_global_look_elsewhere": float(p_global)},
        "decision_global": _interpret(p_global),   # §5 table on the look-elsewhere p
    }
    with open(out_json, "w") as f:
        json.dump(result, f, indent=2)
    print("\nBest θ_min = %.1f°, S = %.4f, global p (look-elsewhere) = %.4g -> %s"
          % (theta_grid[obs_argmax], obs_max, p_global, result["decision_global"]))
    print("Wrote", out_json)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="T7 matched-arc search (registration-conformed)")
    ap.add_argument("--map", required=True, help="SMICA IQU FITS (prereg §2)")
    ap.add_argument("--mask", default=None, help="Planck 2018 UT78 union mask (prereg §2)")
    ap.add_argument("--seed", type=int, default=SEED_FROZEN,
                    help="frozen MC seed (default 770411, prereg §8)")
    ap.add_argument("--nmc", type=int, default=N_MC, help="MC trials (frozen 1000)")
    ap.add_argument("--nside", type=int, default=NSIDE, help="analysis Nside (frozen 64)")
    ap.add_argument("--pixstep", type=int, default=None, help="pixel subsampling stride")
    ap.add_argument("--out", default="t7_results.json", help="JSON output path")
    args = ap.parse_args()
    if args.seed != SEED_FROZEN or args.nmc != N_MC or args.nside != NSIDE:
        print("WARNING: a frozen parameter was overridden on the command line — "
              "the run is NO LONGER registration-conformant (prereg §9).")
    run(args.map, mask_file=args.mask, nside_out=args.nside, n_mc=args.nmc,
        seed=args.seed, pix_step=args.pixstep, out_json=args.out)
