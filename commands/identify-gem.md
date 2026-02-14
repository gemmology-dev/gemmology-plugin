---
name: identify-gem
description: Interactive workflow to systematically identify an unknown coloured gemstone using standard gemmological testing sequence
allowed-tools:
  - Read
  - AskUserQuestion
argument-hint: "[optional: initial observations or suspected identity]"
---

# Gemstone Identification Workflow

Guide the user through systematic gemstone identification using the standard FGA testing sequence.

## Initial Assessment

First, gather basic observations from the user:

1. **Colour Description**
   - Primary hue (red, blue, green, yellow, etc.)
   - Tone (light, medium, dark)
   - Any secondary colours or modifiers

2. **Transparency**
   - Transparent, translucent, or opaque

3. **Cut Style**
   - Faceted, cabochon, or rough
   - If faceted: shape and approximate size

4. **Any Visible Features**
   - Visible inclusions
   - Colour zoning
   - Phenomena (star, cat's eye, colour change)

## Testing Sequence

Guide through tests in this order, asking for results at each step:

### Step 1: Visual Examination (10x Loupe)

Ask user to examine under magnification and describe:
- Lustre (vitreous, adamantine, waxy, etc.)
- Visible inclusions (needles, crystals, fingerprints)
- Surface features (polish, wear)
- Doubling of back facets (if visible)

Use observations to narrow possibilities.

### Step 2: Refractive Index

If user has a refractometer, guide them through:
1. Clean table facet
2. Apply contact liquid
3. Place on prism, read shadow edge(s)

**Interpret results**:
- Single reading = Isotropic (spinel, garnet)
- Two readings = Anisotropic (most gems)
- Calculate birefringence if two readings

Match RI to possible species using `optical-properties` skill data.

### Step 3: Polariscope

Guide user to test optical character:
1. Cross polarisers (dark field)
2. Place stone, rotate 360°
3. Observe light/dark pattern

**Interpret**:
- Stays dark = Singly refractive (cubic system or amorphous)
- 4 blinks = Doubly refractive
- Stays light = Aggregate or ADR

### Step 4: Dichroscope

If stone is coloured and doubly refractive:
1. View through dichroscope
2. Rotate stone 90°
3. Note colours in two windows

Strong pleochroism helps identify species (e.g., tanzanite, iolite).

### Step 5: Spectroscope (if available)

Ask user to observe absorption spectrum:
- Position of lines/bands
- Strength of absorption

Match to known spectra for suspected species.

### Step 6: UV Fluorescence (if available)

Test under long-wave and short-wave UV:
- Colour of fluorescence
- Intensity
- Any phosphorescence

Compare to expected reactions for suspected species.

### Step 7: Specific Gravity (if needed)

If identity still uncertain and user can test:
- Hydrostatic weighing method
- Heavy liquid method (if available)

## Building the Identification

After each test, update the list of possible identifications:

1. **Narrow by colour** - What gems come in this colour?
2. **Narrow by RI** - Which match the measured value?
3. **Narrow by optical character** - SR or DR?
4. **Narrow by pleochroism** - Expected for this species?
5. **Confirm with spectrum/UV** - Matches expected?
6. **Check for synthetic/simulant counterparts** - After narrowing candidates by RI and SG, query `get_counterparts()` from mineral_database to list which synthetics and simulants share those values. This helps identify look-alikes.

### Could This Be Synthetic?

Once a species match is established, consider whether the stone could be synthetic:

1. **Examine inclusions** - Check for diagnostic synthetic features (curved striae, gas bubbles, flux veils, chevron growth, seed plates). The `diagnostic_synthetic_features` field in the mineral database lists known indicators for each synthetic type.
2. **Growth pattern analysis** - Straight/angular = natural; curved = flame fusion; chevron = hydrothermal.
3. **Cleanliness** - Suspiciously clean stones of a species that is typically included (e.g., emerald) warrant further investigation.
4. **UV fluorescence** - Synthetics may fluoresce more strongly or differently than natural counterparts.
5. **Query the database** - Use `get_counterparts("<species>")` to see all known synthetic and simulant matches, including their growth methods and diagnostic features.

## Common Separation Problems

Help user distinguish between commonly confused pairs:

**Ruby vs Red Spinel**
- RI: Ruby 1.76-1.77, Spinel 1.71-1.74
- Polariscope: Ruby DR, Spinel SR
- Dichroscope: Ruby dichroic, Spinel not
- Spectrum: Different chromium patterns

**Blue Sapphire vs Blue Spinel**
- Similar to above but blue colours

**Natural vs Synthetic**
- Examine inclusions carefully
- Curved striae = flame fusion synthetic
- Too clean = suspect synthetic

## Output Format

Provide identification report:

```markdown
# Gemstone Identification Report

## Observations
- **Colour**: [description]
- **Transparency**: [transparent/translucent/opaque]
- **Cut**: [style and shape]

## Test Results
| Test | Result | Interpretation |
|------|--------|----------------|
| RI | [value] | Consistent with [species] |
| Polariscope | [SR/DR] | [species group] |
| Dichroscope | [colours] | [interpretation] |
| Spectrum | [features] | [interpretation] |
| UV | [reaction] | [interpretation] |

## Identification
**Species**: [identified species]
**Variety**: [if applicable]
**Confidence**: [high/medium/low]

## Notes
- [Any observations about origin, treatment, quality]
- [Recommendations for further testing if needed]
```

## Tips

- If tests conflict, question the readings or stone identity
- Some stones require advanced testing (LA-ICP-MS for Be diffusion)
- When in doubt, recommend laboratory certification
- Note any treatment indicators observed

## Reference Skills

Load these skills for detailed property data:
- `optical-properties` - RI and birefringence tables
- `physical-properties` - SG values
- `inclusions-fingerprints` - Inclusion identification
- `synthetics-simulants` - Synthetic detection
