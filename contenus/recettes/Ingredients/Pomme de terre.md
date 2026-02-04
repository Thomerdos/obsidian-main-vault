---
type: ingredient
nom: pomme de terre
categorie: ''
recettes:
- Pommes sautées à cru
tags:
- ingredient
---

# 🥕 Pomme de terre

## 📋 Informations

- **Catégorie**: 
- **Saison**: 
- **Allergènes**: 

## 🍽️ Utilisé dans les recettes

```dataview
TABLE WITHOUT ID
  file.link as "Recette",
  source as "Source",
  temps_preparation as "Préparation",
  temps_cuisson as "Cuisson"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, this.file.link)
SORT file.name ASC
```

## 💡 Notes


## 🔗 Liens
