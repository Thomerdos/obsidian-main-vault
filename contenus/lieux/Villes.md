---
type: index
tags:
  - index
  - hub
---

# 🏙️ Villes

Page centrale regroupant toutes les villes visitées.

## 📋 Liste des villes

```dataview
TABLE 
  pays as "Pays",
  region as "Région"
FROM "contenus/lieux/Villes"
WHERE type = "ville"
SORT file.name ASC
```
