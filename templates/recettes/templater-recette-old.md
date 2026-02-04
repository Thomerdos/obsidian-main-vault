---
type: recette
title: "<% tp.file.title %>"
source: ""
author: []
published: 
created: <% tp.date.now("YYYY-MM-DD") %>
image: ""
ingredients: []
tags:
  - recette
---

# 🍽️ <%= tp.file.title %>

<% if (tp.frontmatter.image) { %>
![<%= tp.file.title %>](<%= tp.frontmatter.image %>)
<% } %>

## 🥘 Ingrédients

<%* 
// Afficher les ingrédients avec liens wiki
if (tp.frontmatter.ingredients && tp.frontmatter.ingredients.length > 0) {
  tp.frontmatter.ingredients.forEach(ingredient => {
    tR += `- [[${ingredient}]]\n`;
  });
} else {
  tR += "<!-- Ajouter les ingrédients ici -->\n";
}
%>

## 👨‍🍳 Instructions

<!-- Ajouter les instructions étape par étape ici -->

## 🔗 Source

<% if (tp.frontmatter.source) { %>
- [Recette originale](<%= tp.frontmatter.source %>)
<% } %>

