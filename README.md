# 🎸 Obsidian Main Vault

A structured Obsidian vault for tracking concert attendance, recipes, and locations with **automatic relationship management** and **full relational database system**.

## ✨ Features

This vault includes a complete relational database system that:
- ✅ **Automatically manages bidirectional relationships** between all entities
- ✅ **Visualizes connections in Graph View** with color-coded entity types
- ✅ **Auto-detects similar artists**, co-occurring genres, and tour companions
- ✅ **Validates data integrity** with schema enforcement
- ✅ **Supports multiple domains**: Music, Locations, and Recipes
- ✅ **228+ notes with 291+ relationships** across concerts, artists, genres, venues, cities, countries, and recipes

**📚 [See the complete relational system guide →](README-RELATIONS.md)**

## 🚀 Quick Start

### View Concerts
- **Main Index**: [`contenus/musique/Concerts.md`](contenus/musique/Concerts.md) - All concerts with statistics
- **By Year**: `contenus/musique/Concerts/YYYY/` - Individual concert files
- **By Artist**: `contenus/musique/Groupes/` - Artist pages with concert history
- **By Venue**: `contenus/musique/Salles/` - Venue pages with concerts held there

### Add Content

#### Using Templates
1. Navigate to `templates/` directory
2. Choose appropriate template (musique, lieux, recettes)
3. Fill in the template fields
4. Save to appropriate `contenus/` subdirectory

#### Semi-Automated Method
Use Python scripts in `tools/`:
```bash
# Add a concert interactively
python3 tools/add-concert.py

# Build relationships
python3 tools/build-relations.py --vault .

# Validate schemas
python3 tools/validate-schema.py --vault .
```

## 📂 Structure

```
obsidian-main-vault/
├── bases/                    # Entity schemas (visible in Obsidian)
│   ├── musique/             # Music entity schemas
│   │   ├── concert.base
│   │   ├── groupe.base
│   │   ├── genre.base
│   │   ├── festival.base
│   │   └── salle.base
│   ├── lieux/               # Location entity schemas
│   │   ├── ville.base
│   │   └── pays.base
│   └── recettes/            # Recipe entity schemas
│       ├── recette.base
│       ├── ingredient.base
│       └── categorie-recette.base
│
├── contenus/                # All content organized by domain
│   ├── musique/
│   │   ├── Concerts/        # Concert files by year (56+ total)
│   │   ├── Groupes/         # Artist pages (67+ total)
│   │   ├── Genres/          # Musical genre pages (56+ total)
│   │   ├── Festivals/       # Festival pages (12+ total)
│   │   └── Salles/          # Venue pages (15+ total)
│   ├── lieux/
│   │   ├── Villes/          # City pages (14+ total)
│   │   └── Pays/            # Country pages (9+ total)
│   └── recettes/
│       └── Fiches/          # Recipe files (60+ total)
│
├── templates/               # Templater templates
│   ├── musique/             # Music templates
│   ├── lieux/               # Location templates
│   └── recettes/            # Recipe templates
│
├── tools/                   # Python automation scripts
│   ├── migrate-vault.py     # Migrate notes to relational system
│   ├── build-relations.py   # Build bidirectional relationships
│   ├── validate-schema.py   # Validate notes against schemas
│   ├── sync-graph.py        # Synchronize graph relationships
│   ├── generate-stats.py    # Generate vault statistics
│   └── add-concert.py       # Interactive concert creation
│
├── docs/                    # Documentation
│   ├── GRAPH-GUIDE.md       # Graph visualization guide
│   ├── RELATIONS.md         # Relationship system docs
│   └── SCHEMA.md            # Schema documentation
│
├── .obsidian/               # Obsidian configuration
│   └── app.json             # Vault settings
│
├── README.md                # This file
├── README-RELATIONS.md      # Relational system guide
└── IMPLEMENTATION-SUMMARY.md # Technical implementation details
```

## 🔗 Automatic Relationships

All pages include automatic relationship management:

- **Concert pages** → Auto-link to artists, venues, cities, countries, festivals
- **Artist pages** → List all concerts where they played
- **Genre pages** → List all artists and concerts of that genre
- **Venue pages** → List all concerts at that venue
- **Festival pages** → List all editions attended
- **City pages** → List venues and concerts in that city
- **Country pages** → List cities and concerts in that country
- **Recipe pages** → Link to ingredients and categories
- **Ingredient pages** → List all recipes using this ingredient

## 📊 Statistics

Current vault contains:
- **56+ concerts** (2013-2026)
- **67+ artists/groups**
- **56+ musical genres**
- **15+ venues** across multiple countries
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
- `migrate-vault.py` - Migrate notes to relational system
- `build-relations.py` - Build and maintain bidirectional relationships
- `validate-schema.py` - Validate notes against schema definitions
- `sync-graph.py` - Synchronize graph relationships
- `generate-stats.py` - Generate vault statistics
- `add-concert.py` - Interactive CLI to add concerts

### Usage

```bash
# Validate all schemas and notes
python3 tools/validate-schema.py --vault .

# Build relationships between entities
python3 tools/build-relations.py --vault .

# Generate statistics
python3 tools/generate-stats.py --vault .

# Add a new concert interactively
python3 tools/add-concert.py
```

## 📖 Documentation

- **[Relational System Guide](README-RELATIONS.md)** - Complete guide to the relationship system
- **[Implementation Summary](IMPLEMENTATION-SUMMARY.md)** - Technical implementation details
- **[Graph Guide](docs/GRAPH-GUIDE.md)** - How to use the graph view
- **[Relations Documentation](docs/RELATIONS.md)** - Relationship documentation
- **[Schema Documentation](docs/SCHEMA.md)** - Schema format and usage

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
1. Use templates from `templates/recettes/`
2. Save to `contenus/recettes/Fiches/`
3. Link to ingredients using `[[ingredient]]` syntax
4. Add appropriate tags and categories

#### Locations
1. Use templates from `templates/lieux/`
2. Save to `contenus/lieux/Villes/` or `contenus/lieux/Pays/`
3. Maintain relationships to concerts and venues

### Maintaining Consistency

- Use lowercase-with-hyphens for YAML keys: `pays-origine`
- Use JSON arrays in YAML: `groupes: ["Artist1", "Artist2"]`
- Use wiki links: `[[Page Name]]`
- Date format: `YYYY-MM-DD`
- Include emoji icons: 🎸 (concerts), 🎤 (groups), 🏛️ (venues)

## 📱 Obsidian Setup

### Required Plugins
- **Dataview** - For automatic relationship queries

### Recommended Plugins
- **Templater** - For quick template insertion
- **Calendar** - For date-based navigation
- **Excalidraw** - For concert memory drawings

### Theme Compatibility
Works with all Obsidian themes. Tested with:
- Default theme
- Minimal theme
- Things theme

## 🔗 Relational System

The vault uses a complete relational database system:

- **10 Entity Types**: concerts, artists, genres, venues, festivals, cities, countries, recipes, ingredients, recipe categories
- **291+ Relationships**: automatically maintained bidirectional links
- **Auto-Detection**: similar artists, genre co-occurrence, tour companions
- **Graph View**: visualize all connections with color-coded nodes
- **Schema Validation**: ensures data integrity across all domains
- **Recursive Schema Loading**: supports organized subdirectories in `bases/`

### Entity Schemas

All entity types are defined in `.base` files in the `bases/` directory:

**Music Domain** (`bases/musique/`):
- concert.base, groupe.base, genre.base, festival.base, salle.base

**Location Domain** (`bases/lieux/`):
- ville.base, pays.base

**Recipe Domain** (`bases/recettes/`):
- recette.base, ingredient.base, categorie-recette.base

### Quick Commands

```bash
# Migrate data
python3 tools/migrate-vault.py --vault .

# Build relationships
python3 tools/build-relations.py --vault .

# Validate data
python3 tools/validate-schema.py --vault .

# Generate statistics
python3 tools/generate-stats.py --vault .
```

**📚 [Complete relational system guide →](README-RELATIONS.md)**

## 🗺️ Roadmap

- [x] ~~Relational database system with automatic bidirectional links~~
- [x] ~~Schema-based validation and migration tools~~
- [x] ~~Graph View with color-coded entity types~~
- [x] ~~Auto-detection of similar artists and related content~~
- [x] ~~Restructured directory organization (bases/, contenus/, templates/)~~
- [x] ~~Recipe schema and templates~~
- [x] ~~Recursive schema loading from subdirectories~~
- [ ] GitHub Actions for automated concert addition
- [ ] Enhanced Python CLI tools
- [ ] Data validation workflow
- [ ] Statistics auto-update workflow
- [ ] Wiki link checker workflow
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
