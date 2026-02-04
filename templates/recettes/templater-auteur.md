---
type: auteur
nom: "<% tp.file.title %>"
parent: "[[Auteurs]]"
site_web: ""
specialite: []
tags:
  - auteur
---

# 👨‍🍳 <%= tp.file.title %>

## 📋 Informations

- **Site web**: <%= tp.frontmatter.site_web || "" %>
- **Spécialité**: <%= tp.frontmatter.specialite ? tp.frontmatter.specialite.join(', ') : "" %>

## 🍽️ Recettes

```dataview
TABLE WITHOUT ID
  file.link as "Recette",
  type_cuisine as "Cuisine",
  temps_preparation as "Préparation (min)",
  temps_cuisson as "Cuisson (min)"
FROM "contenus/recettes/Fiches"
WHERE contains(author, this.file.link) OR contains(author, this.file.name)
SORT file.name ASC
```

## 💡 Notes


## 🔗 Liens
