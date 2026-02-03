---
type: index
tags:
  - index
  - hub
---

# 🥕 Ingrédients

Page centrale regroupant tous les ingrédients.

## 📋 Liste des ingrédients

```dataview
TABLE 
  categorie as "Catégorie",
  saison as "Saison"
FROM "contenus/recettes"
WHERE type = "ingredient"
SORT file.name ASC
```
