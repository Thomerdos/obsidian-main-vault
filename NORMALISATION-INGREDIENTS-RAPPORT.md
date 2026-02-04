# Rapport de Normalisation des Ingrédients

## Résumé

La normalisation des ingrédients dans le vault Obsidian a été effectuée avec succès le 4 février 2026.

### Statistiques

- **204 ingrédients** normalisés créés
- **43 recettes** avec ingrédients mis à jour
- **17 recettes** sans ingrédients (inchangées)
- **60 recettes** au total
- **425 anciennes pages** d'ingrédients supprimées
- **Réduction de 52%** (221 pages éliminées)

## Améliorations Appliquées

✅ **Tous les ingrédients sont en français**
- Exemples: `beef` → `boeuf`, `chicken stock` → `bouillon de poulet`

✅ **Format singulier** (sauf exceptions naturelles)
- Exemples: `tomates` → `tomate`, `oignons` → `oignon`
- Exceptions: `épinards`, `haricots verts`, `petits pois`

✅ **Sans articles** (le, la, les, du, de)
- Exemples: `le beurre` → `beurre`, `de l'ail` → `ail`

✅ **Sans quantités ni unités**
- Exemples: `3-4 tbsp thai cooking tamarind` → `tamarin`
- Exemples: `1,5 cs de piment moulu` → `piment moulu`

✅ **Sans préparations** (haché, coupé, etc.)
- Exemples: `palm sugar, chopped` → `sucre de palme`
- Exemples: `Bean sprouts, loosely packed` → `germes de soja`

✅ **Doublons éliminés**
- Exemples: `basilic frais` → `basilic`
- Exemples: `Basilicic` → `basilic`

## Top 15 des Ingrédients les Plus Utilisés

1. **sel** (24 recettes)
2. **oignon** (21 recettes)
3. **ail** (20 recettes)
4. **beurre** (11 recettes)
5. **eau** (11 recettes)
6. **huile d'olive** (10 recettes)
7. **sucre** (10 recettes)
8. **tomate** (9 recettes)
9. **poivre** (9 recettes)
10. **gingembre** (9 recettes)
11. **thym** (7 recettes)
12. **échalote** (7 recettes)
13. **persil** (6 recettes)
14. **huile** (6 recettes)
15. **ciboule** (6 recettes)

## Catégories d'Ingrédients

- **Légumes**: 27 ingrédients
- **Viandes**: 17 ingrédients
- **Épices/Herbes**: 31 ingrédients
- **Produits laitiers**: 8 ingrédients
- **Féculents**: 11 ingrédients
- **Liquides**: 32 ingrédients

## Exemples de Normalisation

### Traductions de l'anglais vers le français

| Avant | Après |
|-------|-------|
| `beef` | `boeuf` |
| `chicken thigh` | `cuisse de poulet` |
| `chicken stock/broth` | `bouillon de poulet` |
| `Bean sprouts, loosely packed` | `germes de soja` |
| `palm sugar, chopped` | `sucre de palme` |
| `Thai basil leaves` | `basilic thaï` |
| `fermented shrimp paste` | `pâte de crevette` |

### Simplifications

| Avant | Après |
|-------|-------|
| `3-4 tbsp thai cooking tamarind` | `tamarin` |
| `1,5 cs de piment moulu` | `piment moulu` |
| `Basilicic frais` | `basilic` |
| `boeuf haché` | `boeuf haché` (conservé car c'est une forme spécifique) |
| `7-10 stalks garlic chives, cut into 2" pieces` | `ciboulette chinoise` |

### Élimination des doublons

| Anciennes pages | Page normalisée |
|----------------|-----------------|
| `Basilicic`, `Basilicic frais` | `basilic` |
| `Ail`, `d'ail`, `d'ail pressées`, `clove ail`, `cloves ail` | `ail` |
| `Huile`, `d'huile`, `cooking oil` | `huile` |

## Règles de Normalisation Appliquées

1. **Langue**: Toujours en français (traduire l'anglais)
2. **Nombre**: Singulier (sauf exceptions naturelles)
3. **Article**: Pas d'article (le, la, les, du, de, etc.)
4. **Quantité**: Pas de quantité ni d'unité
5. **Préparation**: Pas de préparation (haché, coupé, etc.)
6. **Forme canonique**: 
   - "ail" (pas "gousses d'ail")
   - "tomate" (pas "tomates fraîches")
   - "boeuf" (pas "viande de boeuf")

## Structure des Fichiers

### Pages d'ingrédients
Localisation: `contenus/recettes/Ingredients/`

Format standard:
```markdown
---
title: Nom de l'ingrédient
type: ingredient
---

# Nom de l'ingrédient

Ingrédient utilisé dans les recettes.
```

### Frontmatter des recettes
Format normalisé:
```yaml
ingredients:
- '[[ail]]'
- '[[oignon]]'
- '[[tomate]]'
```

## Scripts Utilisés

Les scripts de normalisation sont disponibles dans `/tools/`:
- `normalize_ingredients.py`: Script principal de normalisation
- `fix_remaining_ingredients.py`: Corrections supplémentaires
- `final_report.py`: Génération du rapport

## Résultats

✅ **Avant**: 425 pages d'ingrédients mal normalisées  
✅ **Après**: 204 ingrédients proprement normalisés  
✅ **Gain**: 52% de réduction, élimination des doublons et des erreurs

Les ingrédients sont maintenant:
- ✅ Tous en français
- ✅ Correctement formatés
- ✅ Sans doublons
- ✅ Facilement recherchables via wikilinks
- ✅ Cohérents à travers toutes les recettes

## Prochaines Étapes

Pour maintenir la qualité:
1. Toujours vérifier la normalisation avant d'ajouter de nouveaux ingrédients
2. Utiliser les ingrédients existants plutôt que d'en créer de nouveaux
3. Respecter les règles de normalisation pour toute nouvelle recette

---

*Rapport généré le 4 février 2026*
