# 📋 Schema Documentation

This document describes all entity types (schemas) in the relational database system.

## Overview

The vault uses 7 entity types, each defined by a `.base` schema file in the `.bases/` directory:

1. **Concert** (🎸) - Individual concert events
2. **Groupe** (🎤) - Musical artists/bands
3. **Genre** (🎵) - Musical genres
4. **Salle** (🏛️) - Concert venues
5. **Festival** (🎪) - Music festivals
6. **Ville** (🏙️) - Cities
7. **Pays** (🌍) - Countries

## Schema Files

### Concert Schema (`.bases/concert.base`)

Represents individual concert events.

**Required Fields:**
- `date` (date): Concert date in YYYY-MM-DD format
- `ville` (link): City where concert took place
- `pays` (link): Country where concert took place

**Optional Fields:**
- `groupes` (list[link]): List of artists/bands that performed
- `salle` (link): Venue where concert took place
- `festival` (link): Festival (if part of a festival)
- `rating` (number): Personal rating

**Relations:**
- `concert-groupes` → `Musique/Groupes/` (list, bidirectional)
- `concert-salle` → `Musique/Salles/` (single, bidirectional)
- `concert-festival` → `Musique/Festivals/` (single, bidirectional)
- `concert-ville` → `Lieux/Villes/` (single, bidirectional)
- `concert-pays` → `Lieux/Pays/` (single, bidirectional)

**Auto Relations:**
- `concert-same-night`: Groups that played on the same date
- `concert-same-venue`: Concerts at the same venue

**Example Frontmatter:**
```yaml
---
type: concert
date: 2024-07-18
groupes: ["Heilung", "Wardruna"]
salle: Le Sucre
festival: 
ville: Lyon
pays: France
rating: 5
tags:
  - concert
---
```

### Groupe Schema (`.bases/groupe.base`)

Represents musical artists and bands.

**Required Fields:**
- `name` (string): Artist/band name

**Optional Fields:**
- `genre` (list[link]): Musical genres
- `pays-origine` (link): Country of origin
- `formation` (number): Year formed
- `site-web` (url): Official website

**Relations:**
- `groupe-concerts` → `Musique/Concerts/` (list)
- `groupe-genres` → `Musique/Genres/` (list, bidirectional)
- `groupe-origine` → `Lieux/Pays/` (single)

**Auto Relations:**
- `groupe-similar`: Similar artists (Jaccard similarity ≥ 0.3 on genres/concerts)
- `groupe-tour-together`: Artists that toured together (3+ shared concerts)

**Example Frontmatter:**
```yaml
---
type: groupe
genre: ["Progressive Rock", "Symphonic Rock"]
pays-origine: France
formation: 1969
site-web: http://www.ange-officiel.com
tags:
  - groupe
---
```

### Genre Schema (`.bases/genre.base`)

Represents musical genres with hierarchical relationships.

**Required Fields:**
- `name` (string): Genre name

**Optional Fields:**
- `description` (text): Genre description

**Relations:**
- `genre-parent` → `Musique/Genres/` (single, bidirectional)
- `genre-children` → `Musique/Genres/` (list)
- `genre-related` → `Musique/Genres/` (list, bidirectional)
- `genre-groupes` → `Musique/Groupes/` (list)

**Auto Relations:**
- `genre-co-occurrence`: Genres that frequently appear together (3+ shared concerts)

**Example Frontmatter:**
```yaml
---
type: genre
description: Heavy, slow, and doom-laden metal music
genre-parent: Metal
genre-children: ["Funeral Doom", "Stoner Doom"]
genre-related: ["Sludge Metal", "Drone Metal"]
tags:
  - genre
---
```

### Salle Schema (`.bases/salle.base`)

Represents concert venues.

**Required Fields:**
- `name` (string): Venue name
- `ville` (link): City where venue is located
- `pays` (link): Country where venue is located

**Optional Fields:**
- `capacite` (number): Venue capacity
- `adresse` (text): Street address

**Relations:**
- `salle-concerts` → `Musique/Concerts/` (list)
- `salle-ville` → `Lieux/Villes/` (single, bidirectional)
- `salle-pays` → `Lieux/Pays/` (single)

**Auto Relations:**
- `salle-nearby`: Venues in the same city

**Example Frontmatter:**
```yaml
---
type: salle
ville: Lyon
pays: France
capacite: 800
adresse: 13 Montée de la Grande Côte, 69001 Lyon
tags:
  - salle
---
```

### Festival Schema (`.bases/festival.base`)

Represents music festivals.

**Required Fields:**
- `name` (string): Festival name
- `ville` (link): City where festival takes place
- `pays` (link): Country where festival takes place

**Optional Fields:**
- `periode` (text): Typical time period (e.g., "Juin", "Summer")
- `editions-vues` (list[number]): Years attended

**Relations:**
- `festival-editions` → `Musique/Concerts/` (list)
- `festival-ville` → `Lieux/Villes/` (single, bidirectional)
- `festival-pays` → `Lieux/Pays/` (single)

**Auto Relations:**
- `festival-concurrent`: Festivals with overlapping dates

**Example Frontmatter:**
```yaml
---
type: festival
ville: Vienne
pays: France
periode: Juin-Juillet
editions-vues: [2024, 2023, 2022]
tags:
  - festival
---
```

### Ville Schema (`.bases/ville.base`)

Represents cities.

**Required Fields:**
- `name` (string): City name
- `pays` (link): Country

**Optional Fields:**
- `region` (text): Region or state

**Relations:**
- `ville-pays` → `Lieux/Pays/` (single, bidirectional)
- `ville-salles` → `Musique/Salles/` (list)
- `ville-festivals` → `Musique/Festivals/` (list)
- `ville-concerts` → `Musique/Concerts/` (list)

**Example Frontmatter:**
```yaml
---
type: ville
pays: France
region: Auvergne-Rhône-Alpes
tags:
  - ville
---
```

### Pays Schema (`.bases/pays.base`)

Represents countries.

**Required Fields:**
- `name` (string): Country name
- `continent` (string): Continent

**Relations:**
- `pays-villes` → `Lieux/Villes/` (list)
- `pays-salles` → `Musique/Salles/` (list)
- `pays-festivals` → `Musique/Festivals/` (list)
- `pays-concerts` → `Musique/Concerts/` (list)
- `pays-groupes-origine` → `Musique/Groupes/` (list)

**Example Frontmatter:**
```yaml
---
type: pays
continent: Europe
tags:
  - pays
---
```

## Field Types

- **string**: Text value
- **text**: Long text (multiple lines)
- **number**: Numeric value
- **date**: Date in YYYY-MM-DD format
- **url**: Web URL
- **link**: Link to another note (wiki-style: `[[Note Name]]`)
- **list[type]**: Array of values of a specific type

## Relation Types

### Bidirectional Relations

These relations are automatically maintained in both directions:
- When you link Concert → Groupe, the Groupe automatically gets Concert in its `groupe-concerts` field
- When you add Ville → Pays, the Pays automatically gets Ville in its `pays-villes` field

### Unidirectional Relations

Some relations are one-way only:
- `groupe-concerts`: Maintained only from Concert to Groupe
- `salle-concerts`: Maintained only from Concert to Salle

### Auto Relations

Automatically calculated based on shared attributes:
- **Jaccard Similarity**: Measures overlap in genres and concerts
- **Co-occurrence**: Identifies entities that frequently appear together
- **Proximity**: Groups entities by shared locations

## Using Schemas

### For Users

When creating notes:
1. Add `type: <entity_type>` to frontmatter
2. Fill in required fields
3. Add optional fields as needed
4. Use `[[Link]]` format for relations

### For Developers

To add a new entity type:
1. Create `.bases/<type>.base` schema file
2. Define required/optional fields
3. Define relations and auto-relations
4. Update migration scripts if needed

## Validation

Use `tools/validate-schema.py` to check:
- All required fields are present
- Field types are correct
- Links point to existing notes
- Bidirectional relations are synchronized

## See Also

- [RELATIONS.md](RELATIONS.md) - Visual relationship map
- [GRAPH-GUIDE.md](GRAPH-GUIDE.md) - Using Graph View
- [README-RELATIONS.md](../README-RELATIONS.md) - User guide
