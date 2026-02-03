---
type: index
tags:
  - index
  - hub
---

# 📚 Catégories de Recettes

Page centrale regroupant les catégories de recettes.

## 📋 Liste des catégories

```dataview
LIST
FROM "contenus/recettes"
WHERE type = "categorie-recette"
SORT file.name ASC
```
