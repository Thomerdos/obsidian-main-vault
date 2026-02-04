---
type: recette
title: "<% tp.file.title %>"
source: ""
author: []
published: 
created: <% tp.date.now("YYYY-MM-DD") %>
image: ""
type_cuisine: ""
origine: ""
regime: []
saison: []
temps_preparation: 
temps_cuisson: 
ingredients: []
tags:
  - recette
---

# 🍽️ <%= tp.file.title %>

<% if (tp.frontmatter.image) { %>
![<%= tp.file.title %>](<%= tp.frontmatter.image %>)
<% } %>

## 📋 Informations

- **Type de cuisine**: <%= tp.frontmatter.type_cuisine || "" %>
- **Origine**: <%= tp.frontmatter.origine || "" %>
- **Régime**: <%= tp.frontmatter.regime ? tp.frontmatter.regime.join(', ') : "" %>
- **Saison**: <%= tp.frontmatter.saison ? tp.frontmatter.saison.join(', ') : "" %>
- **Temps de préparation**: <%= tp.frontmatter.temps_preparation %> minutes
- **Temps de cuisson**: <%= tp.frontmatter.temps_cuisson %> minutes

## 🥘 Ingrédients

<%* 
// List ingredients with wiki links
if (tp.frontmatter.ingredients && tp.frontmatter.ingredients.length > 0) {
  tp.frontmatter.ingredients.forEach(ingredient => {
    tR += `- [[${ingredient}]]\n`;
  });
} else {
  tR += "<!-- Add ingredients here -->\n";
}
%>

## 👨‍🍳 Instructions

<!-- Add step-by-step instructions here -->

## 📷 Photos

<% if (tp.frontmatter.image) { %>
![<%= tp.file.title %>](<%= tp.frontmatter.image %>)
<% } %>

## 💡 Notes & Astuces


## 🔗 Liens

<% if (tp.frontmatter.source) { %>
- [Source originale](<%= tp.frontmatter.source %>)
<% } %>
