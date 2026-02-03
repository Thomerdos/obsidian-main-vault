---
type: categorie-recette
nom: "<% tp.file.title %>"
description: ""
recettes: []
parent: ""
tags:
  - categorie-recette
---

# 📚 <%= tp.file.title %>

## 📋 Description

<%= description %>

## 🍽️ Recettes de cette catégorie

<% recettes.forEach(recette => { %>
- [[<%= recette %>]]
<% }); %>

## 📂 Sous-catégories

<% if (parent) { %>
Catégorie parent: [[<%= parent %>]]
<% } %>

## 🔗 Liens
