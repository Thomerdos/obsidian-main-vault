---
type: index
tags:
  - index
  - hub
---

# 🎵 Genres Musicaux

Page centrale regroupant tous les genres musicaux.

## 📋 Liste des genres

```dataview
TABLE WITHOUT ID
  file.link as "Genre",
  length(filter(pages("contenus/musique/Groupes"), (p) => contains(p.genre, file.name))) as "Artistes"
FROM "contenus/musique/Genres"
WHERE type = "genre"
SORT file.name ASC
```

## 🔗 Navigation

- [[Groupes]] - Tous les artistes
- [[Concerts]] - Historique des concerts
