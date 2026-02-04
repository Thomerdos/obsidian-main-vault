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
  source as "Source"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, this.file.link)
SORT file.name ASC
```

## 💡 Notes


## 🔗 Liens
