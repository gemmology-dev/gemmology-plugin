# Crystal Description Language (CDL) Specification

**Version**: 1.0.0
**Status**: Draft

---

## Table of Contents

1. [Introduction](#introduction)
2. [Syntax Overview](#syntax-overview)
3. [Crystal Systems](#crystal-systems)
4. [Point Groups](#point-groups)
5. [Miller Indices](#miller-indices)
6. [Forms](#forms)
7. [Modifications](#modifications)
8. [Twins](#twins)
9. [Grammar Reference](#grammar-reference)
10. [Examples](#examples)
11. [Appendices](#appendices)

---

## Introduction

The Crystal Description Language (CDL) is a compact, human-readable notation for describing crystal morphology. It enables precise specification of:

- Crystal system and symmetry (point group)
- Crystal forms via Miller indices
- Combinations of multiple forms with relative scaling
- Morphological modifications (elongation, truncation, tapering)
- Twinning configurations

### Design Goals

1. **Concise**: A single line can describe complex crystal morphology
2. **Precise**: Uses crystallographic notation (Miller indices, point groups)
3. **Expressive**: Supports combinations, modifications, and twins
4. **Parsable**: Unambiguous grammar for machine processing

### Basic Example

```
cubic[m3m]:{111}@1.0 + {100}@0.3 | elongate(c:1.2)
```

This describes a cubic crystal with m3m symmetry, showing octahedral {111} faces at full scale plus cube {100} faces at 0.3 scale (truncations), elongated 1.2× along the c-axis.

---

## Syntax Overview

### General Format

```
system[point_group]:form_list [| modifications] [| twin]
```

| Component | Required | Description |
|-----------|----------|-------------|
| `system` | Yes | One of the 7 crystal systems |
| `[point_group]` | No | One of 32 crystallographic point groups |
| `form_list` | Yes | One or more forms separated by `+` |
| `modifications` | No | Comma-separated list of modifications |
| `twin` | No | Twin law specification |

### Whitespace

Whitespace is generally ignored except:
- Required space after `|` separators
- No spaces within Miller indices `{111}`

### Case Sensitivity

- System names: case-insensitive (`cubic`, `CUBIC`, `Cubic` all valid)
- Point groups: case-sensitive (`m3m` not `M3M`)
- Form names: case-insensitive (`octahedron`, `Octahedron`)
- Twin laws: case-insensitive (`spinel`, `Spinel`)

---

## Crystal Systems

CDL supports all seven crystal systems:

| System | Axes | Angles | Symmetry |
|--------|------|--------|----------|
| `cubic` | a = b = c | α = β = γ = 90° | Highest |
| `tetragonal` | a = b ≠ c | α = β = γ = 90° | |
| `orthorhombic` | a ≠ b ≠ c | α = β = γ = 90° | |
| `hexagonal` | a = b ≠ c | α = β = 90°, γ = 120° | |
| `trigonal` | a = b = c | α = β = γ ≠ 90° | |
| `monoclinic` | a ≠ b ≠ c | α = γ = 90°, β ≠ 90° | |
| `triclinic` | a ≠ b ≠ c | α ≠ β ≠ γ | Lowest |

### System-Specific Behavior

Each system has a default point group used when none is specified:

| System | Default Point Group |
|--------|-------------------|
| `cubic` | `m3m` |
| `tetragonal` | `4/mmm` |
| `orthorhombic` | `mmm` |
| `hexagonal` | `6/mmm` |
| `trigonal` | `-3m` |
| `monoclinic` | `2/m` |
| `triclinic` | `-1` |

---

## Point Groups

### The 32 Crystallographic Point Groups

Point groups define the symmetry operations that generate equivalent faces from a single Miller index.

#### Cubic System (5 point groups)

| Point Group | Order | Symmetry Elements | Example Minerals |
|-------------|-------|-------------------|------------------|
| `m3m` (m-3m) | 48 | 3×4-fold, 4×3-fold, 6×2-fold, 9 mirrors, inversion | Diamond, fluorite, garnet |
| `432` | 24 | 3×4-fold, 4×3-fold, 6×2-fold | Cuprite (rare) |
| `-43m` | 24 | 3×4-fold (rotoinversion), 4×3-fold, 6 mirrors | Sphalerite, tetrahedrite |
| `m-3` (m3) | 24 | 4×3-fold, 3×2-fold, 3 mirrors, inversion | Pyrite |
| `23` | 12 | 4×3-fold, 3×2-fold | Ullmannite |

#### Hexagonal System (7 point groups)

| Point Group | Order | Example Minerals |
|-------------|-------|------------------|
| `6/mmm` | 24 | Beryl, graphite |
| `622` | 12 | β-quartz (high temp) |
| `6mm` | 12 | Wurtzite, greenockite |
| `-6m2` | 12 | Benitoite |
| `6/m` | 12 | Apatite |
| `-6` | 6 | |
| `6` | 6 | Nepheline |

#### Trigonal System (5 point groups)

| Point Group | Order | Example Minerals |
|-------------|-------|------------------|
| `-3m` (3m) | 12 | Corundum, calcite, tourmaline |
| `32` | 6 | α-quartz, cinnabar |
| `3m` | 6 | Proustite, pyrargyrite |
| `-3` | 6 | Dolomite, ilmenite |
| `3` | 3 | |

#### Tetragonal System (7 point groups)

| Point Group | Order | Example Minerals |
|-------------|-------|------------------|
| `4/mmm` | 16 | Zircon, rutile |
| `422` | 8 | |
| `4mm` | 8 | |
| `-42m` | 8 | Chalcopyrite, urea |
| `4/m` | 8 | Scheelite, scapolite |
| `-4` | 4 | |
| `4` | 4 | |

#### Orthorhombic System (3 point groups)

| Point Group | Order | Example Minerals |
|-------------|-------|------------------|
| `mmm` | 8 | Topaz, olivine, barite |
| `222` | 4 | Epsomite |
| `mm2` | 4 | Hemimorphite |

#### Monoclinic System (3 point groups)

| Point Group | Order | Example Minerals |
|-------------|-------|------------------|
| `2/m` | 4 | Orthoclase, gypsum, epidote |
| `m` | 2 | |
| `2` | 2 | Tartaric acid |

#### Triclinic System (2 point groups)

| Point Group | Order | Example Minerals |
|-------------|-------|------------------|
| `-1` | 2 | Microcline, albite, kyanite |
| `1` | 1 | |

### How Point Groups Generate Forms

Given a Miller index {hkl} and point group, the symmetry operations generate all equivalent face normals:

**Example: `m3m` with {111}**
1. Start with face normal [1,1,1]/√3
2. Apply 48 symmetry operations (24 rotations × 2 with/without inversion)
3. Get 8 unique normals → octahedron

**Example: `m3m` with {211}**
1. Start with face normal [2,1,1]/√6
2. Apply 48 operations → 24 unique normals
3. Result: trapezohedron (icositetrahedron)

**Example: `m3` (pyrite group) with {210}**
1. Start with face normal [2,1,0]/√5
2. Apply 24 operations → 12 unique normals
3. Result: pyritohedron (not 24 faces like in m3m)

---

## Miller Indices

### Three-Index Notation {hkl}

Used for cubic, tetragonal, orthorhombic, monoclinic, and triclinic systems.

```
{hkl} where h, k, l are integers (positive, negative, or zero)
```

**Notation conventions:**
- Curly braces `{}` denote a form (all symmetry-equivalent faces)
- Parentheses `()` denote a single face (not used in CDL)
- Negative indices written with leading minus: `{1-11}` means (1, -1, 1)

**Common cubic forms:**

| Miller Index | Form Name | Faces |
|--------------|-----------|-------|
| `{100}` | Cube | 6 |
| `{110}` | Rhombic dodecahedron | 12 |
| `{111}` | Octahedron | 8 |
| `{210}` | Tetrahexahedron / Pyritohedron | 24 / 12 |
| `{211}` | Trapezohedron | 24 |
| `{221}` | Trisoctahedron | 24 |
| `{321}` | Hexoctahedron | 48 |

### Four-Index (Miller-Bravais) Notation {hkil}

Used for hexagonal and trigonal systems. The third index `i` is redundant: `i = -(h+k)`

```
{hkil} where i = -(h+k)
```

**Writing convention:**
- Write as four digits with minus signs: `{10-10}` means h=1, k=0, i=-1, l=0
- The `i` index is included for symmetry clarity

**Common hexagonal forms:**

| Miller-Bravais | Form Name | Faces |
|----------------|-----------|-------|
| `{0001}` | Basal pinacoid | 2 |
| `{10-10}` | First-order prism | 6 |
| `{11-20}` | Second-order prism | 6 |
| `{10-11}` | Positive rhombohedron | 6 |
| `{01-11}` | Negative rhombohedron | 6 |
| `{10-12}` | Dipyramid | 12 |

---

## Forms

### Form Specification Syntax

```
form = form_name | miller_index
form_with_scale = form "@" scale
```

Where:
- `form_name`: Named form like `octahedron`, `cube`, `prism`
- `miller_index`: Miller index like `{111}`, `{10-10}`
- `scale`: Float value (default 1.0)

### Scale Interpretation

The scale determines the relative distance from the crystal center to each face:

| Scale | Meaning |
|-------|---------|
| `1.0` | Full extension (dominant form) |
| `0.5` | Half distance (intermediate truncation) |
| `0.1` | Small distance (minor truncation) |
| `> 1.0` | Extended beyond normal |

**Combining forms:**
```
{111}@1.0 + {100}@0.3
```
Creates an octahedron with cube face truncations at the corners.

### Named Forms by System

#### Cubic

| Name | Miller Index | Faces |
|------|--------------|-------|
| `cube` | {100} | 6 |
| `octahedron` | {111} | 8 |
| `dodecahedron` | {110} | 12 |
| `trapezohedron` | {211} | 24 |
| `tetrahexahedron` | {210} | 24 |
| `trisoctahedron` | {221} | 24 |
| `hexoctahedron` | {321} | 48 |

#### Hexagonal/Trigonal

| Name | Miller-Bravais | Faces |
|------|----------------|-------|
| `pinacoid` / `basal` | {0001} | 2 |
| `prism` / `prism_1` | {10-10} | 6 |
| `prism_2` | {11-20} | 6 |
| `rhombohedron` / `rhomb_pos` | {10-11} | 6 |
| `rhomb_neg` | {01-11} | 6 |
| `dipyramid` / `dipyramid_1` | {10-11} | 12 |
| `dipyramid_2` | {11-22} | 12 |
| `scalenohedron` | {21-31} | 12 |

#### Tetragonal

| Name | Miller Index | Faces |
|------|--------------|-------|
| `prism_1` | {100} | 4 |
| `prism_2` | {110} | 4 |
| `pinacoid` / `basal` | {001} | 2 |
| `dipyramid_1` | {101} | 8 |
| `dipyramid_2` | {111} | 8 |

#### Orthorhombic

| Name | Miller Index | Faces |
|------|--------------|-------|
| `pinacoid_a` | {100} | 2 |
| `pinacoid_b` | {010} | 2 |
| `pinacoid_c` | {001} | 2 |
| `prism_ab` | {110} | 4 |
| `prism_ac` | {101} | 4 |
| `prism_bc` | {011} | 4 |
| `dipyramid` | {111} | 8 |

---

## Modifications

Modifications alter the base crystal geometry.

### Syntax

```
modifications = modification ("," modification)*
modification = mod_type "(" params ")"
```

### Elongation

Stretches the crystal along an axis.

```
elongate(axis:ratio)
```

| Parameter | Values | Default |
|-----------|--------|---------|
| `axis` | `a`, `b`, `c` | `c` |
| `ratio` | float > 0 | 1.0 |

**Examples:**
```
elongate(c:1.5)     # 1.5× longer along c-axis
elongate(c:0.5)     # 0.5× (flattened) along c-axis
elongate(a:2.0)     # 2× longer along a-axis
```

### Truncation

Explicitly truncates a form (alternative to using scale).

```
truncate(form:depth)
```

| Parameter | Values | Default |
|-----------|--------|---------|
| `form` | Miller index or form name | required |
| `depth` | 0.0 to 1.0 | 0.5 |

**Examples:**
```
truncate({100}:0.2)      # Shallow cube truncations
truncate(octahedron:0.5) # Moderate octahedron truncations
```

### Tapering

Narrows the crystal toward one end (for barrel, pyramidal habits).

```
taper(direction:factor)
```

| Parameter | Values | Default |
|-----------|--------|---------|
| `direction` | `+a`, `-a`, `+b`, `-b`, `+c`, `-c` | `+c` |
| `factor` | 0.0 to 1.0 | 0.7 |

**Examples:**
```
taper(+c:0.7)    # Top is 70% of bottom width
taper(-c:0.8)    # Bottom is 80% of top width
```

### Bevel

Chamfers edges between forms.

```
bevel(edges:width)
```

| Parameter | Values | Default |
|-----------|--------|---------|
| `edges` | `all` or edge spec | `all` |
| `width` | float > 0 | 0.1 |

**Examples:**
```
bevel(all:0.1)           # Bevel all edges
bevel({111}∩{100}:0.05)  # Bevel only octahedron-cube edges
```

---

## Twins

### Syntax

```
twin = "twin(" law ["," count] ")"
     | "twin(" axis "," angle ["," type] ")"
```

### Named Twin Laws

| Law | Axis | Angle | Type | Systems | Minerals |
|-----|------|-------|------|---------|----------|
| `spinel` | [111] | 180° | contact | cubic | Spinel, diamond |
| `iron_cross` | [001] | 90° | penetration | cubic | Pyrite |
| `brazil` | [11-20] | reflection | penetration | trigonal | Quartz |
| `dauphine` | [0001] | 180° | penetration | trigonal | Quartz |
| `japan` | [11-22] | 84.55° | contact | trigonal | Quartz |
| `carlsbad` | [001] | 180° | penetration | monoclinic | Orthoclase |
| `baveno` | [021] | 180° | contact | monoclinic | Orthoclase |
| `manebach` | [001] | 180° | contact | monoclinic | Orthoclase |
| `albite` | [010] | 180° | polysynthetic | triclinic | Plagioclase |
| `pericline` | [010] | 180° | polysynthetic | triclinic | Plagioclase |

### Twin Count

Default is 2 (simple twin). Higher counts for cyclic twins:

```
twin(spinel)         # Simple twin (2 individuals)
twin(spinel,3)       # Cyclic twin (3 individuals at 120°)
twin(japan,6)        # Sextupling (6 individuals)
```

### Custom Twin Specification

```
twin([1,1,1],180,contact)    # Same as spinel law
twin([0,0,1],90,penetration) # Same as iron cross
```

---

## Grammar Reference

### Complete EBNF Grammar

```ebnf
(* Top-level *)
crystal         = system , [ "[" , point_group , "]" ] , ":" , form_list ,
                  [ "|" , mod_list ] , [ "|" , twin_spec ] ;

(* System *)
system          = "cubic" | "tetragonal" | "orthorhombic" | "hexagonal"
                | "trigonal" | "monoclinic" | "triclinic" ;

(* Point group - 32 valid values *)
point_group     = cubic_pg | hexagonal_pg | trigonal_pg | tetragonal_pg
                | orthorhombic_pg | monoclinic_pg | triclinic_pg ;

cubic_pg        = "m3m" | "432" | "-43m" | "m-3" | "23" ;
hexagonal_pg    = "6/mmm" | "622" | "6mm" | "-6m2" | "6/m" | "-6" | "6" ;
trigonal_pg     = "-3m" | "32" | "3m" | "-3" | "3" ;
tetragonal_pg   = "4/mmm" | "422" | "4mm" | "-42m" | "4/m" | "-4" | "4" ;
orthorhombic_pg = "mmm" | "222" | "mm2" ;
monoclinic_pg   = "2/m" | "m" | "2" ;
triclinic_pg    = "-1" | "1" ;

(* Forms *)
form_list       = form , { "+" , form } ;
form            = ( form_name | miller_index ) , [ "@" , scale ] ;
form_name       = identifier ;
miller_index    = "{" , hkl , "}" ;
hkl             = integer , integer , integer , [ integer ] ;
integer         = [ "-" ] , digit , { digit } ;
scale           = float ;

(* Modifications *)
mod_list        = modification , { "," , modification } ;
modification    = elongate | truncate | taper | bevel ;
elongate        = "elongate" , "(" , axis , ":" , float , ")" ;
truncate        = "truncate" , "(" , ( miller_index | form_name ) , ":" , float , ")" ;
taper           = "taper" , "(" , direction , ":" , float , ")" ;
bevel           = "bevel" , "(" , ( "all" | edge_spec ) , ":" , float , ")" ;
axis            = "a" | "b" | "c" ;
direction       = ( "+" | "-" ) , axis ;
edge_spec       = miller_index , "∩" , miller_index ;

(* Twins *)
twin_spec       = "twin" , "(" , twin_def , ")" ;
twin_def        = twin_law , [ "," , integer ]
                | vector , "," , float , [ "," , twin_type ] ;
twin_law        = "spinel" | "iron_cross" | "brazil" | "dauphine" | "japan"
                | "carlsbad" | "baveno" | "manebach" | "albite" | "pericline" ;
twin_type       = "contact" | "penetration" | "cyclic" ;
vector          = "[" , float , "," , float , "," , float , "]" ;

(* Primitives *)
float           = [ "-" ] , digit , { digit } , [ "." , { digit } ] ;
digit           = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
identifier      = letter , { letter | digit | "_" } ;
letter          = "a" | ... | "z" | "A" | ... | "Z" ;
```

### Reserved Words

```
cubic tetragonal orthorhombic hexagonal trigonal monoclinic triclinic
elongate truncate taper bevel twin
all contact penetration cyclic
spinel iron_cross brazil dauphine japan carlsbad baveno manebach albite pericline
```

---

## Examples

### Simple Crystals

```bash
# Diamond octahedron
cubic[m3m]:{111}

# Fluorite cube
cubic[m3m]:{100}

# Garnet dodecahedron
cubic[m3m]:{110}

# Pyrite cube (lower symmetry - note m3 not m3m)
cubic[m3]:{100}
```

### Combined Forms

```bash
# Truncated octahedron (cube corners)
cubic[m3m]:{111}@1.0 + {100}@0.3

# Truncated cube (octahedron corners)
cubic[m3m]:{100}@1.0 + {111}@0.3

# Cubo-octahedron (equal faces)
cubic[m3m]:{100}@1.0 + {111}@1.0

# Garnet with trapezohedron
cubic[m3m]:{110}@1.0 + {211}@0.5

# Complex modified diamond
cubic[m3m]:{111}@1.0 + {110}@0.4 + {100}@0.2
```

### Hexagonal/Trigonal Crystals

```bash
# Beryl (emerald) - hexagonal prism
hexagonal[6/mmm]:{10-10}@1.0 + {0001}

# Elongated beryl
hexagonal[6/mmm]:{10-10}@1.0 + {0001} | elongate(c:1.5)

# Quartz - prism with rhombohedra
trigonal[32]:{10-10}@1.0 + {10-11}@0.8 + {01-11}@0.8 | elongate(c:2.0)

# Corundum barrel (ruby/sapphire)
trigonal[-3m]:{10-10}@1.0 + {0001}@0.8 | taper(+c:0.7), elongate(c:1.3)

# Calcite rhombohedron
trigonal[-3m]:{10-11}
```

### Tetragonal Crystals

```bash
# Zircon - prism with dipyramid
tetragonal[4/mmm]:{100}@1.0 + {101}@0.9 | elongate(c:1.6)

# Rutile
tetragonal[4/mmm]:{100}@1.0 + {110}@0.5 + {101}@0.3 | elongate(c:1.4)
```

### Orthorhombic Crystals

```bash
# Topaz
orthorhombic[mmm]:{110}@1.0 + {120}@0.7 + {001}@0.5 | elongate(c:1.8)

# Olivine
orthorhombic[mmm]:{110}@1.0 + {010}@0.6 + {021}@0.4
```

### Twinned Crystals

```bash
# Spinel twin (macle)
cubic[m3m]:{111} | twin(spinel)

# Penetration twin (iron cross pyrite)
cubic[m3]:{100} | twin(iron_cross)

# Brazil twin quartz
trigonal[32]:{10-10}@1.0 + {10-11}@0.8 | elongate(c:2.0) | twin(brazil)

# Dauphine twin quartz
trigonal[32]:{10-10}@1.0 + {10-11}@0.8 | twin(dauphine)

# Japan twin quartz (84.55° contact)
trigonal[32]:{10-10}@1.0 + {10-11}@0.8 | twin(japan)

# Carlsbad twin feldspar
monoclinic[2/m]:{010}@1.0 + {001}@0.8 + {110}@0.6 | twin(carlsbad)

# Cyclic triple twin
cubic[m3m]:{111} | twin(spinel,3)
```

### Complex Examples

```bash
# Heavily modified fluorite
cubic[m3m]:{100}@1.0 + {111}@0.5 + {110}@0.3 + {311}@0.1

# Tourmaline (trigonal prism with multiple terminations)
trigonal[3m]:{10-10}@1.0 + {11-20}@0.5 + {10-11}@0.7 + {02-21}@0.4 | elongate(c:3.0)

# Staurolite cross (penetration twin)
orthorhombic[mmm]:{110}@1.0 + {010}@0.8 | twin([0,0,1],90,penetration)
```

---

## Appendices

### Appendix A: Point Group Symmetry Operations

Each point group is defined by a set of symmetry operations (3×3 matrices).

#### m3m (Oh) - 48 operations

The full cubic group consists of:
- 24 proper rotations (identity, 6×90°, 3×180°, 8×120°, 6×180°)
- 24 improper rotations (inversion × each proper rotation)

**Proper rotations:**
```python
identity = [[1,0,0], [0,1,0], [0,0,1]]

# 90° rotations about cube face normals (6 total)
rot_90_x = [[1,0,0], [0,0,-1], [0,1,0]]
rot_90_y = [[0,0,1], [0,1,0], [-1,0,0]]
rot_90_z = [[0,-1,0], [1,0,0], [0,0,1]]
# ... and their inverses

# 180° rotations about cube face normals (3 total)
rot_180_x = [[1,0,0], [0,-1,0], [0,0,-1]]
rot_180_y = [[-1,0,0], [0,1,0], [0,0,-1]]
rot_180_z = [[-1,0,0], [0,-1,0], [0,0,1]]

# 120° rotations about body diagonals [111] (8 total)
rot_120_111 = [[0,0,1], [1,0,0], [0,1,0]]
# ... all permutations

# 180° rotations about edge centers [110] (6 total)
rot_180_110 = [[0,1,0], [1,0,0], [0,0,-1]]
# ... all permutations
```

**Improper rotations:**
Multiply each proper rotation by inversion:
```python
inversion = [[-1,0,0], [0,-1,0], [0,0,-1]]
```

### Appendix B: Miller Index to Face Normal

For a crystal with lattice parameters (a, b, c, α, β, γ):

**Orthogonal systems (cubic, tetragonal, orthorhombic):**
```python
# Direct calculation (α=β=γ=90°)
normal = [h/a, k/b, l/c]
normal = normal / |normal|  # Normalize
```

**Non-orthogonal systems:**
```python
# Use reciprocal lattice vectors
# a* = (b × c) / V, etc.
# normal = h*a* + k*b* + l*c*
```

### Appendix C: Form Generation Algorithm

```python
def generate_form(point_group: str, miller: tuple) -> list:
    """Generate all face normals for a form."""
    operations = get_symmetry_operations(point_group)
    base_normal = miller_to_normal(miller)

    normals = set()
    for op in operations:
        rotated = op @ base_normal
        # Round to avoid floating point issues
        rounded = tuple(round(x, 10) for x in rotated)
        normals.add(rounded)

    return list(normals)
```

### Appendix D: Form Combination Algorithm

```python
def combine_forms(forms: list) -> Geometry:
    """Combine multiple forms into a single crystal geometry.

    Uses half-space intersection: each face defines a half-space,
    the crystal is the intersection of all half-spaces.
    """
    half_spaces = []
    for form in forms:
        for normal in form.normals:
            # Half-space: n·x ≤ d (where d is scaled distance)
            half_spaces.append((normal, form.scale))

    # Compute vertex-representation of polytope
    vertices = compute_half_space_intersection(half_spaces)

    # Compute face-representation
    faces = identify_faces(vertices, half_spaces)

    return Geometry(vertices, faces)
```

---

## Changelog

### Version 1.0.0 (Draft)
- Initial specification
- 7 crystal systems
- 32 point groups
- Basic modifications (elongate, truncate, taper, bevel)
- 10 named twin laws
- Compact string notation

---

## References

1. International Tables for Crystallography, Volume A
2. Klein, C. & Hurlbut, C. S. (1993). Manual of Mineralogy
3. Bloss, F. D. (1971). Crystallography and Crystal Chemistry
4. Dana's New Mineralogy (8th edition)
