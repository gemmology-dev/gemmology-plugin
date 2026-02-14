---
name: synthetics-simulants
description: >-
  Use this skill when the user asks about "synthetic gemstones", "lab-grown gems",
  "flame fusion", "hydrothermal", "flux grown", "Verneuil process", "simulants",
  "imitations", "fake gems", "how to detect synthetics", or needs to identify
  synthetic or imitation gemstones.
---

# Synthetics and Simulants

Guidance on identifying synthetic (laboratory-grown) gemstones and simulants (imitations). Understanding growth methods is key to detection.

## Database Integration

The mineral database contains preset entries for synthetics and simulants with structured data. Use the CLI or Python API to query them:

```bash
# List all synthetics and simulants
mineral-db --origin synthetic
mineral-db --origin simulant

# Show counterparts for a natural gem (all known synthetics/simulants)
mineral-db --counterparts ruby
mineral-db --counterparts diamond

# Get detailed info on a specific synthetic/simulant preset
mineral-db --info synthetic-ruby-verneuil
mineral-db --info cubic-zirconia
mineral-db --info luag
mineral-db --info synthetic-paraiba
```

Python API:
```python
from mineral_database import list_synthetics, list_simulants, get_counterparts, list_by_origin

# Query functions
list_synthetics()                # All synthetic preset IDs
list_simulants()                 # All simulant preset IDs
get_counterparts("ruby")         # Synthetics + simulants for ruby
list_by_origin("synthetic")      # All presets with origin=synthetic
```

## Terminology

| Term | Definition | Example |
|------|------------|---------|
| **Synthetic** | Same chemical/physical properties as natural | Synthetic ruby (Al₂O₃) |
| **Simulant** | Looks similar but different material | Glass imitating ruby |
| **Imitation** | Any material imitating another | YAG imitating any gem |
| **Lab-grown** | Same as synthetic (trade term) | Lab-grown emerald |
| **Created** | Same as synthetic (trade term) | Created sapphire |

## Synthetic Growth Methods

### Flame Fusion (Verneuil Process)

**Invented**: 1902 by Auguste Verneuil

**Process**:
1. Powder dropped through oxyhydrogen flame
2. Melts and crystallises on seed boule
3. Creates pear-shaped "boule"

**Materials produced**:
- Synthetic ruby (preset: `synthetic-ruby-verneuil`)
- Synthetic sapphire (all colours, preset: `synthetic-sapphire-verneuil`)
- Synthetic spinel (preset: `synthetic-spinel-verneuil`)
- Synthetic rutile
- Star ruby/sapphire (with additives)

**Detection features**:

| Feature | Description |
|---------|-------------|
| Curved striae | Curved growth lines (diagnostic) |
| Gas bubbles | Round, sometimes elongated |
| Swirl marks | Curved colour zoning |
| Inclusions | Typically very clean |

**Key indicator**: Curved striae visible under magnification, especially with immersion.

### Flux Growth

**Process**:
- Nutrients dissolved in molten flux (solvent)
- Slow crystallisation over months
- Produces crystals similar to natural

**Materials produced**:
- Flux emerald (Chatham, Gilson; preset: `synthetic-emerald-flux`)
- Flux ruby (Ramaura, Chatham; preset: `synthetic-ruby-flux`)
- Flux sapphire
- Flux alexandrite (preset: `synthetic-alexandrite-flux`)
- Flux spinel

**Detection features**:

| Feature | Description |
|---------|-------------|
| Flux inclusions | Wispy, feather-like, fingerprint-like |
| Platinum platelets | From crucible |
| Colour zoning | Angular but can mimic natural |
| Growth features | Characteristic patterns |

**Challenge**: Flux inclusions can resemble natural fingerprints—careful examination needed.

### Hydrothermal Growth

**Process**:
- Nutrients dissolved in water under high pressure/temperature
- Crystallises on seed plate
- Mimics natural geological conditions

**Materials produced**:
- Hydrothermal emerald (Biron, Regency, Tairus; preset: `synthetic-emerald-hydrothermal`)
- Hydrothermal ruby (preset: `synthetic-ruby-hydrothermal`)
- Hydrothermal sapphire
- Hydrothermal quartz (amethyst, citrine; preset: `synthetic-quartz-hydrothermal`)

**Detection features**:

| Feature | Description |
|---------|-------------|
| Chevron growth | V-shaped or zigzag growth lines |
| Seed plate | Flat boundary visible |
| Nail-head spicules | Characteristic inclusions |
| Two-phase inclusions | Can be present |
| Very clean | Often extremely clean |

**Hydrothermal Quartz**:
- Widely used for electronics industry
- Gem-quality commonly available
- Breadcrumb inclusions possible
- Very difficult to distinguish from natural

### Czochralski (Crystal Pulling)

**Process**:
- Seed dipped in melt
- Slowly pulled upward while rotating
- Creates cylindrical crystal

**Materials produced**:
- Synthetic alexandrite (preset: `synthetic-alexandrite-czochralski`)
- YAG (Yttrium Aluminium Garnet; preset: `yag`)
- GGG (Gadolinium Gallium Garnet; preset: `ggg`)
- LuAG (Lutetium Aluminium Garnet; preset: `luag`) -- newer simulant with higher RI than YAG
- Some laser crystals

**Detection**:
- Very clean
- Curved striae possible
- Gas bubbles rare

### Skull Melting

**Used for**: Cubic zirconia (CZ; preset: `cubic-zirconia`)
- Not relevant for coloured stone imitation
- Diamond simulant

## Detection by Gemstone Type

### Synthetic Ruby

| Method | Natural | Synthetic |
|--------|---------|-----------|
| **Flame fusion** | | |
| Inclusions | Silk, fingerprints, crystals | Curved striae, gas bubbles |
| Growth | Angular zoning | Curved colour bands |
| UV (LW) | Strong red | Very strong red (often) |
| **Flux** | | |
| Inclusions | Natural minerals | Flux veils, platinum |
| Growth | Natural patterns | Flux patterns |
| **Hydrothermal** | | |
| Inclusions | Natural suite | Chevron, nail-heads |
| Growth | Natural | Seed plate visible |

### Synthetic Sapphire

| Detection | Natural | Flame Fusion |
|-----------|---------|--------------|
| Striae | Straight | Curved |
| Inclusions | Silk, crystals, fingerprints | Gas bubbles, clean |
| Zoning | Hexagonal | Curved bands |

### Synthetic Emerald

| Method | Features |
|--------|----------|
| **Flux (Chatham, Gilson)** | Flux veils, wispy inclusions, phenakite crystals |
| **Hydrothermal (Biron)** | Chevron growth, nail-head spicules, very clean |

**Chelsea filter**: Synthetic emerald often shows stronger red than natural (higher Cr).

**UV fluorescence**: Some synthetics fluoresce differently than natural.

### Synthetic Spinel

**Flame fusion spinel** often used as simulant:
- "Hope Sapphire" blue (cobalt)
- Various colours
- Curved striae
- ADR (strain) on polariscope

### Synthetic Alexandrite

| Type | Features |
|------|----------|
| Czochralski | Very clean, strong colour change |
| Flux | Flux inclusions |

**Note**: True alexandrite synthetics are expensive; many "synthetic alexandrites" are actually synthetic colour-change corundum or spinel.

## Common Simulants

### Glass

**Properties**:
- Amorphous (isotropic but often shows strain)
- RI: 1.45-1.70 (typical)
- SG: Variable (2.2-4.5+)
- Hardness: 5-6

**Detection**:
| Feature | Observation |
|---------|-------------|
| Gas bubbles | Round, sometimes swirled |
| Flow lines | Visible under polariscope |
| Conchoidal fracture | Shell-like breaks |
| Warm to touch | Lower thermal conductivity |
| Surface wear | Scratches easily |
| Mould marks | Rounded facet junctions possible |

### Doublets and Triplets

**Doublet**: Two materials joined
- Garnet-topped doublet (GTD): Almandine top, glass base
- Opal doublet: Thin opal on backing

**Triplet**: Three layers
- Opal triplet: Cap + thin opal + backing
- Emerald triplet: Colourless beryl + green cement + colourless beryl

**Detection**:
- Examine girdle for join
- Immersion shows layers
- Bubbles in cement layer
- Different lustre on surfaces

### YAG (Yttrium Aluminium Garnet)

**Properties**:
- RI: 1.833 (isotropic)
- SG: 4.55
- Hardness: 8.5
- Dispersion: 0.028

**Use**: Diamond simulant, various colours
**Note**: Largely replaced by CZ

### GGG (Gadolinium Gallium Garnet)

**Properties**:
- RI: 2.02-2.03
- SG: 7.05
- High dispersion

**Use**: Diamond simulant (historical)

### Cubic Zirconia (CZ)

Not directly relevant for coloured stones but:
- Can be coloured
- RI: 2.15-2.18
- SG: 5.6-5.9
- Very high dispersion

### Specific Simulant Issues

| Natural Gem | Common Simulants |
|-------------|------------------|
| Ruby | Glass, GTD, synthetic ruby, red spinel |
| Sapphire | Glass, synthetic sapphire, synthetic spinel |
| Emerald | Glass, GTD, triplets, synthetic emerald |
| Alexandrite | Synthetic colour-change sapphire/spinel |
| Paraiba | Apatite, glass, coated topaz, synthetic Paraiba tourmaline (preset: `synthetic-paraiba`) |
| Tanzanite | Synthetic forsterite, glass, iolite |
| Jade | Serpentine, glass, dyed quartzite |
| Diamond | CZ (preset: `cubic-zirconia`), moissanite (preset: `moissanite`), YAG (preset: `yag`), LuAG (preset: `luag`), GGG (preset: `ggg`) |

## Testing Protocol

### Standard Sequence

1. **Visual inspection** (10x loupe)
   - Inclusions characteristic of natural?
   - Too clean?
   - Gas bubbles?

2. **Magnification** (microscope)
   - Growth patterns
   - Inclusion identification
   - Curved striae?

3. **Polariscope**
   - SR vs DR
   - ADR in synthetic spinel
   - Strain patterns

4. **Refractometer**
   - Confirm identity
   - Check against natural values

5. **Spectroscope**
   - Natural vs synthetic spectra
   - Dopants in simulants

6. **UV fluorescence**
   - Synthetic often stronger
   - Different colours possible

### Red Flags for Synthetic

- Too clean for gem type
- Perfect colour
- Extremely low price
- Curved growth features
- No origin documentation for expensive stones

## Disclosure Requirements

All synthetics and simulants must be disclosed:
- "Synthetic ruby" not just "ruby"
- "Lab-grown emerald"
- "Created alexandrite"
- Glass must not be called by gem name

## References

- `references/synthetic-detection.md` - Detailed detection methods
- `references/growth-methods.md` - Manufacturing processes
- `references/simulant-properties.md` - Simulant identification data
