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

- **Catégorie**: <%= categorie %>
- **Saison**: <%= saison.join(', ') %>
- **Allergènes**: <%= allergenes.join(', ') %>

## 🍽️ Utilisé dans les recettes

<% recettes.forEach(recette => { %>
- [[<%= recette %>]]
<% }); %>

## 💡 Notes


## 🔗 Liens
