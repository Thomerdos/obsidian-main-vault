# 🔗 Obsidian Main Vault - Hub/Star Graph Structure

Complete guide to the hub/star graph structure using native Obsidian wiki links and Dataview queries.

## 🎯 Overview

This vault uses a **hub/star topology** for clean graph visualization:

✅ **Hub pages** act as central nodes for each entity type
✅ **Native wiki links** connect entities
✅ **Dataview queries** provide dynamic relationship views
✅ **No external scripts** needed - everything is native Obsidian
✅ **Clean graph visualization** with star patterns
✅ **Multi-domain support** for music, locations, and recipes

## 🌟 Hub/Star Architecture

### What is Hub/Star?

The hub/star topology means each entity type has a central "hub" page that all entities of that type link to:

```
       Hub Page
          │
    ┌─────┼─────┐
    │     │     │
  Item1 Item2 Item3
```

This creates clear visual clusters in the Graph View instead of a tangled mess.

## 📋 Hub Pages

### Music Domain

#### `contenus/musique/Genres.md`
Central hub for all musical genres.

**Links to**: All genre pages
**Features**: Dataview table showing all genres with artist counts

#### `contenus/musique/Groupes.md`
Central hub for all artists and bands.

**Links to**: All artist/band pages
**Features**: Dataview table with genres, countries, and formation dates

#### `contenus/musique/Salles.md`
Central hub for all concert venues.

**Links to**: All venue pages
**Features**: Dataview table with locations and capacities

#### `contenus/musique/Festivals.md`
Central hub for all festivals.

**Links to**: All festival pages
**Features**: Dataview table with locations and typical periods

### Location Domain

#### `contenus/lieux/Villes.md`
Central hub for all cities.

**Links to**: All city pages
**Features**: Dataview table with countries and regions

#### `contenus/lieux/Pays.md`
Central hub for all countries.

**Links to**: All country pages
**Features**: Dataview table with continents

### Recipe Domain

#### `contenus/recettes/Ingredients.md`
Central hub for all ingredients.

**Links to**: All ingredient pages
**Features**: Dataview table with categories and seasons

#### `contenus/recettes/Categories.md`
Central hub for recipe categories.

**Links to**: All category pages
**Features**: Dataview list of all categories

## 🔗 Entity Relationships

### Frontmatter Structure

Each entity has a `parent` field linking to its hub:

```yaml
---
type: groupe
parent: "[[Groupes]]"
genre:
  - "[[Progressive Rock]]"
  - "[[Metal]]"
pays-origine: "[[France]]"
tags:
  - groupe
---
```

### Relationship Types

#### Direct Links (Parent)
Every entity links to its hub via `parent: "[[Hub Name]]"`:
- Genres → Genres hub
- Groupes → Groupes hub
- Salles → Salles hub
- Festivals → Festivals hub
- Villes → Villes hub
- Pays → Pays hub

#### Cross-Domain Links
Entities link to related entities via wiki links:
- **Concerts** → Artists, Venues, Festivals, Cities, Countries
- **Artists** → Genres, Origin Country
- **Genres** → Related Genres, Parent/Child Genres
- **Venues** → Cities, Countries
- **Festivals** → Cities, Countries
- **Cities** → Countries

## �� Dataview Queries

### Hub Page Queries

#### Genre Hub Query
```dataview
TABLE WITHOUT ID
  file.link as "Genre",
  length(filter(pages("contenus/musique/Groupes"), (p) => contains(p.genre, file.name))) as "Artistes"
FROM "contenus/musique/Genres"
WHERE type = "genre"
SORT file.name ASC
```

#### Artist Hub Query
```dataview
TABLE 
  genre as "Genres",
  pays-origine as "Pays",
  formation as "Formation"
FROM "contenus/musique/Groupes"
WHERE type = "groupe"
SORT file.name ASC
```

### Entity Page Queries

#### Artist Page - Concert History
```dataview
TABLE date as "Date", salle as "Salle", ville as "Ville"
FROM "contenus/musique/Concerts"
WHERE contains(groupes, this.file.name)
SORT date DESC
```

#### Genre Page - Artists in Genre
```dataview
TABLE pays-origine as "Pays", formation as "Formation"
FROM "contenus/musique/Groupes"
WHERE contains(genre, this.file.name)
SORT file.name ASC
```

#### Venue Page - Concerts at Venue
```dataview
TABLE date as "Date", groupes as "Artistes"
FROM "contenus/musique/Concerts"
WHERE contains(salle, this.file.name)
SORT date DESC
```

## 🎨 Graph View Configuration

### Expected Topology

After migration, your Graph View will show star patterns with hubs at center.

### Graph Filters

Use these filters to focus on specific parts:

```
# Show only music domain
path:contenus/musique

# Show only hubs
tag:#hub

# Show specific entity type
tag:#concert OR tag:#groupe

# Show specific year
path:contenus/musique/Concerts/2024
```

---

**See [README.md](README.md) for complete vault documentation**
