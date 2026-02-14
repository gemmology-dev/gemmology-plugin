---
name: crystal-svg
description: Generate SVG visualization of a gemstone's crystal structure, habit, twinning, cleavage, or custom CDL morphology
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
argument-hint: "<gemstone|--preset NAME|--cdl 'CDL'> [--format svg|stl|gltf] [--info-fga] [--no-grid] [-o path]"
---

# Crystal Structure SVG Generator

Generate scientifically accurate SVG visualizations of gemstone crystal structures, habits, twins, and cleavage planes.

## Parse Arguments

Arguments format: `<target> [options]`

**Target:**
- Gemstone name (e.g., "diamond", "ruby", "tourmaline")
- `--preset NAME` for mineral presets
- `--cdl "CDL_STRING"` for custom Crystal Description Language

**Options:**
- `-o`, `--output`: Output file path (default: stdout)
- `--format {svg,stl,gltf}`: Output format (default: svg)
- `--width`: Width in pixels (default: 600)
- `--height`: Height in pixels (default: 600)
- `--elev ANGLE`: Elevation angle (default: 30)
- `--azim ANGLE`: Azimuth angle (default: -45)
- `--no-axes`: Hide crystallographic axes
- `--no-grid`: Hide background grid
- `--info-fga`: Show FGA exam-relevant properties panel
- `--twin LAW`: Apply twin law (spinel, japan, brazil, etc.)

## Execution

Use the gemmology CLI:

```bash
gemmology crystal-svg <arguments>
# Or use the dedicated command:
crystal-svg <arguments>
```

### Examples

**Using presets (easiest):**
```bash
# Generate diamond crystal
gemmology crystal-svg --preset diamond -o ~/Desktop/diamond.svg

# Ruby with FGA info panel
gemmology crystal-svg --preset ruby --info-fga --no-grid -o ~/Desktop/ruby.svg

# List available presets
gemmology list-presets
```

**Using CDL notation (advanced):**
```bash
# Truncated octahedron
gemmology crystal-svg --cdl "cubic[m3m]:{111}@1.0 + {100}@1.3" -o /tmp/truncated.svg

# Garnet with dodecahedron and trapezohedron
gemmology crystal-svg --cdl "cubic[m3m]:{110}@1.0 + {211}@0.6" -o /tmp/garnet.svg

# Quartz prism with pyramidal termination
gemmology crystal-svg --cdl "trigonal[-3m]:{10-10}@1.0 + {10-11}@0.8" -o /tmp/quartz.svg
```

**Twin crystals:**
```bash
# Japan twin quartz
gemmology crystal-svg --twin japan -o /tmp/japan_twin.svg

# Spinel law twin
gemmology crystal-svg --twin spinel -o /tmp/spinel_twin.svg
```

**Export for 3D printing:**
```bash
# STL format
gemmology crystal-svg --preset diamond --format stl -o /tmp/diamond.stl

# glTF format (web/AR)
gemmology crystal-svg --preset emerald --format gltf -o /tmp/emerald.gltf
```

**Get preset information:**
```bash
gemmology info diamond
```

## CDL Syntax Quick Reference

```
system[point_group]:{hkl}@distance + {hkl}@distance
```

- **System**: cubic, hexagonal, trigonal, tetragonal, orthorhombic, monoclinic, triclinic
- **Point group**: m3m, 6/mmm, -3m, 4/mmm, mmm, 2/m, -1 (etc.)
- **{hkl}**: Miller indices for crystal form
- **@distance**: Relative distance from center (controls truncation)

### Common Forms

| Form | Miller Indices |
|------|---------------|
| Cube | {100} |
| Octahedron | {111} |
| Dodecahedron | {110} |
| Trapezohedron | {211} |
| Prism | {10-10} |
| Pinacoid | {0001} |

## Available Presets

- **Cubic**: diamond, spinel, garnet, fluorite, pyrite
- **Trigonal**: ruby, sapphire, quartz, tourmaline, calcite
- **Hexagonal**: emerald, aquamarine, beryl, apatite
- **Orthorhombic**: topaz, peridot, chrysoberyl, tanzanite
- **Tetragonal**: zircon, rutile
- **Monoclinic**: kunzite, malachite, jadeite

### Synthetic and Simulant Presets

Synthetic and simulant presets are also available:

```bash
# Synthetic presets
gemmology crystal-svg --preset synthetic-ruby-verneuil -o /tmp/synth-ruby.svg
gemmology crystal-svg --preset synthetic-emerald-flux -o /tmp/synth-emerald.svg

# Simulant presets
gemmology crystal-svg --preset cubic-zirconia -o /tmp/cz.svg
gemmology crystal-svg --preset moissanite -o /tmp/moissanite.svg

# List all synthetics or simulants
gemmology list-presets --origin synthetic
gemmology list-presets --origin simulant
```

**Note:** Some synthetic presets (e.g., flame fusion boules) have no CDL expression because the growth form is not a natural crystal habit. In this case, the tool will display an informational message instead of generating a visualization. Use `gemmology info <preset>` to view the preset's properties.

When `--info-fga` is used with a synthetic or simulant preset, the info panel will include the origin (synthetic/simulant) and growth method (e.g., Verneuil, flux, hydrothermal) alongside the standard gemmological properties.

## Available Twin Laws

spinel, japan, brazil, dauphine, carlsbad, baveno, manebach, albite, trilling, fluorite, iron_cross, staurolite_60, staurolite_90

## Output Handling

After generation:
1. Confirm the file was created successfully
2. If no output path specified, display SVG content
3. For macOS, offer to open: `open /path/to/output.svg`
