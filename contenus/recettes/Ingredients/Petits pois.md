---
type: ingredient
nom: petits pois
categorie: ''
recettes:
- Petits pois à la française, une recette classique délicieuse
tags:
- ingredient
---

# 🥕 Petits pois

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
