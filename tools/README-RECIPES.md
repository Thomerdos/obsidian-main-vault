# Documentation du Script de Migration des Recettes

Ce document explique le fonctionnement du script `migrate-recipes.py`, ses options, et comment l'étendre pour supporter de nouveaux sites web.

## 📋 Vue d'ensemble

Le script `migrate-recipes.py` est un outil Python qui transforme les recettes Obsidian pour les structurer avec des propriétés frontmatter cohérentes et des liens wiki vers les ingrédients **uniquement dans le frontmatter**.

### Fonctionnalités principales

1. **Extraction d'ingrédients**: Parse la section `## Ingrédients` et extrait les noms d'ingrédients
2. **Normalisation**: Convertit les noms en forme canonique (singulier, minuscules, sans article, traduction français)
3. **Transformation de tags**: Convertit les anciens tags en propriétés structurées
4. **Création de pages**: Génère automatiquement les pages d'ingrédients
5. **Scraping web**: Récupère les instructions manquantes depuis les sources
6. **Wikilinks dans frontmatter**: Ajoute des liens wiki `[[ingredient]]` **uniquement dans le frontmatter**
7. **Texte préservé**: Le texte des recettes reste complètement intact (format original)
8. **Rapport de migration**: Génère un rapport détaillé des changements

## 🔗 Système de wikilinks frontmatter-only

### ⚠️ Changement important : Wikilinks UNIQUEMENT dans le frontmatter

**Nouvelle approche** (depuis février 2026) : Les wikilinks sont désormais **uniquement dans le frontmatter**, pas dans le texte.

### Pourquoi ce changement ?

**Problèmes de l'ancien système** (wikilinks dans le texte) :
- ❌ Liens invalides : `[[1¾ cups coconut milk (divided)]]` crée une page qui n'existe pas
- ❌ Texte modifié : Le format original des recettes est altéré
- ❌ Multiples crochets : `[[[[ingredient]]]]` dans certains fichiers
- ❌ Multilingue compliqué : Difficile de normaliser quand les quantités sont incluses

**Avantages du nouveau système** (wikilinks frontmatter-only) :
- ✅ **Texte intact** : Le format original des recettes est complètement préservé
- ✅ **Backlinks fonctionnent** : Via le frontmatter `ingredients: []`
- ✅ **Graphe de liens** : Montre les relations recette ↔ ingrédient
- ✅ **Normalisation facilitée** : Les ingrédients sont normalisés uniquement dans le frontmatter
- ✅ **Plus de liens cassés** : Pas de wikilinks avec quantités ou notes
- ✅ **Système plus simple** : Une seule source de vérité pour les liens

### Comment ça fonctionne

**Dans les recettes** :
```markdown
---
title: Green Thai Curry Recipe
ingredients:
  - "[[lait de coco]]"
  - "[[bouillon de poulet]]"
  - "[[cuisses de poulet]]"
  - "[[sucre de palme]]"
type: recette
---

## Ingrédients

- 1¾ cups coconut milk (divided)
- 1 cup chicken stock (unsalted)
- 1 lb chicken thigh (boneless, skinless)
- 2 Tablespoons palm sugar
```

**Le texte reste intact**, seul le frontmatter contient les liens normalisés.

**Dans les pages d'ingrédients** :
```markdown
## 🍽️ Utilisé dans les recettes

\`\`\`dataview
TABLE WITHOUT ID
  file.link as "Recette",
  source as "Source",
  temps_preparation as "Préparation",
  temps_cuisson as "Cuisson"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, this.file.link)
SORT file.name ASC
\`\`\`
```

**Explication de la requête** :
- `ingredients` : champ du frontmatter contenant la liste des wikilinks
- `this.file.link` : référence à la page d'ingrédient actuelle
- Dataview cherche dans le champ `ingredients` du frontmatter de chaque recette
- Si une recette a `[[tomate]]` dans son frontmatter, elle apparaît sur la page "tomate.md"

### Scripts disponibles

#### 1. `migrate-recipes.py` - Migration principale

Extrait les ingrédients et crée les wikilinks dans le frontmatter :

```bash
# Voir ce qui serait fait
python3 tools/migrate-recipes.py --dry-run

# Lancer la migration
python3 tools/migrate-recipes.py

# Avec scraping d'instructions
python3 tools/migrate-recipes.py --scrape
```

#### 2. `clean-recipe-wikilinks.py` - Nettoyage du texte

Supprime tous les wikilinks du texte des recettes (section ## Ingrédients) :

```bash
# Voir ce qui serait fait
python3 tools/clean-recipe-wikilinks.py --dry-run

# Nettoyer les wikilinks
python3 tools/clean-recipe-wikilinks.py
```

Le script :
1. Lit chaque recette
2. Dans la section "## Ingrédients", supprime tous les `[[wikilinks]]`
3. Corrige les wikilinks malformés (`[[[[ingredient]]]]` → `ingredient`)
4. Préserve le texte original

#### 3. `update-ingredient-pages.py` - Mise à jour des pages d'ingrédients

Met à jour la requête Dataview dans les pages d'ingrédients :

```bash
# Voir ce qui serait fait
python3 tools/update-ingredient-pages.py --dry-run

# Mettre à jour les pages
python3 tools/update-ingredient-pages.py
```

Change `WHERE contains(file.outlinks, ...)` en `WHERE contains(ingredients, ...)`

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
cd /chemin/vers/vault
pip install -r requirements.txt
```

Les dépendances installées:
- `PyYAML` - Parsing/écriture de YAML
- `requests` - Requêtes HTTP
- `beautifulsoup4` - Parsing HTML
- `lxml` - Parser HTML performant
- `click` - Interface CLI
- `ratelimit` - Limitation de débit pour le scraping

## 📖 Utilisation

### Options de base

```bash
# Afficher l'aide
python3 tools/migrate-recipes.py --help

# Mode dry-run (voir ce qui serait fait sans modifier)
python3 tools/migrate-recipes.py --dry-run

# Mode normal (modifier les fichiers)
python3 tools/migrate-recipes.py

# Mode avec scraping d'instructions
python3 tools/migrate-recipes.py --scrape

# Traiter une seule recette
python3 tools/migrate-recipes.py --recipe "Piperade"

# Combiner les options
python3 tools/migrate-recipes.py --scrape --recipe "Boeuf bourguignon"
```

### Options détaillées

| Option | Description | Défaut |
|--------|-------------|--------|
| `--vault PATH` | Chemin vers le vault Obsidian | `.` (dossier courant) |
| `--dry-run` | Afficher les changements sans modifier les fichiers | False |
| `--scrape` | Scraper les instructions manquantes depuis les URLs | False |
| `--recipe TEXT` | Traiter uniquement les recettes contenant ce texte | Toutes |

### Exemples d'utilisation

#### Exemple 1: Première migration complète

```bash
# Vérifier d'abord ce qui va être fait
python3 tools/migrate-recipes.py --dry-run

# Si tout semble bon, lancer la migration
python3 tools/migrate-recipes.py
```

#### Exemple 2: Migrer avec scraping

```bash
# Scraper les instructions pour toutes les recettes
python3 tools/migrate-recipes.py --scrape
```

⚠️ **Attention**: Le scraping fait des requêtes HTTP vers les sites source. Un rate limiting de 1 requête/2 secondes est appliqué pour respecter les serveurs.

#### Exemple 3: Corriger une recette spécifique

```bash
# Après avoir modifié manuellement une recette
python3 tools/migrate-recipes.py --recipe "Piperade"
```

#### Exemple 4: Tester sur une recette avant tout

```bash
# Tester sur une seule recette d'abord
python3 tools/migrate-recipes.py --dry-run --recipe "Piperade"

# Si OK, appliquer les changements
python3 tools/migrate-recipes.py --recipe "Piperade"
```

## 🔍 Fonctionnement interne

### 1. Parsing des ingrédients

Le script parse différents formats d'ingrédients:

```python
# Formats reconnus:
"- [ ] 600 g oignon"           → "oignon"
"- [ ] 3 unité poivron"        → "poivron"
"- [ ] quelque pincée sel"     → "sel"
"- 2 kg pommes de terre"       → "pomme de terre"
```

**Regex utilisées**:
```python
r'^[\d,\.]+\s*(?:kg|g|mg|l|ml|cl|dl|unité|gousse|filet|pincée)s?\s+(.+)$'
r'^quelques?\s+(?:pincée|gousse|unité)s?\s+(.+)$'
r'^\d+\s+(.+)$'
```

### 2. Normalisation des ingrédients

**Règles de normalisation**:

1. Conversion en minuscules
2. Suppression des articles: `le`, `la`, `les`, `l'`, `un`, `une`, `des`, `du`, `de`, `d'`
3. Conversion pluriel → singulier pour les ingrédients courants
4. Forme canonique: `ail` (pas `gousses d'ail`)

**Table de normalisation**:
```python
{
    'oignons': 'oignon',
    'tomates': 'tomate',
    'carottes': 'carotte',
    'pommes de terre': 'pomme de terre',
    "gousses d'ail": 'ail',
    # ... etc
}
```

### 3. Transformation des tags

**Mapping des tags**:

```python
TAG_TO_PROPERTY = {
    # Géographie
    'RecetteDuSudOuest': ('origine', 'Sud-Ouest'),
    'RecetteItalienne': ('type_cuisine', 'Italienne'),
    
    # Régime
    'RecetteVégétarienne': ('regime', 'végétarien'),
    'SansGluten': ('regime', 'sans gluten'),
    
    # Saison
    "RecetteTouteL'année": ('saison', "toute l'année"),
    'RecetteHiver': ('saison', 'hiver'),
}
```

**Propriétés générées**:
- `origine`: Valeur unique (dernière trouvée)
- `type_cuisine`: Valeur unique (dernière trouvée)
- `regime`: Liste de valeurs
- `saison`: Liste de valeurs

### 4. Scraping des instructions

**Sites supportés**:

| Site | Sélecteurs CSS |
|------|---------------|
| journaldesfemmes.fr | `.recipe-steps li`, `.rec_step` |
| marmiton.org | `.recipe-steps__item`, `.recipe-step-list__container` |
| ricardocuisine.com | `.recipe__step` |
| 750g.com | `.recipe-step-list__item` |
| Générique | `.instructions li`, `ol[itemprop="recipeInstructions"] li` |

**Fonctionnement**:

1. Télécharge la page HTML (rate limited)
2. Parse avec BeautifulSoup
3. Essaie chaque sélecteur dans l'ordre
4. Formate les étapes avec `- [ ]` (checklist)
5. Remplace la section Instructions vide

### 5. Création de pages d'ingrédients

**Template de page**:

```markdown
---
type: ingredient
nom: "ingredient"
categorie: ""
recettes: []
allergenes: []
saison: []
tags:
  - ingredient
---

# 🥕 Ingredient

## 📋 Informations

- **Catégorie**: 
- **Saison**: 
- **Allergènes**: 

## 🍽️ Utilisé dans les recettes

\`\`\`dataview
TABLE WITHOUT ID
  file.link as "Recette",
  source as "Source"
FROM "contenus/recettes/Fiches"
WHERE contains(file.outlinks, this.file.link)
SORT file.name ASC
\`\`\`

**Explication de la requête**:
- `file.outlinks` = tous les wikilinks sortants de chaque recette
- `this.file.link` = référence à la page d'ingrédient actuelle
- Si une recette contient `[[tomate]]`, elle apparaîtra automatiquement sur la page "tomate.md"
- Cette méthode utilise le graphe de liens natif d'Obsidian au lieu des propriétés frontmatter

## 💡 Notes

## 🔗 Liens
```

## 📊 Rapport de migration

Le script génère `migration-report.md` avec:

```markdown
# Migration Report

**Date**: 2024-01-20 15:30:00

## Summary

- Total recipes: 60
- Processed: 58
- Modified: 55
- Errors: 2
- Unique ingredients: 145
- Ingredient pages created: 132
- Instructions scraped: 12

## Ingredients Found

- **ail** (42 recipes)
- **oignon** (38 recipes)
- **tomate** (35 recipes)
...
```

## 🔧 Extension et personnalisation

### Ajouter un nouveau site web

Pour ajouter le support d'un nouveau site de recettes:

1. **Identifier les sélecteurs CSS**:

Inspectez la page web (F12) et trouvez les classes CSS:

```html
<!-- Exemple: nouveausite.com -->
<div class="recipe-ingredients-list">
  <div class="ingredient-item">500g farine</div>
</div>

<div class="recipe-directions">
  <div class="step">Étape 1</div>
</div>
```

2. **Ajouter les sélecteurs dans le script**:

Éditez `tools/migrate-recipes.py`, fonction `scrape_instructions()`:

```python
selectors = [
    # ... sélecteurs existants ...
    
    # nouveausite.com
    ('.step', 'text'),
    ('.ingredient-item', 'text'),
    
    # ... autres sélecteurs ...
]
```

3. **Tester**:

```bash
python3 tools/migrate-recipes.py --scrape --recipe "recette-du-site" --dry-run
```

### Modifier la normalisation

Pour ajouter de nouveaux mappings pluriel/singulier:

Éditez la fonction `normalize_ingredient_name()`:

```python
replacements = {
    'oignons': 'oignon',
    # Ajouter vos mappings ici
    'courgettes': 'courgette',
    'aubergines': 'aubergine',
}
```

### Ajouter de nouveaux tags

Pour transformer de nouveaux tags en propriétés:

Éditez le dictionnaire `TAG_TO_PROPERTY`:

```python
TAG_TO_PROPERTY = {
    # ... existants ...
    
    # Vos nouveaux tags
    'RecetteEspagnole': ('type_cuisine', 'Espagnole'),
    'RecetteSansLactose': ('regime', 'sans lactose'),
}
```

### Personnaliser le template d'ingrédient

Modifiez la fonction `create_ingredient_page()`:

```python
content = f"""# 🥕 {ingredient.capitalize()}

## Votre section personnalisée

...

## 🍽️ Utilisé dans les recettes

\`\`\`dataview
... votre requête Dataview ...
\`\`\`
"""
```

## 🐛 Débogage

### Activer le mode verbose

Ajoutez des prints dans le code pour déboguer:

```python
print(f"DEBUG: Processing {filepath.name}")
print(f"DEBUG: Found ingredients: {ingredients}")
```

### Tester sur un échantillon

```bash
# Copier quelques recettes dans un dossier test
mkdir /tmp/test-recipes
cp contenus/recettes/Fiches/Piperade*.md /tmp/test-recipes/

# Modifier temporairement le chemin dans le script
# Ou utiliser --vault /tmp/test-recipes
```

### Vérifier les erreurs

Le rapport de migration liste toutes les erreurs:

```bash
# Après la migration, vérifier le rapport
cat migration-report.md
```

## ⚠️ Limitations connues

1. **Scraping**: Certains sites modernes chargent le contenu en JavaScript - le scraping ne fonctionnera pas
2. **Normalisation**: Les ingrédients très spécifiques peuvent ne pas être bien normalisés
3. **Quantités**: Les formats de quantités non standard peuvent être mal parsés
4. **Langues**: Optimisé pour le français, peut nécessiter adaptation pour d'autres langues

## 🔐 Sécurité

- Le script ne supprime jamais de fichiers
- Le mode `--dry-run` permet de vérifier avant modification
- Les URLs sont validées avant scraping
- Rate limiting appliqué (1 req/2s) pour respecter les serveurs
- User-Agent standard utilisé pour les requêtes HTTP

## 📈 Performance

- **Temps de traitement**: ~0.5-1 seconde par recette (sans scraping)
- **Avec scraping**: ~2-3 secondes par recette (à cause du rate limiting)
- **60 recettes**: ~30 secondes (sans scraping), ~3-4 minutes (avec scraping)

## 🧪 Tests

### Test unitaire d'une fonction

```python
# Dans un script Python séparé
from migrate_recipes import parse_ingredient_line, normalize_ingredient_name

# Test parsing
assert parse_ingredient_line("- [ ] 600 g oignon") == "oignon"
assert parse_ingredient_line("- 3 unité poivron") == "poivron"

# Test normalisation
assert normalize_ingredient_name("oignons") == "oignon"
assert normalize_ingredient_name("les tomates") == "tomate"
```

### Test d'intégration

```bash
# Test complet sur une recette
python3 tools/migrate-recipes.py --dry-run --recipe "Test"
```

## 📚 Ressources

- [Documentation BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Documentation Click](https://click.palletsprojects.com/)
- [Guide Webclipper](../docs/WEBCLIPPER-RECETTES.md)
- [Guide workflow recettes](../docs/RECIPES-WORKFLOW.md)

## 💡 Conseils

1. **Toujours tester en dry-run** avant la première migration
2. **Commiter vos fichiers** avant de lancer le script
3. **Commencer par une recette** pour valider le comportement
4. **Vérifier le rapport** après chaque migration
5. **Personnaliser les mappings** selon vos besoins spécifiques

## 🤝 Contribution

Pour améliorer le script:

1. Identifiez un bug ou une amélioration
2. Testez votre modification sur un échantillon
3. Documentez le changement
4. Testez sur l'ensemble du vault (en dry-run d'abord)
5. Committez avec un message descriptif

## 📝 Exemples de modifications

### Exemple 1: Ajouter un nouveau format de quantité

```python
# Dans parse_ingredient_line()
patterns = [
    # Ajouter votre pattern
    r'^[\d,\.]+\s*(?:...|pièce)s?\s+(.+)$',
    # ...
]
```

### Exemple 2: Ignorer certains ingrédients

```python
# Dans extract_ingredients_from_content()
IGNORED_INGREDIENTS = {'eau', 'sel', 'poivre'}

if normalized and normalized not in IGNORED_INGREDIENTS:
    ingredients.append(normalized)
```

### Exemple 3: Ajouter des statistiques

```python
# Dans migrate_recipes()
stats['total_instructions_lines'] = 0

# Dans process_recipe()
if instructions_match:
    stats['total_instructions_lines'] += len(instructions_match.group(1).split('\n'))
```

## ✅ Checklist de migration

- [ ] Installer les dépendances
- [ ] Tester en dry-run
- [ ] Vérifier le rapport de dry-run
- [ ] Commiter les fichiers existants
- [ ] Lancer la migration réelle
- [ ] Vérifier le rapport final
- [ ] Spot-check quelques recettes
- [ ] Vérifier les pages d'ingrédients
- [ ] Tester les requêtes Dataview
- [ ] Commiter les changements

## 🎓 Support

Pour toute question ou problème:

1. Consultez cette documentation
2. Vérifiez les logs d'erreur
3. Testez en mode dry-run
4. Consultez les autres guides dans `docs/`
