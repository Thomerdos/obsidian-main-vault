# GitHub Copilot Instructions for Obsidian Concert Vault

## Repository Context

This is an Obsidian vault for managing concert attendance data with structured markdown files, YAML frontmatter, and Dataview queries using a **hub/star graph structure**.

## Key Changes (2026-02-03)

✅ **Migrated from** `.base` schema files + Python scripts
✅ **Migrated to** Native Dataview + hub/star structure  
✅ **Removed** External Python dependency for relationships
✅ **All relationships** now use native wiki links

## Directory Structure

```
obsidian-main-vault/
├── contenus/
│   ├── musique/
│   │   ├── Genres.md           # HUB for all genres
│   │   ├── Groupes.md          # HUB for all artists
│   │   ├── Salles.md           # HUB for all venues
│   │   ├── Festivals.md        # HUB for all festivals
│   │   ├── Concerts/YYYY/      # Individual concert files by year
│   │   ├── Groupes/            # Artist/band pages (65+ total)
│   │   ├── Genres/             # Musical genre pages (56+ total)
│   │   ├── Festivals/          # Festival pages (12+ total)
│   │   └── Salles/             # Venue pages (16+ total)
│   ├── lieux/
│   │   ├── Villes.md           # HUB for all cities
│   │   ├── Pays.md             # HUB for all countries
│   │   ├── Villes/             # City pages (14+ total)
│   │   └── Pays/               # Country pages (9+ total)
│   └── recettes/
│       ├── Ingredients.md      # HUB for ingredients
│       ├── Categories.md       # HUB for recipe categories
│       └── Fiches/             # Recipe files (60+ total)
└── templates/                  # Templater templates
```

## Hub/Star Structure

### What are Hub Pages?

Hub pages are central index pages that:
- Act as the central node for each entity type in Graph View
- Link to all entities of that type
- Use Dataview to dynamically list all entities
- Create clean star-shaped clusters in Graph View

### Entity Linking

**Every entity** (except concerts) must link to its hub:

```yaml
---
type: groupe
parent: "[[Groupes]]"  # Links to hub page
---
```

This creates the "star" topology where all groups connect to the Groupes hub.

## Frontmatter Schemas

### Concert
```yaml
type: concert
date: YYYY-MM-DD
groupes:
  - "[[Artist 1]]"
  - "[[Artist 2]]"
salle: "[[Venue Name]]"
festival: "[[Festival Name]]"
ville: "[[City]]"
pays: "[[Country]]"
rating: 5
tags:
  - concert
```

**Note**: Concerts do NOT have a `parent` field.

### Groupe (Artist)
```yaml
type: groupe
parent: "[[Groupes]]"          # REQUIRED
genre:
  - "[[Genre1]]"
  - "[[Genre2]]"
pays-origine: "[[Country]]"
formation: YYYY
site-web: https://...
tags:
  - groupe
```

### Genre
```yaml
type: genre
parent: "[[Genres]]"           # REQUIRED
related:                        # Optional
  - "[[Related Genre]]"
children:                       # Optional
  - "[[Sub-genre]]"
tags:
  - genre
```

### Salle (Venue)
```yaml
type: salle
parent: "[[Salles]]"           # REQUIRED
ville: "[[City]]"
pays: "[[Country]]"
capacite: 800
adresse: "Street address"
tags:
  - salle
```

### Festival
```yaml
type: festival
parent: "[[Festivals]]"        # REQUIRED
ville: "[[City]]"
pays: "[[Country]]"
periode: "Juin"
editions-vues:
  - 2024
  - 2023
tags:
  - festival
```

### Ville (City)
```yaml
type: ville
parent: "[[Villes]]"           # REQUIRED
pays: "[[Country]]"
region: "Region Name"
tags:
  - ville
```

### Pays (Country)
```yaml
type: pays
parent: "[[Pays]]"             # REQUIRED
continent: "Europe"
tags:
  - pays
```

## Important Rules

### Wiki Links in YAML

**ALWAYS** use double quotes around wiki links in YAML:

```yaml
# ✅ CORRECT
genre:
  - "[[Progressive Rock]]"
pays-origine: "[[France]]"

# ❌ WRONG
genre:
  - [[Progressive Rock]]
pays-origine: [[France]]
```

### Parent Field

**ALL entities (except concerts) must have parent field**:

```yaml
# ✅ CORRECT
type: groupe
parent: "[[Groupes]]"

# ❌ WRONG - Missing parent
type: groupe
tags:
  - groupe
```

### Obsolete Fields

**DO NOT** include these fields (removed in migration):
- ❌ `concerts: []`
- ❌ `groupes: []` (in genres)
- ❌ `genres: []`
- ❌ `groupe-concerts: [...]`
- ❌ `salle-concerts: [...]`
- ❌ `ville-concerts: [...]`
- ❌ `festival-editions: [...]`
- ❌ `editions: []` (in festivals)
- ❌ Any computed relationship fields

These are now calculated dynamically via Dataview queries.

## Dataview Query Patterns

### Artist Page - Show Concerts
```dataview
TABLE date as "Date", salle as "Salle", ville as "Ville"
FROM "contenus/musique/Concerts"
WHERE contains(groupes, this.file.name)
SORT date DESC
```

### Genre Page - Show Artists
```dataview
TABLE pays-origine as "Pays", formation as "Formation"
FROM "contenus/musique/Groupes"
WHERE contains(genre, this.file.name)
SORT file.name ASC
```

### Venue Page - Show Concerts
```dataview
TABLE date as "Date", groupes as "Artistes"
FROM "contenus/musique/Concerts"
WHERE contains(salle, this.file.name)
SORT date DESC
```

### Hub Page - List All Entities
```dataview
TABLE 
  genre as "Genres",
  pays-origine as "Pays",
  formation as "Formation"
FROM "contenus/musique/Groupes"
WHERE type = "groupe"
SORT file.name ASC
```

## Common Tasks

### Adding a New Concert

1. Create file: `contenus/musique/Concerts/YYYY/YYYY-MM-DD - Event.md`
2. Use concert template structure
3. Fill frontmatter with wiki links: `"[[Artist]]"`, `"[[Venue]]"`, etc.
4. Dataview queries will automatically show it on related pages

### Adding a New Artist

1. Create file: `contenus/musique/Groupes/Artist Name.md`
2. **MUST include** `parent: "[[Groupes]]"`
3. Use wiki links for genres and country
4. Artist appears automatically in Groupes hub and genre pages

### Adding a New Genre

1. Create file: `contenus/musique/Genres/Genre Name.md`
2. **MUST include** `parent: "[[Genres]]"`
3. Optionally add related/children genres using wiki links
4. Genre appears automatically in Genres hub

## Code Style Guidelines

### YAML
- Lowercase with hyphens: `pays-origine`, not `PaysOrigine`
- Wiki links in quotes: `"[[Page Name]]"`
- Arrays for multiple values: `genre: ["[[Genre1]]", "[[Genre2]]"]`

### Markdown
- Use emoji icons: 🎸 (concerts), 🎤 (groups), 🏛️ (venues), 🎪 (festivals)
- Use wiki links: `[[Page Name]]`
- Date format: `YYYY-MM-DD`

### File Naming
- Concerts: `YYYY-MM-DD - Event Name.md`
- Others: `Entity Name.md`

## Testing Changes

1. **Validate YAML** - Check frontmatter syntax
2. **Test Dataview** - Open in Obsidian to verify queries work
3. **Check Graph View** - Verify hub/star topology appears correctly
4. **Verify wiki links** - Ensure all `[[links]]` point to existing pages

## Tools Available

### Python Scripts (tools/)
- `add-concert.py` - Interactive concert creation
- `generate-stats.py` - Generate vault statistics

**Note**: Relationship management scripts have been removed (build-relations.py, sync-graph.py, migrate-vault.py, validate-schema.py) - no longer needed!

## Common Pitfalls to Avoid

1. ❌ Missing `parent` field in entities
2. ❌ Wiki links without quotes in YAML: `genre: [[Metal]]` → Use `"[[Metal]]"`
3. ❌ Including obsolete computed fields like `concerts: []`
4. ❌ Wrong hub page name: `parent: "[[Genre]]"` → Use `"[[Genres]]"` (plural)
5. ❌ Trying to run removed Python scripts
6. ❌ Creating `.base` schema files (no longer used)

## Best Practices

1. **Always use hub pages** - Don't skip the `parent` field
2. **Test in Obsidian** - Verify Dataview renders correctly
3. **Keep wiki links quoted** - Prevents YAML parsing errors
4. **Check Graph View** - Should show clean star patterns
5. **Use Dataview** - Let queries handle relationship display

---

**Remember**: This vault now uses native Obsidian features only. No Python scripts needed for relationships!
