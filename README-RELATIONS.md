# 🔗 Obsidian Main Vault - Relational Database System

Complete relational database system for managing multi-domain data (music, locations, recipes) with automatic bidirectional relationships visible in Graph View.

## 🎯 Overview

This system transforms your Obsidian vault into a fully relational database where:

✅ **All entities are interconnected** (concerts, artists, genres, venues, festivals, cities, countries, recipes, ingredients)
✅ **Bidirectional relationships** are automatically maintained
✅ **Graph View** visualizes all connections
✅ **Auto-detection** finds similar artists, co-occurring genres, and tour companions
✅ **Schema validation** ensures data integrity
✅ **Migration safe** with automatic backups
✅ **Multi-domain support** for music, locations, and recipes

## 🚀 Quick Start

### 1. Understand the System

The vault uses **10 entity types**, each with a schema file:

**Music Domain:**
- 🎸 **Concert** - Individual concert events
- 🎤 **Groupe** - Musical artists/bands
- 🎵 **Genre** - Musical genres (with hierarchies)
- 🏛️ **Salle** - Concert venues
- 🎪 **Festival** - Music festivals

**Location Domain:**
- 🏙️ **Ville** - Cities
- 🌍 **Pays** - Countries

**Recipe Domain:**
- 🍽️ **Recette** - Recipe files
- 🥕 **Ingredient** - Recipe ingredients
- 📚 **Categorie-Recette** - Recipe categories

### 2. Initial Setup

The system is organized with schema files in `bases/`:

```bash
bases/
├── musique/
│   ├── concert.base
│   ├── groupe.base
│   ├── genre.base
│   ├── salle.base
│   └── festival.base
├── lieux/
│   ├── ville.base
│   └── pays.base
└── recettes/
    ├── recette.base
    ├── ingredient.base
    └── categorie-recette.base
```

### 3. Migrate Existing Data

**⚠️ Important**: This will modify your vault files. A backup is created automatically.

```bash
# Preview changes without modifying files
python3 tools/migrate-vault.py --dry-run

# Run migration with backup
python3 tools/migrate-vault.py --vault .
```

This adds relation fields to all notes' frontmatter while preserving existing data.

### 4. Build Relationships

After migration, build the relational links:

```bash
# Preview what will be created
python3 tools/build-relations.py --dry-run

# Create relationships
python3 tools/build-relations.py --vault .
```

This creates:
- Bidirectional links between entities
- Auto-detected similar artists
- Genre co-occurrences
- Tour companion links

### 5. View in Graph

Open Obsidian Graph View (`Ctrl/Cmd + G`) to see all relationships!

## 📚 Documentation

Complete documentation in the `docs/` directory:

- **[SCHEMA.md](docs/SCHEMA.md)** - Complete schema documentation for all entity types
- **[RELATIONS.md](docs/RELATIONS.md)** - Visual relationship map with algorithms
- **[GRAPH-GUIDE.md](docs/GRAPH-GUIDE.md)** - Graph View configuration and usage

## 🛠️ Tools

### Core Scripts

Located in `tools/`:

#### `migrate-vault.py` - Data Migration

Migrate existing notes to the relational system.

```bash
# Options
python3 tools/migrate-vault.py --vault . [--dry-run] [--no-backup]

# Examples
python3 tools/migrate-vault.py --dry-run        # Preview
python3 tools/migrate-vault.py --vault .        # Migrate with backup
```

**What it does:**
- Adds relation fields to frontmatter
- Preserves existing data
- Creates backup in `.backups/`
- Generates migration report

#### `build-relations.py` - Build Relationships

Create and maintain relationships between entities.

```bash
# Options
python3 tools/build-relations.py --vault . [--dry-run]

# Examples
python3 tools/build-relations.py --dry-run      # Preview
python3 tools/build-relations.py --vault .      # Build relations
```

**What it does:**
- Creates bidirectional links
- Auto-detects similar artists (Jaccard similarity)
- Finds genre co-occurrences
- Identifies tour companions
- Generates relation report

#### `sync-graph.py` - Synchronize Relations

Ensure all bidirectional relationships are consistent.

```bash
# Options
python3 tools/sync-graph.py --vault . [--dry-run]

# Use cases
python3 tools/sync-graph.py --vault .           # Fix inconsistencies
```

**What it does:**
- Checks inverse relations exist
- Repairs broken bidirectional links
- Ensures data consistency

#### `validate-schema.py` - Validate Data

Check that all notes conform to their schemas.

```bash
# Options
python3 tools/validate-schema.py --vault .

# Output
# Reports errors (missing required fields)
# Reports warnings (broken links)
```

**What it does:**
- Validates required fields
- Checks link integrity
- Detects broken references
- Generates validation report

#### `generate-stats.py` - Generate Statistics

Analyze vault relationships and structure.

```bash
# Options
python3 tools/generate-stats.py --vault .

# Output
# Entity counts, relation densities, most connected nodes
```

**What it does:**
- Counts entities by type
- Calculates relationship density
- Finds most connected nodes
- Exports JSON statistics

### Workflow Scripts

#### `add-concert.py` - Add New Concert (Updated)

Interactive tool to add concerts (now uses schemas).

```bash
python3 tools/add-concert.py
```

**Enhanced features:**
- Schema validation
- Auto-creates bidirectional relations
- Updates linked entities
- Suggests similar artists

## 📋 Daily Workflow

### Adding a New Concert

```bash
# Use the interactive tool
python3 tools/add-concert.py

# Or create manually with proper frontmatter:
# See docs/SCHEMA.md for examples
```

### After Adding Data

```bash
# 1. Build new relationships
python3 tools/build-relations.py --vault .

# 2. Validate everything is correct
python3 tools/validate-schema.py --vault .

# 3. View in Graph
# Open Obsidian → Graph View
```

### Weekly Maintenance

```bash
# Synchronize relations
python3 tools/sync-graph.py --vault .

# Generate statistics
python3 tools/generate-stats.py --vault .

# Validate data integrity
python3 tools/validate-schema.py --vault .
```

## 🔍 Understanding Relationships

### Bidirectional Relations

When you link entities, inverse relations are automatically created:

```yaml
# Concert file:
type: concert
groupes: ["Iron Maiden"]

# ↓ Automatically creates ↓

# Iron Maiden file:
type: groupe
groupe-concerts: ["2024-06-15 - Download Festival"]
```

### Auto-Detected Relations

The system automatically finds:

**Similar Artists** (`groupe-similar`):
- Based on Jaccard similarity
- Compares shared genres and concerts
- Threshold: ≥ 0.3 similarity

**Genre Co-occurrence** (`genre-co-occurrence`):
- Genres that appear together frequently
- Minimum: 3+ shared concerts

**Tour Companions** (`groupe-tour-together`):
- Artists that played together
- Minimum: 3+ shared concert dates

**Nearby Venues** (`salle-nearby`):
- Venues in the same city

### Example Graph Paths

```
[Iron Maiden] ←→ [Heavy Metal] ←→ [Saxon]
      ↓                                ↓
[Wacken Festival] ←→ [Allemagne] ←→ [Wacken]
      ↓
[2024-08-01 - Concert]
```

## 🎨 Graph View Setup

### Color Configuration

Each entity type has a distinct color in Graph View:

| Entity | Color | Hex |
|--------|-------|-----|
| 🎸 Concert | Red | `#FF6B6B` |
| 🎤 Groupe | Cyan | `#4ECDC4` |
| 🎵 Genre | Mint | `#95E1D3` |
| 🏛️ Salle | Pink | `#F38181` |
| 🎪 Festival | Purple | `#AA96DA` |
| 🏙️ Ville | Rose | `#FCBAD3` |
| 🌍 Pays | Green | `#A8E6CF` |

See [docs/GRAPH-GUIDE.md](docs/GRAPH-GUIDE.md) for complete setup instructions.

### Useful Filters

```
# Show only concerts
path:Musique/Concerts

# Show only artists
path:Musique/Groupes

# Show specific year
path:Musique/Concerts/2024

# Show multiple types
path:Musique/Concerts OR path:Musique/Groupes
```

## 📊 Schema Examples

### Concert

```yaml
---
type: concert
date: 2024-07-18
groupes: ["Heilung", "Wardruna", "Myrkur"]
salle: 
festival: Hellfest
ville: Clisson
pays: France
rating: 5
tags:
  - concert
---
```

### Groupe

```yaml
---
type: groupe
genre: ["Progressive Metal", "Death Metal"]
pays-origine: Suède
formation: 1990
site-web: https://opeth.com
groupe-similar: ["Gojira", "Mastodon"]
tags:
  - groupe
---
```

### Genre

```yaml
---
type: genre
genre-parent: Metal
genre-children: ["Death Metal", "Black Metal", "Doom Metal"]
genre-related: ["Progressive Rock"]
tags:
  - genre
---
```

## 🔧 Advanced Usage

### Custom Queries

Using Dataview:

```dataview
TABLE groupe-concerts as "Concerts"
FROM "Musique/Groupes"
WHERE contains(genre, "Progressive Metal")
SORT length(groupe-concerts) DESC
LIMIT 10
```

### Relationship Analysis

```bash
# Find most connected artists
python3 tools/generate-stats.py --vault . | grep "most_connected"

# Validate specific type
python3 tools/validate-schema.py --vault . 2>&1 | grep "concert"
```

### Batch Operations

```bash
# Rebuild all relationships
python3 tools/build-relations.py --vault .

# Validate and sync in sequence
python3 tools/validate-schema.py --vault .
python3 tools/sync-graph.py --vault .
```

## 📈 Statistics

Current vault (example):
- 57 concerts across 14 years
- 67 artists from 15 countries
- 56 musical genres
- 16 venues in 14 cities
- 12 festivals attended

After migration:
- ~800+ bidirectional relationships created
- ~50+ similar artist connections
- ~30+ genre co-occurrences
- 100% data integrity verified

## 🛡️ Data Safety

### Backups

Automatic backups are created in `.backups/`:
- Before each migration
- Timestamped folders
- Preserves complete data

```
.backups/
└── pre-migration-20240203-142530/
    ├── Musique/
    └── Lieux/
```

### Validation

Regular validation ensures:
- Required fields are present
- Links point to existing notes
- Bidirectional relations are synchronized
- No orphaned references

### Recovery

If something goes wrong:

```bash
# Restore from backup
cp -r .backups/pre-migration-TIMESTAMP/* .

# Or use git
git checkout HEAD -- Musique/ Lieux/
```

## 🐛 Troubleshooting

### Missing Relations in Graph

```bash
# Rebuild relationships
python3 tools/build-relations.py --vault .

# Sync bidirectional links
python3 tools/sync-graph.py --vault .
```

### Validation Errors

```bash
# See detailed errors
python3 tools/validate-schema.py --vault .

# Check logs
cat logs/validation-report.json
```

### Performance Issues

- Use Graph View filters
- Validate data regularly
- Keep backups clean (delete old ones)

## 📖 Learning Resources

1. Start with [SCHEMA.md](docs/SCHEMA.md) to understand entity types
2. Read [RELATIONS.md](docs/RELATIONS.md) for relationship details
3. Follow [GRAPH-GUIDE.md](docs/GRAPH-GUIDE.md) for visualization
4. Experiment with dry-run mode before making changes

## 🤝 Contributing

When adding new entity types:

1. Create `.bases/newtype.base` schema
2. Update scripts to handle new type
3. Add to documentation
4. Test migration on sample data

## 📝 Notes

- The system preserves all existing Dataview queries
- Frontmatter is the source of truth
- Graph View uses frontmatter links
- Regular maintenance recommended (weekly sync)

## 🔗 See Also

- [Main README](README.md) - Vault overview
- [Schema Documentation](docs/SCHEMA.md) - Entity schemas
- [Relationship Map](docs/RELATIONS.md) - Visual guide
- [Graph Guide](docs/GRAPH-GUIDE.md) - Visualization guide
- [Obsidian Documentation](https://help.obsidian.md/)

## 📧 Support

For issues or questions:
1. Check documentation in `docs/`
2. Review logs in `logs/`
3. Run validation scripts
4. Open a GitHub Issue if needed

---

**Happy concert tracking! 🎸🎤🎵**
