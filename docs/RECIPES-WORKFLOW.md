# Guide du Workflow des Recettes

Ce guide explique le système complet de gestion des recettes dans le vault Obsidian, comment l'utiliser, et comment en tirer le meilleur parti.

## 📐 Architecture du système

### Structure des fichiers

```
contenus/recettes/
├── Categories.md           # Hub des catégories
├── Ingredients.md          # Hub des ingrédients (à créer)
├── Fiches/                 # Toutes les recettes
│   ├── Boeuf bourguignon.md
│   ├── Piperade basque.md
│   └── ...
└── Ingredients/            # Pages d'ingrédients individuels
    ├── Oignon.md
    ├── Tomate.md
    └── ...
```

### Propriétés frontmatter

Chaque recette utilise un frontmatter structuré:

```yaml
---
type: recette
title: "Nom de la recette"
source: "https://source-url.com"
author: ["Auteur"]
published: 2024-01-15
created: 2024-01-20
image: "https://image-url.jpg"
type_cuisine: "Italienne"      # Type de cuisine
origine: "Toscane"              # Région/pays d'origine
regime: ["végétarien"]          # Liste des régimes
saison: ["été", "automne"]      # Saisons appropriées
temps_preparation: 30           # Minutes
temps_cuisson: 45               # Minutes
ingredients:                    # Liste des ingrédients normalisés
  - tomate
  - oignon
  - ail
  - basilic
tags:
  - recette
---
```

## 🎯 Méthodes d'ajout de recettes

### Méthode 1: Webclipper (Recommandé pour les recettes web)

**Avantages**: Rapide, capture automatique des images et du contenu

1. Installez l'extension Obsidian Web Clipper
2. Naviguez vers une recette en ligne
3. Cliquez sur l'icône Web Clipper
4. Sélectionnez le template "Recette"
5. Sauvegardez dans `contenus/recettes/Fiches/`
6. Post-traitez avec le script: `python3 tools/migrate-recipes.py --recipe "Nom"`

**Guide détaillé**: [WEBCLIPPER-RECETTES.md](WEBCLIPPER-RECETTES.md)

### Méthode 2: Template Templater (Pour création manuelle)

**Avantages**: Contrôle total, bon pour les recettes personnelles

1. Créez une nouvelle note dans `contenus/recettes/Fiches/`
2. Utilisez le template `templater-recette.md`
3. Remplissez tous les champs
4. Listez les ingrédients dans la propriété `ingredients: []`

### Méthode 3: Migration de recettes existantes

**Avantages**: Transformation automatique des anciennes recettes

```bash
# Migrer toutes les recettes
python3 tools/migrate-recipes.py

# Migrer avec scraping des instructions manquantes
python3 tools/migrate-recipes.py --scrape

# Migrer une recette spécifique
python3 tools/migrate-recipes.py --recipe "Piperade"

# Mode dry-run (voir ce qui serait fait)
python3 tools/migrate-recipes.py --dry-run
```

## 🥕 Système d'ingrédients

### Comment ça marche

1. **Dans les recettes**: Les ingrédients sont listés dans deux endroits:
   - Propriété frontmatter `ingredients: []` (noms normalisés)
   - Section `## Ingrédients` (avec quantités et liens wiki)

2. **Pages d'ingrédients**: Chaque ingrédient a sa propre page qui liste automatiquement toutes les recettes qui l'utilisent

### Normalisation des ingrédients

Les noms d'ingrédients sont normalisés pour cohérence:
- **Singulier**: `tomate` (pas `tomates`)
- **Minuscules**: `oignon` (pas `Oignon`)
- **Sans article**: `ail` (pas `de l'ail`)
- **Forme simple**: `pomme de terre` (pas `pommes de terre coupées`)

### Exemple de lien

Dans la section Ingrédients de la recette:
```markdown
## Ingrédients

- 6 [[tomate]]s
- 2 [[oignon]]s
- 3 gousses [[ail]]
- 100g [[parmesan]]
```

La quantité reste visible, mais l'ingrédient devient un lien cliquable.

### Pages d'ingrédients

Chaque page d'ingrédient affiche automatiquement toutes les recettes qui l'utilisent via Dataview:

```markdown
## 🍽️ Utilisé dans les recettes

\`\`\`dataview
TABLE WITHOUT ID
  file.link as "Recette",
  temps_preparation as "Préparation (min)",
  temps_cuisson as "Cuisson (min)",
  type_cuisine as "Cuisine"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, "tomate")
SORT file.name ASC
\`\`\`
```

## 🔍 Requêtes Dataview utiles

### Toutes les recettes avec un ingrédient

```dataview
TABLE 
  temps_preparation as "Préparation",
  temps_cuisson as "Cuisson",
  type_cuisine as "Cuisine"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, "tomate")
SORT file.name ASC
```

### Recettes par type de cuisine

```dataview
TABLE 
  temps_preparation as "Préparation",
  regime as "Régime"
FROM "contenus/recettes/Fiches"
WHERE type_cuisine = "Italienne"
SORT file.name ASC
```

### Recettes végétariennes

```dataview
TABLE 
  type_cuisine as "Cuisine",
  temps_preparation as "Préparation"
FROM "contenus/recettes/Fiches"
WHERE contains(regime, "végétarien")
SORT file.name ASC
```

### Recettes de saison

```dataview
TABLE 
  type_cuisine as "Cuisine",
  ingredients as "Ingrédients"
FROM "contenus/recettes/Fiches"
WHERE contains(saison, "été")
SORT file.name ASC
```

### Recettes rapides (< 30 min préparation)

```dataview
TABLE 
  temps_preparation as "Préparation",
  temps_cuisson as "Cuisson",
  type_cuisine as "Cuisine"
FROM "contenus/recettes/Fiches"
WHERE temps_preparation < 30
SORT temps_preparation ASC
```

### Recettes par origine

```dataview
LIST
FROM "contenus/recettes/Fiches"
WHERE origine = "Sud-Ouest"
SORT file.name ASC
```

## 📊 Créer des vues personnalisées

### Hub d'ingrédients

Créez un fichier `contenus/recettes/Ingredients.md`:

```markdown
# 🥕 Ingrédients

Liste de tous les ingrédients utilisés dans les recettes.

\`\`\`dataview
TABLE 
  length(recettes) as "Nombre de recettes"
FROM "contenus/recettes/Ingredients"
SORT file.name ASC
\`\`\`

## Par catégorie

### Légumes

\`\`\`dataview
LIST
FROM "contenus/recettes/Ingredients"
WHERE categorie = "légume"
SORT file.name ASC
\`\`\`

### Épices

\`\`\`dataview
LIST
FROM "contenus/recettes/Ingredients"
WHERE categorie = "épice"
SORT file.name ASC
\`\`\`
```

### Dashboard de recettes

Créez `contenus/recettes/Dashboard.md`:

```markdown
# 🍽️ Dashboard Recettes

## Statistiques

- Total recettes: `= length(file.lists.inlinks) WHERE contains(file.path, "recettes/Fiches")`
- Types de cuisine: `= length(unique(type_cuisine)) FROM "contenus/recettes/Fiches"`
- Ingrédients uniques: `= length(file.lists) FROM "contenus/recettes/Ingredients"`

## Recettes récemment ajoutées

\`\`\`dataview
TABLE 
  created as "Ajouté le",
  type_cuisine as "Cuisine"
FROM "contenus/recettes/Fiches"
SORT created DESC
LIMIT 10
\`\`\`

## Recettes à essayer

\`\`\`dataview
LIST
FROM "contenus/recettes/Fiches"
WHERE !contains(file.outlinks, "note-degustation")
SORT file.name ASC
\`\`\`
```

## 🏷️ Système de tags

### Tags automatiques transformés

Le script de migration transforme automatiquement les anciens tags en propriétés structurées:

| Ancien tag | Nouvelle propriété | Valeur |
|------------|-------------------|--------|
| `RecetteFrançaise` | `type_cuisine` | `"Française"` |
| `RecetteItalienne` | `type_cuisine` | `"Italienne"` |
| `RecetteDuSudOuest` | `origine` | `"Sud-Ouest"` |
| `RecetteVégétarienne` | `regime` | `["végétarien"]` |
| `RecetteHiver` | `saison` | `["hiver"]` |

### Tags conservés

- `recette` : Tag principal pour toutes les recettes
- Tags d'ingrédients spécifiques si nécessaire

### Tags ignorés

Ces tags sont retirés pendant la migration car redondants ou obsolètes:
- `RecetteFacile`, `RecetteMoyenne`, `RecetteDifficile` (difficulté)
- `ChoixDeLaRédaction` (éditorial)

## 🔧 Maintenance

### Vérifier les liens brisés

```dataview
TABLE 
  file.outlinks as "Liens"
FROM "contenus/recettes/Fiches"
WHERE any(file.outlinks, (l) => !exists(l))
```

### Recettes sans ingrédients structurés

```dataview
LIST
FROM "contenus/recettes/Fiches"
WHERE !ingredients OR length(ingredients) = 0
```

### Ingrédients sans catégorie

```dataview
LIST
FROM "contenus/recettes/Ingredients"
WHERE !categorie OR categorie = ""
```

## 💡 Bonnes pratiques

### Lors de l'ajout d'une recette

1. ✅ Utilisez des noms d'ingrédients cohérents (singulier, minuscules)
2. ✅ Remplissez tous les champs de métadonnées
3. ✅ Ajoutez l'image de la recette
4. ✅ Vérifiez que les liens wiki sont créés
5. ✅ Testez que les pages d'ingrédients existent

### Pour les ingrédients

1. ✅ Nommez les ingrédients au singulier: `tomate` pas `tomates`
2. ✅ Évitez les articles: `ail` pas `de l'ail`
3. ✅ Soyez cohérent: utilisez toujours le même nom pour le même ingrédient
4. ✅ Utilisez la forme la plus simple: `pomme de terre` pas `pomme de terre coupée en dés`

### Pour les métadonnées

1. ✅ `type_cuisine`: Le style culinaire (Française, Italienne, Chinoise, etc.)
2. ✅ `origine`: La région ou pays spécifique (Provence, Toscane, Sud-Ouest, etc.)
3. ✅ `regime`: Liste de régimes alimentaires (végétarien, végétalien, sans gluten, etc.)
4. ✅ `saison`: Quand cette recette est la plus appropriée
5. ✅ `temps_preparation`: En minutes, juste la préparation
6. ✅ `temps_cuisson`: En minutes, juste la cuisson

## 🚀 Cas d'usage avancés

### Planification de menus

Créez une note de menu hebdomadaire:

```markdown
# Menu Semaine 42

## Lundi
- [[Salade de tomates]]

## Mardi
- [[Boeuf bourguignon]]

## Mercredi
- [[Pâtes carbonara]]

\`\`\`dataview
TABLE 
  sum(temps_preparation) as "Préparation totale",
  sum(temps_cuisson) as "Cuisson totale"
FROM [[Salade de tomates]], [[Boeuf bourguignon]], [[Pâtes carbonara]]
\`\`\`
```

### Liste de courses automatique

Pour générer une liste de courses basée sur plusieurs recettes:

```dataview
TABLE 
  ingredients as "Ingrédients nécessaires"
FROM [[Recette 1]], [[Recette 2]], [[Recette 3]]
```

### Suivi des recettes testées

Ajoutez une propriété `testee: true` après avoir fait une recette:

```dataview
TABLE 
  created as "Ajoutée",
  type_cuisine as "Cuisine"
FROM "contenus/recettes/Fiches"
WHERE !testee
SORT file.name ASC
```

## 🐛 Résolution de problèmes

### Les requêtes Dataview ne fonctionnent pas

1. Vérifiez que le plugin Dataview est installé et activé
2. Vérifiez la syntaxe de votre requête
3. Vérifiez les noms des propriétés (sensible à la casse)

### Les liens d'ingrédients sont brisés

Exécutez le script de migration pour recréer les liens:
```bash
python3 tools/migrate-recipes.py --recipe "Nom de la recette"
```

### Un ingrédient a plusieurs orthographes

1. Choisissez la forme canonique (singulier, minuscules)
2. Utilisez le script pour normaliser
3. Ou faites un rechercher/remplacer dans tout le vault

## 📚 Ressources

- [Guide Webclipper](WEBCLIPPER-RECETTES.md)
- [Documentation du script de migration](../tools/README-RECIPES.md)
- [Documentation Dataview](https://blacksmithgu.github.io/obsidian-dataview/)

## ✨ Exemples de recettes complètes

Voir les exemples dans `contenus/recettes/Fiches/`:
- `Boeuf bourguignon.md` - Recette bien structurée avec instructions détaillées
- `Piperade basque traditionnelle.md` - Exemple de recette migrée

## 🎓 Tutoriel étape par étape

### Ajouter votre première recette

1. **Clipper une recette web**:
   ```
   - Aller sur journaldesfemmes.fr/recette
   - Cliquer sur Web Clipper
   - Sélectionner template "Recette"
   - Sauvegarder
   ```

2. **Post-traiter**:
   ```bash
   python3 tools/migrate-recipes.py --recipe "Ma recette"
   ```

3. **Compléter**:
   ```yaml
   type_cuisine: "Française"
   origine: "Provence"
   regime: ["végétarien"]
   saison: ["été"]
   temps_preparation: 20
   temps_cuisson: 30
   ```

4. **Vérifier**:
   - Les ingrédients ont des liens `[[ingredient]]`
   - Les pages d'ingrédients existent
   - La recette apparaît dans les requêtes Dataview

5. **Profiter**:
   - Naviguez entre recettes et ingrédients
   - Créez des collections personnalisées
   - Planifiez vos menus
