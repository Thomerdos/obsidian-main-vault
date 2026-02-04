---
type: ingredient
nom: "<% tp.file.title %>"
categorie: ""
recettes: []
allergenes: []
saison: []
tags:
  - ingredient
---

# 🥕 <%= tp.file.title %>

## 📋 Informations

- **Catégorie**: <%= tp.frontmatter.categorie || "" %>
- **Saison**: <%= tp.frontmatter.saison ? tp.frontmatter.saison.join(', ') : "" %>
- **Allergènes**: <%= tp.frontmatter.allergenes ? tp.frontmatter.allergenes.join(', ') : "" %>

## 🍽️ Utilisé dans les recettes

```dataview
TABLE WITHOUT ID
  file.link as "Recette",
  temps_preparation as "Préparation (min)",
  temps_cuisson as "Cuisson (min)",
  type_cuisine as "Cuisine",
  regime as "Régime"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, "<% tp.file.title.toLowerCase() %>")
SORT file.name ASC
```

## 💡 Notes


## 🔗 Liens
