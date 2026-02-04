---
type: hub
tags:
  - hub
  - auteurs
---

# 👨‍🍳 Auteurs de Recettes

Hub central pour tous les auteurs de recettes du vault.

## 📊 Statistiques

```dataview
TABLE 
  length(rows) as "Nombre de recettes"
FROM "contenus/recettes/Fiches"
WHERE author
FLATTEN author as author_name
GROUP BY author_name
SORT length(rows) DESC
```

## 📚 Liste des Auteurs

```dataview
TABLE WITHOUT ID
  file.link as "Auteur",
  specialite as "Spécialité",
  site_web as "Site web"
FROM "contenus/recettes/Auteurs"
WHERE type = "auteur"
SORT file.name ASC
```

## 🔗 Navigation

- [[Recettes]] - Toutes les recettes
- [[Ingredients]] - Tous les ingrédients
- [[Categories]] - Catégories de recettes
