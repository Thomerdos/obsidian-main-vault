# Guide des Templates de Recettes Simplifiés

## Changements Effectués

Les templates de recettes ont été simplifiés pour faciliter leur utilisation tout en maintenant la compatibilité avec Webclipper.

## Templates Disponibles

### 1. Template Principal : `templater-recette.md`

Le template principal a été simplifié en supprimant les champs optionnels peu utilisés :

**Champs supprimés** :
- `type_cuisine`
- `origine`
- `regime`
- `saison`
- `temps_preparation`
- `temps_cuisson`

**Sections supprimées** :
- "📋 Informations" (affichage des métadonnées)
- "📷 Photos" (doublait l'image principale)
- "💡 Notes & Astuces"

**Structure actuelle** :
```yaml
---
type: recette
title: "Nom de la recette"
source: "URL"
author: []
published: 
created: YYYY-MM-DD
image: "URL image"
ingredients: []
tags:
  - recette
---
```

**Sections** :
- 🍽️ Titre avec image
- 🥘 Ingrédients (avec liens wiki automatiques)
- 👨‍🍳 Instructions
- 🔗 Source

### 2. Template Webclipper : `webclipper-recette.md`

Le template Webclipper a été simplifié de la même manière et harmonisé avec le template principal.

**Avantages** :
- Structure identique au template principal
- Sélecteurs CSS conservés pour l'extraction automatique
- Notes d'utilisation simplifiées

### 3. Backup : `templater-recette-old.md`

L'ancien template complet a été sauvegardé pour référence. Si vous avez besoin des champs additionnels (type_cuisine, regime, saison, etc.), vous pouvez les ajouter manuellement aux recettes qui en ont besoin.

## Compatibilité

### Recettes Existantes

Les recettes existantes qui utilisent les anciens champs (type_cuisine, regime, saison, etc.) **continuent de fonctionner normalement**. Les champs ne sont simplement plus affichés dans les sections dédiées.

Si vous souhaitez afficher ces informations pour une recette spécifique, vous pouvez les ajouter manuellement dans le corps de la recette.

### Nouvelles Recettes

Les nouvelles recettes utiliseront la structure simplifiée, ce qui rend la création plus rapide et plus facile.

## Avantages de la Simplification

1. **Plus facile à utiliser** : Moins de champs à remplir
2. **Plus rapide** : Création de recettes accélérée
3. **Plus maintenable** : Moins de données à gérer
4. **Compatible Webclipper** : Fonctionne parfaitement avec l'outil de capture web
5. **Flexible** : Vous pouvez toujours ajouter des champs personnalisés si nécessaire

## Utilisation

### Avec Templater Plugin

1. Créer un nouveau fichier dans `contenus/recettes/Fiches/`
2. Invoquer Templater (`Ctrl+P` puis "Templater")
3. Sélectionner `templater-recette.md`
4. Remplir les informations

### Avec Webclipper

1. Sur la page web de la recette, activer Webclipper
2. Sélectionner le template `webclipper-recette.md`
3. Capturer la recette
4. Vérifier et ajuster les ingrédients et instructions
5. Créer les liens wiki vers les ingrédients (`[[nom-ingredient]]`)

## Migration des Recettes Existantes

**Important** : Aucune migration n'est nécessaire. Les recettes existantes fonctionnent parfaitement avec leurs champs actuels.

Si vous souhaitez mettre à jour une recette existante pour utiliser la nouvelle structure simplifiée, vous pouvez :

1. Supprimer les champs non utilisés du frontmatter
2. Supprimer les sections non nécessaires
3. Garder uniquement : titre, image, ingrédients, instructions, source

## Prochaines Étapes

1. Tester le nouveau template avec une nouvelle recette
2. Vérifier la compatibilité Webclipper
3. Ajuster si nécessaire selon vos besoins

## Questions Fréquentes

**Q: Puis-je encore ajouter des champs comme `type_cuisine` ?**  
R: Oui ! Vous pouvez ajouter n'importe quel champ personnalisé au frontmatter. Le template ne les affichera simplement pas automatiquement.

**Q: Que faire si j'ai besoin de l'ancien template complet ?**  
R: Utilisez `templater-recette-old.md` qui contient tous les anciens champs.

**Q: Les recettes existantes vont-elles casser ?**  
R: Non, toutes les recettes existantes continuent de fonctionner normalement.
