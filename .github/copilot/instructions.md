# GitHub Copilot Instructions for Obsidian Concert Vault

## Repository Context

This is an Obsidian vault for managing concert attendance data and recipes with structured markdown files, YAML frontmatter, and Dataview queries using a **hub/star graph structure**.

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
│       ├── Auteurs.md            # HUB pour tous les auteurs
│       ├── Ingredients.md        # HUB pour tous les ingrédients
│       ├── Categories.md         # HUB pour les catégories
│       ├── Recherche-par-ingredients.md  # Recherche interactive
│       ├── Fiches/               # Fichiers de recettes (60+ total)
│       ├── Ingredients/          # Pages d'ingrédients
│       └── Auteurs/              # Pages d'auteurs
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

### Recette (Recipe)
```yaml
type: recette
title: "Nom de la recette"
source: "https://..."
author:
  - "[[Nom Auteur]]"
published: 2024-01-15
created: 2026-02-04
image: "https://..."
type_cuisine: "Italienne"
origine: "Toscane"
regime:
  - "végétarien"
saison:
  - "été"
temps_preparation: 30
temps_cuisson: 45
ingredients:
  - tomate
  - basilic
  - mozzarella
tags:
  - recette
```

**Important pour les recettes**:
- `ingredients`: liste normalisée (singulier, minuscules, sans article)
- `author`: liste de liens wiki vers pages d'auteurs: `"[[Chef Simon]]"`
- Sections en français mais propriétés en anglais pour cohérence

### Ingredient
```yaml
type: ingredient
nom: "tomate"
categorie: "légume"
recettes: []
allergenes: []
saison:
  - "été"
tags:
  - ingredient
```

### Auteur (Recipe Author)
```yaml
type: auteur
nom: "Chef Simon"
parent: "[[Auteurs]]"          # REQUIRED
site_web: "https://..."
specialite:
  - "Cuisine française"
  - "Pâtisserie"
tags:
  - auteur
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

### Recipe Page - Show Ingredients with Links
```markdown
## Ingrédients

- 500g [[tomate]]
- 2 [[oignon]]
- 3 gousses [[ail]]
- 100g [[parmesan]]
```

### Ingredient Page - Show All Recipes Using It
```dataview
TABLE WITHOUT ID
  file.link as "Recette",
  temps_preparation as "Préparation (min)",
  temps_cuisson as "Cuisson (min)",
  type_cuisine as "Cuisine"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, "tomate")
SORT file.name ASC
```

### Author Page - Show All Their Recipes
```dataview
TABLE WITHOUT ID
  file.link as "Recette",
  type_cuisine as "Cuisine",
  temps_preparation as "Préparation (min)"
FROM "contenus/recettes/Fiches"
WHERE contains(author, this.file.link)
SORT file.name ASC
```

### Search Recipes by Multiple Ingredients
```dataview
TABLE 
  ingredients as "Ingrédients",
  type_cuisine as "Cuisine"
FROM "contenus/recettes/Fiches"
WHERE 
  contains(ingredients, "tomate") AND
  contains(ingredients, "basilic")
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

### Adding a New Recipe

1. Create file: `contenus/recettes/Fiches/Nom de la Recette.md`
2. Use recipe template with English property names but French sections
3. List ingredients in `ingredients: []` (normalized: singular, lowercase)
4. Link authors: `author: ["[[Chef Name]]"]`
5. Add wiki links in ingredient section: `- 500g [[tomate]]`
6. Recipe appears automatically in ingredient and author pages

### Adding a New Author

1. Create file: `contenus/recettes/Auteurs/Author Name.md`
2. **MUST include** `parent: "[[Auteurs]]"`
3. Fill in `site_web` and `specialite`
4. Recipes will automatically appear via Dataview

### Search Recipes by Ingredients

**Method 1: Obsidian**
- Use `contenus/recettes/Recherche-par-ingredients.md`
- Edit the ingredient list in the DataviewJS query

**Method 2: Command Line**
```bash
# Find recipes with these ingredients
python3 tools/search-recipes-by-ingredients.py tomate oignon ail

# Require all ingredients
python3 tools/search-recipes-by-ingredients.py --exact tomate basilic mozzarella

# Show what's missing
python3 tools/search-recipes-by-ingredients.py --show-missing poulet riz
```

## Code Style Guidelines

### YAML
- Lowercase with hyphens: `pays-origine`, not `PaysOrigine`
- Wiki links in quotes: `"[[Page Name]]"`
- Arrays for multiple values: `genre: ["[[Genre1]]", "[[Genre2]]"]`
- **Property names in English** for consistency across the vault

### Markdown
- Use emoji icons: 🎸 (concerts), 🎤 (groups), 🏛️ (venues), 🎪 (festivals), 🍽️ (recipes), 🥕 (ingredients), 👨‍🍳 (authors)
- Use wiki links: `[[Page Name]]`
- Date format: `YYYY-MM-DD`

### Recipe-specific
- Ingredient names: normalized (singular, lowercase, no articles)
  - ✅ `tomate`, `oignon`, `ail`
  - ❌ `tomates`, `Oignon`, `de l'ail`
- Ingredient list in recipe: include quantity + wiki link
  - ✅ `- 500g [[tomate]]`
  - ❌ `- [[500g tomate]]`
- Section headers in French: `## Ingrédients`, `## Instructions`, `## Notes & Astuces`

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
- `migrate-recipes.py` - Recipe migration and ingredient extraction
- `search-recipes-by-ingredients.py` - Find recipes by available ingredients

**Recipe Tools Usage**:
```bash
# Migrate/update recipes
python3 tools/migrate-recipes.py --dry-run

# Search by ingredients
python3 tools/search-recipes-by-ingredients.py tomate oignon ail

# With options
python3 tools/search-recipes-by-ingredients.py --exact --show-missing poulet riz
```

## Common Pitfalls to Avoid

1. ❌ Missing `parent` field in entities (except concerts and recipes)
2. ❌ Wiki links without quotes in YAML: `genre: [[Metal]]` → Use `"[[Metal]]"`
3. ❌ Including obsolete computed fields like `concerts: []`
4. ❌ Wrong hub page name: `parent: "[[Genre]]"` → Use `"[[Genres]]"` (plural)
5. ❌ Trying to run removed Python scripts
6. ❌ Creating `.base` schema files (no longer used)
7. ❌ Non-normalized ingredients: `tomates` → Use `tomate`
8. ❌ Including quantity in ingredient name: `ingredients: ["500g tomate"]` → Use `["tomate"]`

## Best Practices

1. **Always use hub pages** - Don't skip the `parent` field (except for concerts and recipes)
2. **Test in Obsidian** - Verify Dataview renders correctly
3. **Keep wiki links quoted** - Prevents YAML parsing errors
4. **Check Graph View** - Should show clean star patterns
5. **Use Dataview** - Let queries handle relationship display
6. **English property names** - Use `author`, `created`, `published` for consistency
7. **French content** - Section headers and content in French: `## Ingrédients`, `## Instructions`
8. **Normalize ingredients** - Always singular, lowercase, no articles

---

**Remember**: 
- Concert vault uses native Obsidian features only. No Python scripts needed for relationships!
- Recipe system uses Python tools for migration and search, but relationships work via Dataview
- Property names in English, content and section headers in French
