---
type: recette
title: "{{title}}"
source: "{{url}}"
author: ["{{author}}"]
published: {{date:YYYY-MM-DD}}
created: {{date:YYYY-MM-DD}}
image: "{{image}}"
ingredients: []
tags:
  - recette
---

# 🍽️ {{title}}

![]({{image}})

{{description}}

## 🥘 Ingrédients

{{selector:.recipe-ingredients}}
{{selector:.ingredients}}
{{selector:[itemprop="recipeIngredient"]}}

## 👨‍🍳 Instructions

{{selector:.recipe-steps}}
{{selector:.instructions}}
{{selector:.directions}}
{{selector:[itemprop="recipeInstructions"]}}

## 🔗 Source

- [Recette originale]({{url}})

---

<!-- 
NOTES: Après avoir clippé, vérifiez les ingrédients et créez les liens wiki vers les fichiers d'ingrédients.
-->
