---
type: index
tags:
  - index
  - hub
---

# 🏛️ Salles de Concert

Page centrale regroupant toutes les salles de concert.

## 📋 Liste des salles

```dataview
TABLE 
  ville as "Ville",
  pays as "Pays",
  capacite as "Capacité"
FROM "contenus/musique/Salles"
WHERE type = "salle"
SORT file.name ASC
```
