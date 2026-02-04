---
type: recherche
tags:
  - recherche
  - recettes
---

# 🔍 Recherche de Recettes par Ingrédients

Trouvez des recettes en fonction des ingrédients que vous avez sous la main.

## 🎯 Comment utiliser cette page

1. **Modifier la liste ci-dessous** avec vos ingrédients disponibles
2. **Regarder les résultats** dans les sections automatiques
3. **Cliquer sur une recette** pour voir la recette complète

## 📝 Vos Ingrédients Disponibles

Modifiez cette liste avec vos ingrédients (un par ligne, sans tiret):

```
tomate
oignon
ail
basilic
```

## 🍽️ Méthode 1: Recettes contenant TOUS ces ingrédients

Pour trouver les recettes qui utilisent **tous** vos ingrédients, utilisez cette requête Dataview (remplacez les ingrédients):

```dataview
TABLE 
  ingredients as "Tous les ingrédients",
  type_cuisine as "Cuisine",
  temps_preparation as "Préparation (min)"
FROM "contenus/recettes/Fiches"
WHERE 
  contains(ingredients, "tomate") AND
  contains(ingredients, "oignon") AND
  contains(ingredients, "ail") AND
  contains(ingredients, "basilic")
SORT file.name ASC
```

## 🎨 Méthode 2: Recettes contenant AU MOINS UN de ces ingrédients

Pour trouver les recettes qui utilisent **au moins un** de vos ingrédients:

```dataview
TABLE 
  ingredients as "Ingrédients",
  type_cuisine as "Cuisine",
  temps_preparation as "Préparation (min)"
FROM "contenus/recettes/Fiches"
WHERE 
  contains(ingredients, "tomate") OR
  contains(ingredients, "oignon") OR
  contains(ingredients, "ail") OR
  contains(ingredients, "basilic")
SORT file.name ASC
```

## 🔢 Méthode 3: Score de correspondance (plus de correspondances = mieux)

Cette requête montre combien de vos ingrédients sont utilisés dans chaque recette:

```dataviewjs
// Liste de vos ingrédients disponibles
const mesIngredients = ["tomate", "oignon", "ail", "basilic"];

// Récupérer toutes les recettes
const recettes = dv.pages('"contenus/recettes/Fiches"')
  .where(p => p.ingredients && p.ingredients.length > 0)
  .map(p => {
    // Compter combien d'ingrédients correspondent
    const correspondances = mesIngredients.filter(ing => 
      p.ingredients.some(recIng => recIng.toLowerCase().includes(ing.toLowerCase()))
    );
    
    return {
      recette: p.file.link,
      score: correspondances.length,
      ingredients_matches: correspondances.join(", "),
      total_ingredients: p.ingredients.length,
      cuisine: p.type_cuisine,
      temps: p.temps_preparation
    };
  })
  .filter(r => r.score > 0)
  .sort(r => r.score, "desc");

// Afficher le tableau
dv.table(
  ["Recette", "Score", "Ingrédients trouvés", "Total ingrédients", "Cuisine", "Temps (min)"],
  recettes.map(r => [
    r.recette,
    r.score + "/" + mesIngredients.length,
    r.ingredients_matches,
    r.total_ingredients,
    r.cuisine || "-",
    r.temps || "-"
  ])
);
```

## 💡 Astuces

1. **Pour modifier la recherche**: Éditez la liste `mesIngredients` dans la requête DataviewJS ci-dessus
2. **Format des ingrédients**: Utilisez la forme normalisée (singulier, minuscules): `tomate` pas `tomates`
3. **Recettes partielles**: La Méthode 3 est idéale - elle vous montre les recettes même si vous n'avez pas tous les ingrédients
4. **Ingrédients de base**: Vous pouvez exclure sel, poivre, huile de la recherche car ils sont souvent présents

## 🛠️ Script Python pour recherche avancée

Pour une recherche plus puissante depuis la ligne de commande:

```bash
# Trouver des recettes avec ces ingrédients
python3 tools/search-recipes-by-ingredients.py tomate oignon ail

# Avec score minimum
python3 tools/search-recipes-by-ingredients.py --min-score 2 tomate oignon ail basilic

# Afficher les ingrédients manquants
python3 tools/search-recipes-by-ingredients.py --show-missing tomate oignon
```

## 📚 Exemples de Recherches Courantes

### Recettes avec tomates et basilic
```dataview
LIST FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, "tomate") AND contains(ingredients, "basilic")
SORT file.name ASC
```

### Recettes végétariennes avec courgette
```dataview
LIST FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, "courgette") AND contains(regime, "végétarien")
SORT file.name ASC
```

### Recettes rapides (< 30 min) avec poulet
```dataview
TABLE temps_preparation as "Temps", type_cuisine as "Cuisine"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, "poulet") AND temps_preparation < 30
SORT temps_preparation ASC
```

## 🔗 Navigation

- [[Ingredients]] - Liste de tous les ingrédients
- [[Recettes]] - Toutes les recettes
- [[Categories]] - Par catégorie de cuisine
