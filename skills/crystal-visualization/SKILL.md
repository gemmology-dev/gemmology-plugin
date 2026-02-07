---
name: crystal-visualization
description: >-
  Use this skill when the user asks to "generate crystal SVG", "draw crystal
  structure", "visualize crystal system", "show unit cell", "show crystal
  structure of [gemstone]", "illustrate [gemstone] atomic structure", "show
  crystal habit", "draw octahedron", "show twinning", "display cleavage planes",
  "what does this crystal look like", "show me a [mineral] crystal", "export
  crystal for 3D printing", "create STL file", "generate GEMCAD file", or needs
  visual representations of crystalline structures. Supports presets for 46
  minerals, Crystal Description Language (CDL) for custom morphologies, and
  export to SVG, STL, glTF, and GEMCAD formats.
---

# Crystal Structure Visualization

Generate SVG images of crystal structures, habits, twins, and cleavage planes using the ASE + matplotlib Python script.

## Prerequisites

The script requires these Python packages:
- `ase` (Atomic Simulation Environment) - for atomic structures
- `matplotlib` - for rendering
- `numpy` - for numerical operations

Check if installed:
```bash
python3 -c "import ase, matplotlib, numpy" 2>/dev/null && echo "Ready" || echo "Install needed"
```

Install if needed:
```bash
pip install ase matplotlib numpy
```

### Optional: Native C++ Acceleration

For faster geometry computation (halfspace intersection, bond detection), a native C++ module can be built:

```bash
cd ${CLAUDE_PLUGIN_ROOT}/scripts/native
mkdir -p build && cd build
cmake .. -DPython3_EXECUTABLE=$(which python3)
make -j4
make install
```

Requires: CMake 3.15+, C++17 compiler. The module uses pybind11 + Eigen for performance-critical operations.

## Quick Start: Presets (Recommended)

The fastest way to generate crystal visualizations is using presets. 46 minerals are available with typical crystal habits.

**Always use `--no-grid` for cleaner SVG output** (removes background grid and axis outlines).

### List Available Presets
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --list-presets
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --list-presets cubic  # Filter by system
```

### Generate from Preset
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset diamond --no-grid -o /tmp/diamond.svg
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset garnet --no-grid -o /tmp/garnet.svg
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset quartz --no-grid -o /tmp/quartz.svg
```

### Get Preset Info as JSON
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset diamond --json
```

### Suggest CDL for a Mineral
When a user asks about a specific mineral, suggest CDL notation:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --suggest garnet
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --suggest ruby --json
```

## Crystal Description Language (CDL)

CDL provides precise control over crystal morphology using Miller indices and point group symmetry.

### CDL Syntax
```
system[point_group]:{hkl}@scale + {hkl}@scale | modifications | twin(law)
```

### CDL Examples
```bash
# Pure octahedron
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}" --no-grid -o /tmp/octahedron.svg

# Truncated octahedron (octahedron + cube)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}@1.0 + {100}@1.3" --no-grid -o /tmp/truncated.svg

# Garnet habit (dodecahedron + trapezohedron)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{110}@1.0 + {211}@0.6" --no-grid -o /tmp/garnet.svg

# Color faces by form (educational)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}@1.0 + {100}@1.3" --color-by-form --no-grid -o /tmp/colored.svg
```

### Explain CDL Notation
Help users understand what a CDL string means:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --explain "cubic[m3m]:{111}@1.0 + {100}@1.3"
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --explain "cubic[m3m]:{111}" --json
```

### Geometry Statistics
Get vertex/edge/face counts:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}" --geometry-stats
```

## Export Formats

### SVG (Default)
Best for documentation and web display.
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset diamond --no-grid -o /tmp/diamond.svg
```

### STL (3D Printing)
Binary STL format for 3D printing:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}" --format stl -o /tmp/crystal.stl
```

### glTF (Web/AR/VR)
glTF 2.0 format for Three.js, AR/VR applications:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}" --format gltf -o /tmp/crystal.gltf
```

### GEMCAD (Gem Cutting)
ASCII format for GemCad, Gem Cut Studio, and other faceting software:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}" --format gemcad -o /tmp/crystal.asc
```

### JSON (Data)
Structured data for programmatic use:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}" --format json
```

## Usage

### Basic Gemstone Visualization

Generate a crystal structure SVG for a specific gemstone:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py <gemstone> -o /tmp/crystal.svg
```

Examples:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py diamond -o /tmp/diamond.svg
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py ruby -o /tmp/ruby.svg
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py emerald -o /tmp/emerald.svg
```

### Crystal System Visualization

Generate a generic unit cell for any of the 7 crystal systems:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py cubic -o /tmp/cubic.svg
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py hexagonal -o /tmp/hexagonal.svg
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py monoclinic -o /tmp/monoclinic.svg
```

### Crystal Habits (External Morphology)

Show the external crystal form rather than atomic structure:

```bash
# Gemstone default habit
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py diamond --view habit -o /tmp/diamond_habit.svg

# Specific habit type
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --habit octahedron -o /tmp/octahedron.svg
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py quartz --view habit -o /tmp/quartz_prism.svg
```

Available habits: octahedron, cube, dodecahedron, hexagonal_prism, hexagonal_bipyramid, tetragonal_prism, tetragonal_bipyramid, orthorhombic_prism, barrel, tabular, trapezohedron, rhombic_dodecahedron

### Twin Configurations

Display common crystal twinning patterns:

```bash
# Spinel law twin (octahedra sharing {111} plane)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py spinel --twin spinel_law -o /tmp/spinel_twin.svg

# Fluorite penetration twin
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py fluorite --twin fluorite -o /tmp/fluorite_twin.svg

# Auto-detect twin for gemstone
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py diamond --twin -o /tmp/diamond_twin.svg
```

Available twin laws: spinel_law, iron_cross, carlsbad, albite, brazil, dauphine, japan, trilling, fluorite, staurolite_60, staurolite_90

### Cleavage Planes

Visualize cleavage planes overlaid on crystal habit:

```bash
# Diamond octahedral cleavage
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py diamond --cleavage -o /tmp/diamond_cleavage.svg

# Topaz basal cleavage
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py topaz --cleavage basal_001 -o /tmp/topaz_cleavage.svg

# Specific cleavage type
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cleavage octahedral_111 -o /tmp/cleavage.svg
```

Available cleavage types: cubic_100, octahedral_111, rhombohedral, basal_001, prismatic_110, pinacoidal

### Atomic Bonds

Show bonds between atoms in structure view:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py diamond --bonds -o /tmp/diamond_bonds.svg

# Custom bond cutoff distance
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py quartz --bonds --bond-cutoff 2.0 -o /tmp/quartz_bonds.svg
```

### Supercell View

Generate a 2x2x2 supercell for better visualization:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py diamond --type supercell -o /tmp/diamond_supercell.svg
```

### Custom View Angles

Adjust the viewing angle:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py ruby --elev 45 --azim -60 -o /tmp/ruby.svg
```

### Hide Axes

Generate without crystallographic axis arrows:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py quartz --no-axes -o /tmp/quartz.svg
```

### Hide Grid

Generate without background grid and panes for cleaner images:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}" --no-grid -o /tmp/clean.svg
```

### Face Labels

Show Miller indices on visible crystal faces (educational):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}@1.0 + {100}@1.3" --face-labels --no-grid -o /tmp/labeled.svg
```

### Full Information Display

Combine all options for maximum detail:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset garnet --color-by-form --face-labels --no-grid -o /tmp/garnet_full.svg
```

### Info Panels

Add gemstone property panels to SVG output:

```bash
# Basic info (name, formula, system, hardness)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset diamond --info --no-grid -o /tmp/diamond_info.svg

# Full gemological info
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset ruby --info-full --no-grid -o /tmp/ruby_info.svg

# FGA exam-relevant properties
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset emerald --info-fga --no-grid -o /tmp/emerald_fga.svg

# Custom property selection
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset sapphire --info-props name,ri,sg,hardness --no-grid -o /tmp/sapphire.svg
```

**User-provided data** (works with CDL or presets):
```bash
# CDL with custom info
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "cubic[m3m]:{111}" \
    --info-data name="Unknown Spinel" \
    --info-data ri=1.718 \
    --info --no-grid -o /tmp/custom.svg

# Override preset values
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset ruby \
    --info-data localities="Mogok, Myanmar" \
    --info --no-grid -o /tmp/burma_ruby.svg

# Load from JSON file
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --cdl "hexagonal[6/mmm]:{10-10}" \
    --info-json /path/to/gem_data.json \
    --info --no-grid -o /tmp/from_json.svg
```

**Panel customization:**
```bash
# Position: top-left, top-right (default), bottom-left, bottom-right
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset garnet --info --info-position bottom-left --no-grid -o /tmp/garnet.svg

# Style: compact (default), detailed, minimal
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset topaz --info-full --info-style detailed --no-grid -o /tmp/topaz.svg

# Font size
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --preset diamond --info --info-fontsize 12 --no-grid -o /tmp/diamond.svg
```

**Available property keys** for `--info-props` or `--info-data`:
- Identification: `name`, `chemistry`, `system`, `hardness`
- Physical: `sg`, `cleavage`, `fracture`, `lustre`
- Optical: `ri`, `birefringence`, `optical_character`, `dispersion`, `pleochroism`
- Gemological: `colors`, `treatments`, `localities`, `inclusions`
- Crystal: `point_group`, `forms`, `description`

### List Available Options

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crystal_svg.py --list
```

## Available Gemstones

| Gemstone | Crystal System | Structure |
|----------|---------------|-----------|
| diamond | Cubic | Diamond structure (C) |
| spinel | Cubic | Spinel structure (MgAl2O4) |
| garnet | Cubic | Garnet structure |
| fluorite | Cubic | Fluorite (CaF2) |
| lazurite | Cubic | Sodalite group (lapis lazuli) |
| ruby | Trigonal | Corundum (Al2O3) |
| sapphire | Trigonal | Corundum (Al2O3) |
| corundum | Trigonal | Corundum (Al2O3) |
| quartz | Trigonal | Quartz (SiO2) |
| tourmaline | Trigonal | Tourmaline (borosilicate) |
| emerald | Hexagonal | Beryl (Be3Al2Si6O18) |
| aquamarine | Hexagonal | Beryl (Be3Al2Si6O18) |
| beryl | Hexagonal | Beryl (Be3Al2Si6O18) |
| apatite | Hexagonal | Apatite (Ca5(PO4)3F) |
| topaz | Orthorhombic | Topaz (Al2SiO4(F,OH)2) |
| peridot | Orthorhombic | Olivine (Mg2SiO4) |
| chrysoberyl | Orthorhombic | Chrysoberyl (BeAl2O4) |
| tanzanite | Orthorhombic | Zoisite |
| zircon | Tetragonal | Zircon (ZrSiO4) |
| kunzite | Monoclinic | Spodumene (LiAlSi2O6) |
| spodumene | Monoclinic | Spodumene (LiAlSi2O6) |
| malachite | Monoclinic | Malachite (Cu2CO3(OH)2) |
| turquoise | Triclinic | Turquoise |
| rhodonite | Triclinic | Rhodonite (MnSiO3) |

## Available Crystal Systems

- **cubic** - a=b=c, a=b=g=90deg
- **tetragonal** - a=b!=c, a=b=g=90deg
- **orthorhombic** - a!=b!=c, a=b=g=90deg
- **hexagonal** - a=b!=c, a=b=90deg, g=120deg
- **trigonal** - a=b=c, a=b=g!=90deg
- **monoclinic** - a!=b!=c, a=g=90deg, b!=90deg
- **triclinic** - a!=b!=c, a!=b!=g!=90deg

## Output

The script generates SVG files that:
- Show atoms as coloured spheres (element-specific colours)
- Display the unit cell as a wireframe box
- Include crystallographic axes (a, b, c) with colour coding:
  - a-axis: Red
  - b-axis: Green
  - c-axis: Blue
- Use orthographic projection for accurate geometry
- Include title and legend

## Workflow

1. Determine the visualization type from user request:
   - Atomic structure (default)
   - Crystal habit (--view habit)
   - Twin configuration (--twin)
   - Cleavage planes (--cleavage)
2. Run the script with appropriate arguments
3. Read the generated SVG file
4. Either:
   - Embed the SVG in the response (for viewing)
   - Save to a user-specified location
   - Both

## Troubleshooting

If the script fails:
1. Check Python version: `python3 --version` (requires 3.8+)
2. Verify ASE installed: `python3 -c "import ase; print(ase.__version__)"`
3. Check matplotlib backend: the script uses 'Agg' (non-interactive)

For missing structures, the script will list available options with `--list`.
