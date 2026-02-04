# Guide Webclipper pour les Recettes

Ce guide explique comment utiliser Obsidian Web Clipper pour capturer facilement des recettes depuis le web et les intégrer dans votre vault.

## 📦 Installation

### 1. Installer le plugin Obsidian Web Clipper

Le Web Clipper d'Obsidian permet de capturer du contenu web directement dans votre vault.

- **Extension navigateur**: Installez l'extension Obsidian Web Clipper depuis votre navigateur
  - [Chrome Web Store](https://chrome.google.com/webstore)
  - [Firefox Add-ons](https://addons.mozilla.org)
- **Configuration**: Connectez l'extension à votre vault Obsidian

### 2. Configurer le template de recette

1. Le template `templates/recettes/webclipper-recette.md` est déjà créé dans votre vault
2. Dans l'extension Web Clipper, ajoutez ce template comme template personnalisé
3. Nommez-le "Recette" pour le retrouver facilement

## 🎯 Workflow recommandé

### Étape 1: Clipper la recette

1. Naviguez vers une recette sur un site web
2. Cliquez sur l'icône Obsidian Web Clipper dans votre navigateur
3. Sélectionnez le template "Recette"
4. Vérifiez que les informations de base sont capturées:
   - Titre
   - URL source
   - Image
   - Auteur
   - Date de publication
5. Cliquez sur "Clip to Obsidian"
6. Sauvegardez dans `contenus/recettes/Fiches/`

### Étape 2: Post-traitement automatique (Option A - Recommandé)

**Utiliser le script Python de migration:**

```bash
# Traiter la recette qui vient d'être clippée
cd /chemin/vers/vault
python3 tools/migrate-recipes.py --recipe "Nom de la recette"
```

Le script va automatiquement:
- ✅ Extraire les ingrédients de la section texte
- ✅ Normaliser les noms d'ingrédients
- ✅ Créer la propriété `ingredients: []` dans le frontmatter
- ✅ Créer les pages d'ingrédients manquantes
- ✅ Ajouter des liens wiki `[[ingredient]]` dans la liste

### Étape 2: Post-traitement manuel (Option B)

**Utiliser le template Templater:**

1. Ouvrez la recette clippée dans Obsidian
2. Exécutez le template `templater-post-webclipper.md`
3. Le template va automatiquement traiter les ingrédients

### Étape 3: Compléter les métadonnées

Éditez le frontmatter pour ajouter:

```yaml
type_cuisine: "Italienne"      # Type de cuisine
origine: "Toscane"              # Origine géographique
regime: ["végétarien"]          # Régimes alimentaires
saison: ["été"]                 # Saisons appropriées
temps_preparation: 20           # Minutes
temps_cuisson: 45               # Minutes
```

## 🌐 Sélecteurs CSS par site

Le template Webclipper inclut des sélecteurs CSS pour les sites de recettes populaires:

### journaldesfemmes.fr
- **Ingrédients**: `.recipe-ingredients-list`, `.rec_ingredients`
- **Instructions**: `.recipe-steps`, `.rec_step`

### marmiton.org
- **Ingrédients**: `.recipe-ingredients`, `.ingredient-item`
- **Instructions**: `.recipe-steps`, `.recipe-step-list__item`

### ricardocuisine.com
- **Ingrédients**: `.recipe__ingredients`, `.ingredient`
- **Instructions**: `.recipe__step`

### 750g.com
- **Ingrédients**: `.recipe-ingredient`
- **Instructions**: `.recipe-step-list__item`

### papillesetpupilles.fr
- **Ingrédients**: `.ingredients`
- **Instructions**: `.instructions`

### Sites génériques

Le template inclut aussi des sélecteurs génériques qui fonctionnent sur de nombreux sites:
- `[itemprop="recipeIngredient"]`
- `[itemprop="recipeInstructions"]`
- `.ingredients li`
- `.directions li`

## 🔧 Personnalisation

### Ajouter un nouveau site

Si vous utilisez fréquemment un site non couvert, vous pouvez ajouter ses sélecteurs:

1. Inspectez la page web (F12 dans votre navigateur)
2. Trouvez les classes CSS pour les ingrédients et instructions
3. Ajoutez-les au template `webclipper-recette.md`:

```markdown
## Ingrédients

{{selector:.votre-classe-ingredients}}

## Instructions

{{selector:.votre-classe-instructions}}
```

### Modifier le template

Vous pouvez personnaliser `templates/recettes/webclipper-recette.md` pour:
- Ajouter d'autres champs
- Modifier la structure
- Changer les sélecteurs CSS

## 💡 Astuces

### Vérifier la capture avant de sauvegarder

Avant de cliquer "Clip to Obsidian", vérifiez:
- ✅ Le titre est correct
- ✅ L'image principale est capturée
- ✅ Les ingrédients sont visibles
- ✅ Les instructions sont présentes

### Que faire si les ingrédients ne sont pas capturés?

1. **Copiez-collez manuellement**: Copiez la liste d'ingrédients et collez-la dans la section `## Ingrédients`
2. **Utilisez le script de migration**: Le script `migrate-recipes.py` saura extraire les ingrédients même d'un format texte simple
3. **Ajoutez les ingrédients dans le frontmatter**: Modifiez directement la propriété `ingredients: []`

### Exemple de recette bien structurée

```markdown
---
type: recette
title: "Tarte aux pommes"
source: "https://example.com/tarte-aux-pommes"
author: ["Chef Jean"]
published: 2024-01-15
created: 2024-01-20
image: "https://example.com/image.jpg"
type_cuisine: "Française"
origine: "Normandie"
regime: ["végétarien"]
saison: ["automne", "hiver"]
temps_preparation: 30
temps_cuisson: 45
ingredients:
  - pomme
  - pâte brisée
  - sucre
  - beurre
  - cannelle
tags:
  - recette
---

## Ingrédients

- 6 [[pomme]]s
- 1 [[pâte brisée]]
- 100g [[sucre]]
- 50g [[beurre]]
- 1 cuillère à café [[cannelle]]

## Instructions

1. Préchauffer le four à 180°C
2. Éplucher et couper les pommes en quartiers
3. Disposer sur la pâte brisée
4. Saupoudrer de sucre et cannelle
5. Parsemer de noisettes de beurre
6. Cuire 45 minutes
```

## 🐛 Résolution de problèmes

### L'extension ne se connecte pas au vault

1. Vérifiez qu'Obsidian est ouvert
2. Vérifiez que l'API locale est activée dans Obsidian (Paramètres → Sécurité)
3. Redémarrez l'extension

### Les sélecteurs CSS ne fonctionnent pas

Certains sites utilisent du JavaScript pour charger le contenu dynamiquement. Dans ce cas:
1. Attendez que la page soit complètement chargée
2. Ou copiez-collez manuellement le contenu
3. Utilisez le script de migration pour extraire les ingrédients

### Les ingrédients ne sont pas bien formatés

Pas de problème! Le script `migrate-recipes.py` est conçu pour gérer différents formats:
- Listes avec tirets
- Listes avec checkboxes `- [ ]`
- Texte brut avec quantités
- Différents formats de quantités (kg, g, tasse, etc.)

## 📚 Ressources

- [Documentation Obsidian Web Clipper](https://help.obsidian.md/Web+clipper)
- [Guide du workflow des recettes](RECIPES-WORKFLOW.md)
- [Documentation du script de migration](../tools/README-RECIPES.md)

## 🎓 Exemples

### Exemple 1: Recette simple sans scraping

```bash
# Clipper la recette → Obsidian Web Clipper
# Post-traiter → Script Python
python3 tools/migrate-recipes.py --recipe "Ma nouvelle recette"
```

### Exemple 2: Recette avec scraping d'instructions

```bash
# Si les instructions sont incomplètes, activer le scraping
python3 tools/migrate-recipes.py --recipe "Ma recette" --scrape
```

### Exemple 3: Traiter plusieurs recettes clippées

```bash
# Sans argument, traite toutes les recettes
python3 tools/migrate-recipes.py
```

## ✅ Checklist après clipping

- [ ] Vérifier le titre et l'URL source
- [ ] Compléter type_cuisine, origine, regime, saison
- [ ] Ajouter temps_preparation et temps_cuisson
- [ ] Exécuter le script de migration ou le template post-webclipper
- [ ] Vérifier que les ingrédients ont des liens wiki
- [ ] Vérifier que les pages d'ingrédients ont été créées
- [ ] Relire les instructions et corriger si nécessaire
- [ ] Ajouter des notes personnelles si désiré
