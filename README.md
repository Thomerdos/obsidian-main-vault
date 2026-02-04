# 🎸 Obsidian Main Vault

A structured Obsidian vault for tracking concert attendance, recipes, and locations with **native Dataview queries** and **hub/star graph structure**.

## ✨ Features

This vault uses a clean hub/star structure that:
- ✅ **Native Obsidian wiki links** for all relationships
- ✅ **Hub pages** connect all entities of the same type in Graph View
- ✅ **Dataview queries** for dynamic relationship visualization
- ✅ **No external scripts needed** - everything works natively in Obsidian
- ✅ **Clean graph visualization** with star topology
- ✅ **Multiple domains**: Music, Locations, and Recipes
- ✅ **228+ notes** across concerts, artists, genres, venues, cities, countries, and recipes

## 🚀 Quick Start

### View Concerts
- **Main Index**: [`contenus/musique/Concerts.md`](contenus/musique/Concerts.md) - All concerts with statistics
- **By Year**: `contenus/musique/Concerts/YYYY/` - Individual concert files
- **By Artist**: `contenus/musique/Groupes/` - Artist pages with concert history
- **By Venue**: `contenus/musique/Salles/` - Venue pages with concerts held there

### Browse Recipes
- **All Recipes**: `contenus/recettes/Fiches/` - 60+ recipes with structured ingredients
- **By Ingredient**: `contenus/recettes/Ingredients/` - Find recipes by ingredient
- **Categories**: `contenus/recettes/Categories.md` - Browse by cuisine type

### Add Content

#### Using Templates
1. Navigate to `templates/` directory
2. Choose appropriate template (musique, lieux, recettes)
3. Fill in the template fields
4. Save to appropriate `contenus/` subdirectory

#### Semi-Automated Method - Concerts
```bash
# Add a concert interactively
python3 tools/add-concert.py
```

#### Semi-Automated Method - Recipes
```bash
# Option 1: Use Web Clipper (see docs/WEBCLIPPER-RECETTES.md)
# Clip recipe from web → Post-process with:
python3 tools/migrate-recipes.py --recipe "Recipe Name"

# Option 2: Migrate existing recipes
python3 tools/migrate-recipes.py
```

## 📂 Structure

```
obsidian-main-vault/
├── contenus/                # All content organized by domain
│   ├── musique/
│   │   ├── Genres.md        # Hub for all genres
│   │   ├── Groupes.md       # Hub for all groups
│   │   ├── Salles.md        # Hub for all venues
│   │   ├── Festivals.md     # Hub for all festivals
│   │   ├── Concerts/        # Concert files by year (57+ total)
│   │   ├── Groupes/         # Artist pages (65+ total)
│   │   ├── Genres/          # Musical genre pages (56+ total)
│   │   ├── Festivals/       # Festival pages (12+ total)
│   │   └── Salles/          # Venue pages (16+ total)
│   ├── lieux/
│   │   ├── Villes.md        # Hub for all cities
│   │   ├── Pays.md          # Hub for all countries
│   │   ├── Villes/          # City pages (14+ total)
│   │   └── Pays/            # Country pages (9+ total)
│   └── recettes/
│       ├── Ingredients.md   # Hub for ingredients
│       ├── Categories.md    # Hub for recipe categories
│       ├── Fiches/          # Recipe files (60+ total)
│       └── Ingredients/     # Individual ingredient pages
│
├── templates/               # Templater templates
│   ├── musique/             # Music templates
│   ├── lieux/               # Location templates
│   └── recettes/            # Recipe templates
│       ├── templater-recette.md          # New recipe template
│       ├── templater-ingredient.md       # Ingredient template
│       ├── webclipper-recette.md         # Web clipper template
│       └── templater-post-webclipper.md  # Post-process template
│
├── tools/                   # Python automation scripts
│   ├── add-concert.py       # Interactive concert creation
│   ├── generate-stats.py    # Generate vault statistics
│   └── migrate-recipes.py   # Recipe migration & ingredient extraction
│
├── docs/                    # Documentation
│   ├── WEBCLIPPER-RECETTES.md  # Web clipper guide for recipes
│   ├── RECIPES-WORKFLOW.md     # Complete recipes workflow
│   └── ...
│
├── .obsidian/               # Obsidian configuration
│   └── app.json             # Vault settings
│
├── README.md                # This file
├── README-RELATIONS.md      # Graph structure guide
└── requirements.txt         # Python dependencies
```

## 🔗 Hub/Star Graph Structure

The vault uses a clean hub/star topology for optimal graph visualization:

### Hub Pages (Central Nodes)
- **Music Domain**:
  - `Genres.md` → All genre pages
  - `Groupes.md` → All artist/band pages
  - `Salles.md` → All venue pages
  - `Festivals.md` → All festival pages
- **Location Domain**:
  - `Villes.md` → All city pages
  - `Pays.md` → All country pages
- **Recipe Domain**:
  - `Ingredients.md` → All ingredients
  - `Categories.md` → All recipe categories

### Entity Links
Each entity page links to its hub via `parent: "[[Hub Name]]"` in frontmatter, creating a star topology in Graph View.

### Relationships via Wiki Links
All relationships use native Obsidian wiki links:
- Concert pages → Artists, venues, festivals, cities, countries
- Artist pages → Genres, origin country
- Genre pages → Related genres, parent/child genres
- Venue/Festival pages → Cities, countries
- City pages → Countries

### Dynamic Queries
Dataview queries automatically show:
- **Artist pages** → All concerts where they played
- **Genre pages** → All artists and concerts of that genre
- **Venue pages** → All concerts at that venue
- **Festival pages** → All editions attended
- **City pages** → Venues and concerts in that city
- **Country pages** → Cities and concerts in that country

## 📊 Statistics

Current vault contains:
- **57+ concerts** (2013-2026)
- **65+ artists/groups**
- **56+ musical genres**
- **16+ venues** across multiple countries
- **12+ festivals**
- **14+ cities** with concert activity
- **60+ recipe files**

Top locations:
- 🇫🇷 France: 44+ concerts
- 🏙️ Vienne: 13+ concerts (Jazz à Vienne)
- 🏙️ Lyon: 11+ concerts

## 🛠️ Automation

### Python Scripts

Tools for vault management in `tools/` directory:
- `add-concert.py` - Interactive CLI to add concerts
- `generate-stats.py` - Generate vault statistics

### Usage

```bash
# Generate statistics
python3 tools/generate-stats.py --vault .

# Add a new concert interactively
python3 tools/add-concert.py
```

## 📖 Documentation

### General
- **[Graph Structure Guide](README-RELATIONS.md)** - Hub/star topology and Dataview queries
- **[Implementation Summary](IMPLEMENTATION-SUMMARY.md)** - Technical migration details

### Recipes System
- **[Recipe Workflow Guide](docs/RECIPES-WORKFLOW.md)** - Complete guide to the recipe system
- **[Web Clipper Guide](docs/WEBCLIPPER-RECETTES.md)** - How to clip recipes from the web
- **[Migration Script Documentation](tools/README-RECIPES.md)** - Script usage and customization

## 🍽️ Recipe Management System

### Features

This vault includes a powerful recipe management system with:
- ✅ **Structured ingredients** with automatic normalization
- ✅ **Wiki-linked ingredients** for easy navigation
- ✅ **Auto-generated ingredient pages** listing all recipes
- ✅ **Tag transformation** to structured properties
- ✅ **Web clipping support** for easy recipe capture
- ✅ **Migration script** to transform existing recipes
- ✅ **Dataview queries** for filtering and discovery

### Recipe Properties

Each recipe includes:
```yaml
type: recette
title: "Recipe Name"
source: "https://..."
type_cuisine: "Italienne"     # Cuisine type
origine: "Toscane"            # Geographic origin
regime: ["végétarien"]        # Dietary restrictions
saison: ["été"]               # Seasons
temps_preparation: 20         # Minutes
temps_cuisson: 45             # Minutes
ingredients:                  # Normalized ingredient list
  - tomate
  - basilic
  - mozzarella
```

### Quick Recipe Workflow

1. **Clip from web**: Use Web Clipper with the recipe template
2. **Process**: Run `python3 tools/migrate-recipes.py --recipe "Name"`
3. **Complete**: Fill in metadata (cuisine, origin, times)
4. **Enjoy**: Navigate between recipes and ingredients!

### Example Dataview Queries

Find all recipes with tomatoes:
```dataview
TABLE temps_preparation, type_cuisine
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, "tomate")
```

Find vegetarian Italian recipes:
```dataview
LIST
FROM "contenus/recettes/Fiches"
WHERE type_cuisine = "Italienne" AND contains(regime, "végétarien")
```

See [Recipe Workflow Guide](docs/RECIPES-WORKFLOW.md) for more examples.

## 🔐 Data Quality

All concert files include:
- ✅ Complete frontmatter (type, date, location)
- ✅ Valid YAML syntax
- ✅ Location mappings (ville/pays)
- ✅ Artist lists
- ✅ Wiki-style links to entities

Last verified: 2026-02-03 (100% complete)

## 🤝 Contributing

### Adding Content

#### Concerts
1. Use template from `templates/musique/templater-concert.md`
2. Save to `contenus/musique/Concerts/YYYY/YYYY-MM-DD - Event.md`
3. Ensure all frontmatter fields are filled
4. Create missing entity pages (artists, venues) if needed

#### Recipes

**Method 1: Web Clipper (Recommended)**
1. Use Obsidian Web Clipper extension with `templates/recettes/webclipper-recette.md`
2. Clip recipe from any website
3. Post-process: `python3 tools/migrate-recipes.py --recipe "Name"`
4. Complete metadata fields

**Method 2: Manual Creation**
1. Use template from `templates/recettes/templater-recette.md`
2. Save to `contenus/recettes/Fiches/`
3. Fill all frontmatter fields
4. List ingredients in `ingredients: []` property
5. Use `[[ingredient]]` links in the ingredients section

**Method 3: Migration**
1. Place recipe in `contenus/recettes/Fiches/`
2. Run: `python3 tools/migrate-recipes.py`
3. Script will extract ingredients and create links

See [Recipe Workflow Guide](docs/RECIPES-WORKFLOW.md) for details.

#### Locations
1. Use templates from `templates/lieux/`
2. Save to `contenus/lieux/Villes/` or `contenus/lieux/Pays/`
3. Maintain relationships to concerts and venues

### Maintaining Consistency

- Use lowercase-with-hyphens for YAML keys: `pays-origine`
- Use wiki links in YAML: `"[[Page Name]]"`
- Date format: `YYYY-MM-DD`
- Include emoji icons: 🎸 (concerts), 🎤 (groups), 🏛️ (venues)

## 📱 Obsidian Setup

### Required Plugins
- **Dataview** - For automatic relationship queries and recipe filtering

### Recommended Plugins
- **Templater** - For quick template insertion
- **Calendar** - For date-based navigation
- **Excalidraw** - For concert memory drawings
- **Web Clipper** - For capturing recipes from websites (browser extension)

### Theme Compatibility
Works with all Obsidian themes. Tested with:
- Default theme
- Minimal theme
- Things theme

## 🗺️ Graph View

The hub/star structure creates clean graph visualization:

```
                         ┌──────────┐
              ┌──────────│  Genres  │──────────┐
              │          └──────────┘          │
              ▼               ▼                ▼
         ┌─────────┐    ┌──────────┐     ┌─────────┐
         │  Jazz   │←──→│Prog Rock │←───→│  Metal  │
         └─────────┘    └──────────┘     └─────────┘
              │              │                │
              ▼              ▼                ▼
         ┌─────────┐    ┌──────────┐     ┌─────────┐
         │Groupes  │    │ Concerts │     │ Salles  │
         │  hub    │    │          │     │  hub    │
         └─────────┘    └──────────┘     └─────────┘
              │                               │
    ┌─────────┼─────────┐           ┌────────┼────────┐
    ▼         ▼         ▼           ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐  ┌───────┐ ┌───────┐ ┌───────┐
│ Magma │ │ Ghost │ │Ayreon │  │Le Sucre│ │ 013  │ │Olympia│
└───────┘ └───────┘ └───────┘  └───────┘ └───────┘ └───────┘
```

Each entity type has its own hub creating star topologies that connect through actual relationships (concerts, shared genres, locations).

## 🗺️ Roadmap

- [x] ~~Relational database system with automatic bidirectional links~~
- [x] ~~Schema-based validation and migration tools~~
- [x] ~~Graph View with color-coded entity types~~
- [x] ~~Auto-detection of similar artists and related content~~
- [x] ~~Restructured directory organization~~
- [x] ~~Recipe schema and templates~~
- [x] **Migration to native Dataview with hub/star structure**
- [x] **Removed external Python dependency for relationships**
- [ ] Enhanced concert addition workflow
- [ ] Backup/export functionality
- [ ] Concert photo gallery integration
- [ ] Setlist import from setlist.fm API
- [ ] Recipe import from common formats

## 📜 License

This is a personal vault. All concert data is original content by the vault owner.

## 🙋 Support

For questions about structure or automation:
1. Check [Copilot Instructions](.github/copilot/instructions.md)
2. Review [Structure Guide](Musique/README-STRUCTURE.md)
3. Open a GitHub Issue for bugs or feature requests
