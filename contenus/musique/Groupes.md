---
type: index
tags:
  - index
  - hub
---

# 🎤 Groupes & Artistes

Page centrale regroupant tous les groupes et artistes.

## 📋 Liste des artistes

```dataview
TABLE 
  genre as "Genres",
  pays-origine as "Pays",
  formation as "Formation"
FROM "contenus/musique/Groupes"
WHERE type = "groupe"
SORT file.name ASC
```

## 🔗 Navigation

- [[Genres]] - Genres musicaux
- [[Concerts]] - Historique des concerts
