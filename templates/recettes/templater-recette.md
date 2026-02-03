---
type: recette
nom: "<% tp.file.title %>"
categorie: ""
temps_preparation: 
temps_cuisson: 
difficulte: ""
portions: 
ingredients: []
etapes: ""
tags:
  - recette
photo: ""
origine: ""
---

# 🍽️ <%= tp.file.title %>

## 📋 Informations

- **Catégorie**: <%= categorie %>
- **Temps de préparation**: <%= temps_preparation %> minutes
- **Temps de cuisson**: <%= temps_cuisson %> minutes
- **Difficulté**: <%= difficulte %>
- **Portions**: <%= portions %> personnes
- **Origine**: <%= origine %>

## 🥘 Ingrédients

<% ingredients.forEach(ingredient => { %>
- [[<%= ingredient %>]]
<% }); %>

## 👨‍🍳 Étapes de préparation

<%= etapes %>

## 📷 Photos

<% if (photo) { %>
![<%= tp.file.title %>](<%= photo %>)
<% } %>

## 💡 Notes & Astuces


## 🔗 Liens
