---
type: recette
title: "{{title}}"
source: "{{url}}"
author: ["{{author}}"]
published: {{date:YYYY-MM-DD}}
created: {{date:YYYY-MM-DD}}
image: "{{image}}"
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

![]({{image}})

{{description}}

## Ingrédients

{{selector:.recipe-ingredients}}
{{selector:.ingredients}}
{{selector:[itemprop="recipeIngredient"]}}

## Instructions

{{selector:.recipe-steps}}
{{selector:.instructions}}
{{selector:.directions}}
{{selector:[itemprop="recipeInstructions"]}}

## Notes

<!-- Add any personal notes here -->

## Liens

- [Source originale]({{url}})

---

<!-- 
NOTES D'UTILISATION:
1. Après avoir clippé cette recette, vérifiez et complétez les métadonnées frontmatter
2. Utilisez le script migrate-recipes.py pour extraire et structurer les ingrédients:
   python3 tools/migrate-recipes.py --recipe "{{title}}"
3. Ou utilisez le template templater-post-webclipper.md pour post-traitement manuel
4. Les ingrédients seront extraits et normalisés automatiquement
5. Les pages d'ingrédients seront créées automatiquement si elles n'existent pas

SÉLECTEURS CSS PAR SITE:
- journaldesfemmes.fr: .recipe-ingredients-list, .recipe-steps
- marmiton.org: .recipe-ingredients, .recipe-steps  
- ricardocuisine.com: .recipe__ingredients, .recipe__step
- 750g.com: .recipe-ingredient, .recipe-step-list__item
- papillesetpupilles.fr: .ingredients, .instructions
-->
