# Kotti Brand Guidelines
## V4 Corner Line — Amber Heritage

### Mark Elements

The mark consists of 4 elements:

1. **Roofline** — heaviest stroke, defines the perspective silhouette
2. **Corner line** — dashed vertical at the building bend (the NKZ corner)
3. **Balcony grid** — 2–3 horizontal lines fading in opacity (50% → 33% → 18%)
4. **Arc base** — curved line representing the commercial plinth/foundation

Optional: ghost mass fill at 4–6% opacity behind the mark.

### Clear Space

Minimum clear space around the mark = **height of the arc base curve** on all sides.
For the wordmark lockup, clear space = **cap height of "k"** on all sides.

### Minimum Sizes

| Context         | Min width | Elements shown                        |
|-----------------|-----------|---------------------------------------|
| Hero / display  | 120px+    | All 4 elements + ghost mass           |
| Navigation      | 64–96px   | Roofline + corner + 2 balconies + arc |
| Icon / badge    | 48px      | Roofline + 1 balcony + arc (no corner)|
| Favicon         | 16–32px   | Roofline + arc only                   |

The corner line drops at sizes below 64px. Balcony count reduces progressively.

### Color Palette — Amber Heritage

| Role       | Hex       | Usage                                    |
|------------|-----------|------------------------------------------|
| Primary    | `#D4920B` | Mark, links, active states, brand color  |
| Highlight  | `#F5C842` | Hover states, callouts, light accents    |
| Accent     | `#C44B1A` | Warnings, destructive actions, errors    |
| Dark       | `#1A1714` | Backgrounds (dark mode), text (light)    |
| Light      | `#F7F3ED` | Backgrounds (light mode), text (dark)    |

### Color Modes

- **Dark on dark**: Amber `#D4920B` mark on `#0E0D0B` / `#1A1714` background
- **Dark on light**: Dark `#1A1714` mark on `#F7F3ED` background, amber ghost fill
- **On brand**: Dark `#1A1714` mark on `#D4920B` amber background
- **Monochrome**: White `#E8E4DC` mark on dark, or dark on white (no amber)

### Typography

Single-font system: **JetBrains Mono** throughout.

| Role       | Weight | Size (docs) | Usage                         |
|------------|--------|-------------|-------------------------------|
| Display    | 700    | 2rem+       | Page titles, hero text        |
| Heading    | 600–700| 1.2–1.6rem  | Section headings              |
| Body       | 400    | 0.82rem     | Body text, descriptions       |
| Code       | 400    | 0.78rem     | Code blocks, inline code      |
| Label      | 500    | 0.68rem     | Navigation, tags, meta        |

### Wordmark

- **Lowercase bold** `kotti` — default, casual, developer-friendly
- **Spaced caps** `KOTTI` — formal contexts, letterheads, presentations
- Wordmark font: JetBrains Mono Bold (700)

### Don'ts

- Don't rotate or skew the mark
- Don't change the wing ratio (the asymmetry is intentional)
- Don't use colors outside the palette
- Don't outline the full building shape (that's the old logo)
- Don't add the corner line at sizes below 64px
- Don't place on busy photo backgrounds without overlay

### File Inventory

```
svg/
├── kotti-mark-dark.svg          # Amber on dark background
├── kotti-mark-light.svg         # Dark on light background
├── kotti-mark-mono-white.svg    # White monochrome
├── kotti-favicon.svg            # 16px simplified (roof + arc)
├── kotti-wordmark-dark.svg      # Horizontal lockup, dark bg
├── kotti-wordmark-light.svg     # Horizontal lockup, light bg
└── kotti-wordmark-stacked-dark.svg  # Stacked lockup

mkdocs-theme/
├── mkdocs.yml                   # Full MkDocs config
├── stylesheets/
│   └── kotti.css                # Material for MkDocs brand skin
└── overrides/
    └── partials/
        └── logo.html            # Inline SVG logo partial
```

### MkDocs Setup

Material for MkDocs is the **base infrastructure**. The Kotti brand is applied as a skin:

1. `pip install mkdocs-material`
2. Copy `mkdocs.yml` to project root
3. Copy `stylesheets/kotti.css` to `docs/stylesheets/`
4. Copy `overrides/` to `docs/overrides/`
5. Copy SVG assets to `docs/assets/`
6. `mkdocs serve`

The CSS overrides Material's custom properties for colors, fonts, and component
styles. All Material features (search, tabs, dark mode, versioning, code copy,
admonitions, etc.) work unchanged.
