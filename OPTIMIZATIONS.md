# Gemmology-Plugin Optimizations & Improvements

**Status**: Pending Implementation
**Priority**: Medium (production-ready, feature gaps to fill)
**Date**: January 2026

---

## Overview

The gemmology-plugin is a **well-engineered orchestration layer** (8/10 quality) that successfully integrates cdl-parser, crystal-geometry, mineral-database, and crystal-renderer. It provides both CLI tools and Python API. Key areas for improvement are missing agents/skills, documentation, and feature completeness.

---

## Critical Issues

### None

The plugin is production-ready with no blocking issues.

---

## High-Priority Improvements

### 1. Missing Agents (Architectural Gap)

**Issue**: README mentions agents but none are defined.

**Expected Agents**:

| Agent | Purpose | Tools |
|-------|---------|-------|
| `crystallography-expert` | Crystal systems, symmetry, Miller indices | Read, Grep, WebFetch |
| `gemmology-expert` | Gemstone properties, FGA data | Read, mineral-database |
| `cdl-expert` | CDL syntax help, interactive construction | Read, cdl-parser |

**Proposed Structure**:
```
agents/
├── crystallography-expert.md
├── gemmology-expert.md
└── cdl-expert.md
```

**Example Agent Definition** (`agents/crystallography-expert.md`):
```yaml
---
name: crystallography-expert
description: Expert on crystal systems, symmetry operations, and Miller indices
tools:
  - Read
  - Grep
  - WebFetch
trigger:
  keywords:
    - crystal system
    - point group
    - Miller index
    - symmetry
    - unit cell
---

You are an expert crystallographer with deep knowledge of:
- The 7 crystal systems and their lattice parameters
- 32 crystallographic point groups
- Miller index notation (3-index and 4-index Miller-Bravais)
- Symmetry operations and their combinations

When answering questions:
1. Reference the crystal-geometry package for calculations
2. Explain concepts clearly with examples
3. Provide CDL notation when relevant
```

---

### 2. Empty Skills Directory

**Issue**: Skills referenced in commands but not defined in package.

**Expected Skills** (from `/identify-gem` command):
- `optical-properties` - RI, birefringence, dispersion
- `physical-properties` - Hardness, SG, cleavage
- `inclusions-fingerprints` - Diagnostic inclusions
- `synthetics-simulants` - Detection methods

**Proposed Structure**:
```
skills/
├── optical-properties.md
├── physical-properties.md
├── inclusions-fingerprints.md
├── synthetics-simulants.md
├── treatments-enhancements.md
└── origin-determination.md
```

**Example Skill Definition** (`skills/optical-properties.md`):
```yaml
---
name: optical-properties
description: Quick reference for gemstone optical properties
invocable: true
---

# Optical Properties Reference

## Refractive Index (RI)
- **Definition**: Ratio of speed of light in air to speed in material
- **Measurement**: Refractometer with contact liquid (RI 1.81)
- **Key Values**:
  - Diamond: 2.417 (beyond refractometer)
  - Corundum: 1.762-1.770
  - Beryl: 1.577-1.583
  - Quartz: 1.544-1.553

## Birefringence (DR)
- **Definition**: Difference between max and min RI
- **Strong**: Zircon (0.059), Calcite (0.172)
- **Moderate**: Tourmaline (0.018-0.020)
- **Weak**: Topaz (0.008-0.010)
```

---

### 3. No Hooks Implementation

**Issue**: No hooks for tool interception or automation.

**Proposed Hooks**:

| Hook | Event | Purpose |
|------|-------|---------|
| `validate-cdl` | PreToolUse(Bash) | Validate CDL syntax before execution |
| `cache-svg` | PostToolUse(Write) | Cache generated SVGs |
| `error-recovery` | Stop | Handle geometry computation failures |

**Example Hook** (`hooks/validate-cdl.md`):
```yaml
---
name: validate-cdl
event: PreToolUse
tools:
  - Bash
match:
  command: "gemmology crystal-svg"
---

Before running the crystal-svg command, validate the CDL syntax:

1. Extract the CDL string from the command
2. Run `gemmology validate <cdl>` to check syntax
3. If invalid, block execution and explain the error
4. Suggest corrections based on common mistakes
```

---

### 4. Documentation Gap

**Issue**: Empty `docs/` directory, README is minimal.

**Proposed Documentation**:
```
docs/
├── getting-started.md       # Installation and first steps
├── cdl-reference.md         # Complete CDL syntax guide
├── api-reference.md         # Python API documentation
├── cli-reference.md         # Command-line usage
├── presets.md               # Mineral preset catalog
├── troubleshooting.md       # Common issues and solutions
└── fga-curriculum.md        # Gemstone identification guide
```

**Example: CDL Reference** (`docs/cdl-reference.md`):
```markdown
# Crystal Description Language Reference

## Basic Syntax
```
system[point_group]:{form}@scale + {form}@scale | modification
```

## Crystal Systems
| System | Example Point Groups | Lattice |
|--------|---------------------|---------|
| cubic | m3m, -43m, 432 | a=b=c, α=β=γ=90° |
| hexagonal | 6/mmm, 6mm | a=b≠c, α=β=90°, γ=120° |
...

## Named Forms
| Name | Miller Indices | System | Faces |
|------|---------------|--------|-------|
| octahedron | {111} | cubic | 8 |
| cube | {100} | cubic | 6 |
...
```

---

## Medium-Priority Improvements

### 5. CLI Integration Tests

**Issue**: Only unit tests for argument parser, no actual CLI execution tests.

**Proposed Tests**:
```python
# tests/test_cli_integration.py
import subprocess
import tempfile
from pathlib import Path

class TestCLIIntegration:
    def test_crystal_svg_preset(self):
        """Test crystal-svg with preset."""
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as f:
            result = subprocess.run(
                ['gemmology', 'crystal-svg', '--preset', 'diamond', '-o', f.name],
                capture_output=True, text=True
            )
            assert result.returncode == 0
            assert Path(f.name).stat().st_size > 0
            Path(f.name).unlink()

    def test_crystal_svg_cdl(self):
        """Test crystal-svg with CDL string."""
        result = subprocess.run(
            ['gemmology', 'crystal-svg', '--cdl', 'cubic[m3m]:{111}'],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert '<svg' in result.stdout

    def test_list_presets(self):
        """Test list-presets command."""
        result = subprocess.run(
            ['gemmology', 'list-presets'],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert 'diamond' in result.stdout.lower()

    def test_info_command(self):
        """Test info command."""
        result = subprocess.run(
            ['gemmology', 'info', 'diamond'],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert 'Diamond' in result.stdout
        assert 'C' in result.stdout  # Chemistry

    def test_invalid_preset(self):
        """Test error handling for invalid preset."""
        result = subprocess.run(
            ['gemmology', 'crystal-svg', '--preset', 'nonexistent'],
            capture_output=True, text=True
        )
        assert result.returncode != 0
        assert 'error' in result.stderr.lower() or 'not found' in result.stderr.lower()
```

---

### 6. Remove Temporary File Usage

**Issue**: Convenience functions create temp files unnecessarily.

**Current** (`__init__.py`):
```python
def generate_crystal_svg(cdl: str, ...) -> str:
    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as f:
        output_path = Path(f.name)
    generate_cdl_svg(cdl, output_path, ...)
    svg_content = output_path.read_text()
    output_path.unlink()  # Clean up
    return svg_content
```

**Proposed Fix**:
```python
import io

def generate_crystal_svg(cdl: str, ...) -> str:
    """Generate SVG without temp files."""
    # If crystal-renderer supports StringIO output:
    buffer = io.StringIO()
    generate_cdl_svg(cdl, buffer, ...)
    return buffer.getvalue()

    # Or use in-memory matplotlib figure:
    fig = create_crystal_figure(cdl, ...)
    buffer = io.BytesIO()
    fig.savefig(buffer, format='svg')
    return buffer.getvalue().decode('utf-8')
```

---

### 7. Add Preset Caching

**Issue**: Presets fetched from database on every call.

**Proposed Fix**:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_preset_cached(name: str) -> dict | None:
    """Get preset with caching."""
    return get_preset(name)

def generate_preset_svg(preset_name: str, ...) -> str:
    preset = get_preset_cached(preset_name)
    if preset is None:
        raise ValueError(f"Unknown preset: {preset_name}")
    # ...
```

---

### 8. CLI Argument Validation

**Issue**: No validation of angle ranges, format combinations.

**Proposed Fix**:
```python
def _validate_args(args) -> list[str]:
    """Validate CLI arguments, return list of warnings."""
    warnings = []

    if args.elev is not None:
        if not -90 <= args.elev <= 90:
            warnings.append(f"Elevation {args.elev}° outside recommended range [-90, 90]")

    if args.azim is not None:
        if not -180 <= args.azim <= 180:
            warnings.append(f"Azimuth {args.azim}° outside recommended range [-180, 180]")

    if args.format == 'stl' and args.info_fga:
        warnings.append("--info-fga ignored for STL format (3D only)")

    return warnings

def _handle_svg_command(args):
    warnings = _validate_args(args)
    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    # Continue with execution...
```

---

### 9. Twin Law Integration

**Issue**: Twin law CLI integration unclear, may fail silently.

**Current** (`cli.py`):
```python
if args.twin:
    cdl = f"cubic[m3m]:octahedron|twin({args.twin})"
```

**Issues**:
- Hardcodes cubic system
- Hardcodes octahedron form
- No validation of twin law name

**Proposed Fix**:
```python
def _build_twin_cdl(twin_law: str, base_preset: str = 'diamond') -> str:
    """Build CDL for twinned crystal with validation."""
    from cdl_parser import TWIN_LAWS

    if twin_law not in TWIN_LAWS:
        valid = ', '.join(sorted(TWIN_LAWS.keys()))
        raise ValueError(f"Unknown twin law: {twin_law}. Valid: {valid}")

    preset = get_preset(base_preset)
    if preset is None:
        raise ValueError(f"Unknown base preset: {base_preset}")

    base_cdl = preset['cdl']
    return f"{base_cdl}|twin({twin_law})"
```

---

## Low-Priority Improvements

### 10. Performance Benchmarks

**Issue**: No performance metrics or benchmarks.

**Proposed Test**:
```python
# tests/test_performance.py
import time
import pytest

class TestPerformance:
    @pytest.mark.benchmark
    def test_simple_svg_generation(self):
        """Benchmark simple SVG generation."""
        start = time.perf_counter()
        for _ in range(10):
            generate_crystal_svg("cubic[m3m]:{111}")
        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / 10) * 1000
        assert avg_ms < 500, f"Too slow: {avg_ms:.1f}ms average"

    @pytest.mark.benchmark
    def test_complex_svg_generation(self):
        """Benchmark complex crystal."""
        cdl = "cubic[m3m]:{111}@1.0 + {100}@1.3 + {110}@1.5"
        start = time.perf_counter()
        generate_crystal_svg(cdl)
        elapsed = (time.perf_counter() - start) * 1000
        assert elapsed < 2000, f"Too slow: {elapsed:.1f}ms"
```

---

### 11. Plugin Manifest Enhancement

**Issue**: `plugin.json` is minimal.

**Proposed Enhancement**:
```json
{
  "name": "gemmology",
  "version": "1.0.0",
  "description": "Crystal visualization and gemstone expertise plugin",
  "author": "Bissbert",
  "commands": {
    "crystal-svg": {
      "description": "Generate SVG/STL/glTF crystal visualizations",
      "usage": "gemmology crystal-svg --preset diamond"
    },
    "identify-gem": {
      "description": "Interactive gemstone identification workflow",
      "usage": "/identify-gem"
    }
  },
  "agents": [
    "crystallography-expert",
    "gemmology-expert",
    "cdl-expert"
  ],
  "skills": [
    "optical-properties",
    "physical-properties",
    "inclusions-fingerprints"
  ],
  "settings": {
    "defaultFormat": "svg",
    "defaultElevation": 30,
    "defaultAzimuth": -45,
    "showAxesByDefault": true
  }
}
```

---

### 12. Known Geometry Issue

**Issue**: `orpiment` preset fails geometry generation.

**Location**: Tracked in `test_end_to_end_verification.py`:
```python
KNOWN_ISSUES = {'orpiment'}  # Complex monoclinic, fails halfspace intersection
```

**Root Cause**: Likely in `crystal-geometry` package - complex monoclinic form.

**Action**: Document in crystal-geometry OPTIMIZATIONS.md, investigate fix.

---

## CDL v2 Preparation

### 13. Support for New CDL Syntax

**For CDL v2 Features** (from `CDL-V2-SPECIFICATION.md`):

| Feature | Plugin Changes Needed |
|---------|----------------------|
| Block composition `()` | Update CLI to handle multi-line input |
| Named references `@name` | Add reference resolution in pipeline |
| Features `[phantom:N]` | Pass features to renderer |
| Growth operator `>` | Support in geometry generation |
| Aggregate operator `~` | Multi-geometry rendering |
| Comments `//` | Strip before parsing |

**Proposed CLI Enhancement**:
```python
# Support multi-line CDL from file
parser.add_argument(
    '--cdl-file', '-f',
    type=Path,
    help='Read CDL from file (supports multi-line v2 syntax)'
)

def _load_cdl(args) -> str:
    if args.cdl_file:
        return args.cdl_file.read_text()
    elif args.cdl:
        return args.cdl
    elif args.preset:
        return get_preset(args.preset)['cdl']
```

---

## Implementation Priority

| Priority | Task | Effort | Impact |
|----------|------|--------|--------|
| P1 | Create agent definitions | 4 hours | Feature completeness |
| P1 | Create skill definitions | 4 hours | FGA curriculum |
| P1 | Add documentation | 1 day | User adoption |
| P2 | CLI integration tests | 4 hours | Test coverage |
| P2 | Remove temp file usage | 2 hours | Performance |
| P2 | Add preset caching | 1 hour | Performance |
| P2 | CLI argument validation | 2 hours | Error handling |
| P3 | Fix twin law integration | 2 hours | Feature fix |
| P3 | Performance benchmarks | 2 hours | Quality assurance |
| P3 | Plugin manifest enhancement | 1 hour | Discoverability |

---

## Verification Checklist

After implementing improvements:

- [ ] All existing tests pass (50+ tests)
- [ ] Agents defined and documented
- [ ] Skills defined for FGA curriculum
- [ ] Documentation covers all features
- [ ] CLI integration tests pass
- [ ] No temp file creation in convenience functions
- [ ] Preset caching implemented
- [ ] CLI validates all arguments
- [ ] Twin law CLI works correctly
- [ ] Plugin manifest complete

---

## Package Integration Summary

| Package | Integration Status | Notes |
|---------|-------------------|-------|
| cdl-parser | ✅ Complete | All exports re-exported |
| crystal-geometry | ✅ Complete | Geometry generation working |
| mineral-database | ✅ Complete | Presets accessible |
| crystal-renderer | ✅ Complete | SVG/STL/glTF working |
| cdl-lsp | ⚠️ Optional | Listed but not integrated |

---

*Document created: 2026-01-20*
