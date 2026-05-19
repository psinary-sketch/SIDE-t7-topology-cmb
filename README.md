# SIDE-t7-topology-cmb v0.1

Kernel verification of the load-bearing structural facts of the T₇ topology for the cosmic microwave background.

## Status

| | |
|---|---|
| Toolchain | `leanprover/lean4:v4.29.0-rc8` |
| Mathlib | not required |
| sorry | 0 |
| axioms | 0 |

Companion paper: `T7_TOPOLOGY_CMB_PAPER`. Related: `MATTER_AS_ARITHMETIC_v1_0_CONSOLIDATED.md`, `FANO_PLANE_OF_ARITHMETIC.md`.

## The structure

T₇ is the Klein surface with seven Möbius strips on the Fano frame. Its first homology group is

```
H₁(𝕋₇) = ℤ ⊕ (ℤ/2)³
```

The torsion factor (ℤ/2)³ has 8 elements; 7 are non-zero (the Fano points).

The Möbius identifications produce matched arc pairs in the CMB — not matched circles, because Möbius is non-orientable. The matched-arc count is 7, matching the Fano point count.

The B-mode polarization signature reflects (Stokes U sign flip) under Möbius identification — a signature no orientable topology produces.

## Comparison with competing topologies

| Topology | Matched features | Orientable |
|---|---|---|
| 3-torus | 3 circle pairs | yes |
| Poincaré dodecahedron | 6 circle pairs | yes |
| **T₇** | **7 arc pairs** | **no** |
| infinite flat | 0 | yes |

## What's verified

### §1 — Fano combinatorics
- Points (7), Lines (7), Points per line (3), Lines per point (3)
- Double counting: 7 × 3 = 3 × 7 (`fano_double_counting`)
- 21 incidences (`twenty_one_incidences`)
- Self-duality of Fano (`fano_self_dual`)

### §2 — T₇ first homology
- H₁ free rank 1, torsion rank 3
- Torsion cardinality = 2³ = 8 (`T7_torsion_eight`)
- Non-zero torsion count = 7 (`T7_torsion_nonzero_seven`)
- `T7_torsion_matches_fano`

### §3 — Möbius strips
- 7 Möbius strips, non-orientable
- `mobius_count_matches_fano`

### §4 — Matched-arc prediction
- 7 matched arc pairs (`matched_arc_count`)
- `matched_arcs_equal_mobius_count`
- Polarization reflects under Möbius identification

### §5 — Distinction from competing topologies
- Each named topology with its feature count and orientability
- `T7_nonorientable`, `T7_unique_arc_count`

### §6 — Fano collinearity spectrum
- Dominant eigenvalue multiplicity 1, subdominant eigenspace dimension 6
- Sum matches Fano point count (`spectrum_total_matches_fano`)

### §7 — Bridge to the dark sector
- `dark_factorization`: 77 = 7 × 11 (Fano count × necessity ceiling)

### §8 — Cubit substrate
- Cubit cardinality = 8 (`cubit_cardinality_eight`)
- `cubit_matches_torsion`: 8 = H₁ torsion cardinality
- `cubit_nonzero_eq_fano`: 8 − 1 = 7

### §9 — GL(3, 𝔽₂) order
- 168 = 24 × 7 (`GL3F2_factorization`, `GL3F2_value`)

### §10 — CMB search pipeline parameters
- HEALPix Nside = 64
- Monte Carlo trials = 1000

### §11 — Resolution floor
- 1/(cubit cardinality × p_min) = 1/16 (`resolution_floor_sixteen`)
- Inherited from `SIDE-silence-principle` §7

### §12 — Falsification routes
- Four falsification routes catalogued in their own section.

## Build

```bash
lake build
```

Self-contained — no Mathlib.

## Federation context

| Kernel | Role for the cosmology constellation |
|---|---|
| SIDE-omega-b | Ω_b = 4/81 |
| SIDE-quaternionic-dark-sector | Dark/visible ratio decomposition |
| **SIDE-t7-topology-cmb** | **Spatial topology prediction for the CMB** |
| SIDE-silence-principle | Resolution floor inheritance |
| SIDE-substrate-cluster | The (ℤ/2)³ substrate labelings |

## License

CC-BY 4.0.

> Seale, J. Y. (2026). *SIDE-t7-topology-cmb v0.1: The T₇ Topology and the Cosmic Microwave Background.* A PLACE TO STAND Research Programme.

---

`:: → · ← ::`

*Seven Möbius strips on the Fano frame. Seven matched arc pairs in the sky.*
