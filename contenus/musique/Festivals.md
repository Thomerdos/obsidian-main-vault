---
type: index
tags:
  - index
  - hub
---

# 🎪 Festivals

Page centrale regroupant tous les festivals.

## 📋 Liste des festivals

```dataview
TABLE 
  ville as "Ville",
  pays as "Pays",
  periode as "Période"
FROM "contenus/musique/Festivals"
WHERE type = "festival"
SORT file.name ASC
```
