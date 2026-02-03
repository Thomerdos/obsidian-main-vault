# GitHub Copilot Instructions for Obsidian Concert Vault

## Repository Context

This is an Obsidian vault for managing concert attendance data with structured markdown files, YAML frontmatter, and Dataview queries for automatic relationships.

## Directory Structure

```
obsidian-main-vault/
├── Musique/
│   ├── Concerts.md              # Main concert index
│   ├── _templates/              # Reusable templates
│   ├── Concerts/YYYY/           # Individual concert files by year
│   ├── Groupes/                 # Artist/band pages
│   ├── Genres/                  # Musical genre pages (56 total)
│   ├── Festivals/               # Festival pages
│   └── Salles/                  # Venue pages
└── Lieux/
    ├── Villes/                  # City pages
    └── Pays/                    # Country pages
```

## Key Concepts

### 1. Entity Types

- **Concert**: Individual concert event with date, artists, location
- **Groupe**: Artist/band with concert history and genres
- **Genre**: Musical genre with artists and concerts of that style
- **Salle**: Venue with location and concerts held there
- **Festival**: Recurring festival with editions attended
- **Ville**: City with venues and concerts
- **Pays**: Country with cities and concerts

### 2. Frontmatter Schema

Each entity has structured YAML frontmatter:

```yaml
# Concert
type: concert
date: YYYY-MM-DD
groupes: ["Artist 1", "Artist 2"]
salle: Venue Name
festival: Festival Name
ville: City
pays: Country
rating:
tags: [concert]

# Groupe
type: groupe
genre: ["Genre1", "Genre2"]
pays-origine: 
formation: 
site-web: 
tags: [groupe]

# Genre
type: genre
tags: [genre]

# Salle
type: salle
ville: City
pays: Country
capacite: 
adresse: 
tags: [salle]
```

### 3. Automatic Relationships

All templates include Dataview queries that create bidirectional links:
- Group pages show all concerts where they played and link to genres
- Genre pages list all artists and concerts of that genre
- Venue pages list all concerts at that venue
- City pages show all venues and concerts
- Festival pages track all editions attended

### 4. Location Mappings

Automatic location inference via cascading mappings:
1. Festival → Ville (e.g., Hellfest → Clisson)
2. Salle → Ville (e.g., Brin de Zinc → Lyon)
3. Ville → Pays (e.g., Lyon → France)

## Common Tasks

### Adding a New Concert

1. Create file: `Musique/Concerts/YYYY/YYYY-MM-DD - Event.md`
2. Use template from `Musique/_templates/template-concert.md`
3. Fill frontmatter with date, artists, venue/festival, location
4. Add line to `Musique/Concerts.md` in appropriate year section
5. Create missing entity pages (groups, venues) if needed

### Adding a New Group/Genre/Venue/Festival

1. Copy appropriate template from `_templates/`
2. Create file in correct directory (Groupes/, Genres/, Salles/, Festivals/)
3. Fill frontmatter with required fields
4. For groups, use wiki links for genres: `- **Genre** : [[Heavy Metal]], [[Progressive Rock]]`
5. Dataview queries will automatically list related concerts

### Updating Main Index

The `Concerts.md` file should maintain:
- Links to individual concert files
- Dataview queries for each year
- Statistics sections (top groups, venues, cities)

## Dataview Query Patterns

```dataview
# List concerts by group
TABLE date, salle, ville
FROM "Musique/Concerts"
WHERE contains(groupes, "Group Name")
SORT date DESC

# Count concerts by venue
TABLE length(rows) as "Concerts"
FROM "Musique/Concerts"
WHERE salle != null
GROUP BY salle
SORT length(rows) DESC

# Upcoming concerts
TABLE groupes, salle, ville
FROM "Musique/Concerts/2026"
WHERE date >= date(today)
SORT date ASC
```

## Guidelines for Copilot

### When Creating New Files

1. **Always use absolute paths** starting from `/home/runner/work/obsidian-main-vault/obsidian-main-vault`
2. **Use templates** from `_templates/` directories
3. **Maintain frontmatter consistency** - all fields must match schema
4. **Include Dataview queries** in entity pages for automatic relationships
5. **Follow naming convention**: `YYYY-MM-DD - Event.md` for concerts

### When Modifying Existing Files

1. **Preserve existing content** unless explicitly asked to change
2. **Keep Dataview queries intact** - they're essential for relationships
3. **Update statistics** when adding new concerts
4. **Maintain chronological order** in concert listings

### Code Style

1. **Markdown**: Use emoji icons consistently (🎸 for concerts, 🎤 for groups, etc.)
2. **YAML**: Use lowercase with hyphens (e.g., `pays-origine`, not `PaysOrigine`)
3. **Arrays**: Use JSON format in YAML: `groupes: ["Artist1", "Artist2"]`
4. **Links**: Use wiki-style links: `[[Page Name]]`

### Testing Changes

1. **Validate YAML frontmatter** - check for syntax errors
2. **Test Dataview queries** by opening in Obsidian
3. **Verify wiki links** point to existing pages
4. **Check date formats** are consistent (YYYY-MM-DD)

## Known Patterns

### Location Mapping Dictionaries

```python
VILLE_TO_PAYS = {
    "Lyon": "France",
    "Paris": "France",
    "Tilburg": "Pays-Bas",
    "Milan": "Italie",
    # ... see scripts for complete list
}

SALLE_TO_VILLE = {
    "Brin de Zinc": "Lyon",
    "L'Olympia": "Paris",
    "Poppodium 013": "Tilburg",
    # ... see scripts for complete list
}

FESTIVAL_TO_VILLE = {
    "Hellfest": "Clisson",
    "Jazz à Vienne": "Vienne",
    "Roadburn Festival": "Tilburg",
    # ... see scripts for complete list
}
```

### Special Characters

Handle these carefully in filenames and YAML:
- Accented characters: é, è, à, ô
- Apostrophes: ' in L'Olympia
- Special symbols: ))) in Sunn O)))
- Ampersands: & in King Gizzard & The Lizard Wizard

## File Exclusions

Add to `.gitignore`:
- `/scripts/` - Python migration scripts (temporary)
- Old directories: `/Villes/`, `/Pays/`, `/Musique/Salles de concert/`
- Backup files: `*.backup`, `*.old`
- Obsidian settings: `.obsidian/`

## Documentation

- **Main README**: Root `README.md` - project overview
- **Structure Guide**: `Musique/README-STRUCTURE.md` - detailed usage
- **Verification**: `Musique/VERIFICATION-LOCALISATION.md` - location data audit

## Common Pitfalls to Avoid

1. ❌ Empty frontmatter fields - use empty string `""` or omit entirely
2. ❌ Inconsistent date formats - always use YYYY-MM-DD
3. ❌ Broken wiki links - verify target page exists
4. ❌ Missing templates - copy from `_templates/` before modifying
5. ❌ Duplicate concert files - check year subdirectory first
6. ❌ Incorrect location mappings - verify ville/pays combinations

## Automation Opportunities

### GitHub Actions

Potential workflows:
1. **Validate YAML** on PR - check frontmatter syntax
2. **Check wiki links** - verify all [[links]] resolve
3. **Update statistics** - regenerate Concerts.md sections
4. **Create missing entities** - auto-generate group/venue pages
5. **Location inference** - auto-fill ville/pays from venue/festival

### Scripts

Current scripts (in exclusion list):
- `migrate-concerts.py` - One-time migration from flat list to structured files

Potential new scripts:
- `add-concert.py` - Interactive CLI to add new concert
- `validate-vault.py` - Check data consistency
- `generate-stats.py` - Update statistics sections
- `find-missing-entities.py` - List groups/venues without pages

## Best Practices

1. **Test in Obsidian** - Always open vault and verify Dataview renders
2. **Keep backups** - Before bulk operations, backup Concerts.md
3. **Incremental changes** - Add concerts one at a time initially
4. **Verify relationships** - Check that new concerts appear in group/venue pages
5. **Update indexes** - Keep Concerts.md synchronized with individual files
