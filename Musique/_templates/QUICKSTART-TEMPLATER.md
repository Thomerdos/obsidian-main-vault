# 🚀 Quick Start - Templates Templater

Guide rapide pour commencer immédiatement avec les templates Templater.

## ⚡ TL;DR - Démarrage en 30 secondes

1. **Installer Templater** : Settings → Community plugins → Browse → "Templater" → Install
2. **Configurer** : Settings → Templater → Template folder: `Musique/_templates`
3. **Utiliser** : `Ctrl+P` → `Templater: Insert templater-concert` → Suivre les prompts

## 🎯 Cas d'usage principaux

### Ajouter un concert
```
Ctrl/Cmd + P → Templater: Insert templater-concert
```
✅ Le système guide avec les entités existantes  
✅ Détecte et corrige les fautes de frappe automatiquement  
✅ Crée toutes les entités nécessaires  
✅ Met à jour l'index automatiquement

### Workflow typique

1. **Créer une note vide** n'importe où
2. **Lancer le template** via palette de commandes
3. **Répondre aux prompts** :
   - Regarder les suggestions affichées
   - Copier-coller ou taper le nom
   - Accepter les corrections proposées
4. **C'est tout !** Le fichier est créé, nommé, placé, et l'index est mis à jour

## 🔑 Fonctionnalités clés

### ✨ Suggestions intelligentes

Chaque prompt affiche les entités existantes :
```
Groupes (séparés par des virgules)

Existant: Ayreon, Ghost, Iron Maiden, Gojira, ... (+45 de plus)
```

→ Évite les erreurs de saisie  
→ Rappelle ce qui existe déjà  
→ Facile de copier-coller

### 🎯 Détection de doublons

Si vous tapez un nom qui ressemble à un existant :
```
⚠️ "ghost" n'existe pas exactement.
Similaires trouvés: Ghost

Utiliser un existant ou confirmer "ghost"?
[Ghost] ← suggestion par défaut
```

→ Appuyer sur Entrée pour accepter  
→ Ou taper un autre nom pour confirmer

### 🤖 Création automatique

- ✅ Groupes → créés si nouveaux
- ✅ Salle/Festival → créés si nouveaux  
- ✅ Ville → créée si nouvelle
- ✅ Pays → créé si nouveau
- ✅ Dossier année → créé si nécessaire
- ✅ Concerts.md → mis à jour automatiquement

### 📁 Organisation automatique

Le fichier concert est automatiquement :
- **Nommé** : `YYYY-MM-DD - Nom`
- **Placé** : `Musique/Concerts/YYYY/`
- **Indexé** : Ligne ajoutée dans `Concerts.md` au bon endroit

## 📋 Exemples rapides

### Concert simple
```
Date: 2026-03-15
Groupes: Ghost
Salle: Halle Tony Garnier
Festival: [vide]
Ville: Lyon
Pays: France
```
→ Fichier: `Musique/Concerts/2026/2026-03-15 - Ghost.md`

### Festival
```
Date: 2026-06-18
Groupes: Gojira, Meshuggah, Tool
Salle: [vide]
Festival: Hellfest
Ville: Clisson
Pays: France
```
→ Fichier: `Musique/Concerts/2026/2026-06-18 - Hellfest.md`

## 🎨 Templates disponibles

| Template | Commande | Usage |
|----------|----------|-------|
| 🎸 Concert | `templater-concert` | Ajouter un concert/festival |
| 🎤 Groupe | `templater-groupe` | Ajouter un artiste/groupe |
| 🏛️ Salle | `templater-salle` | Ajouter une salle |
| 🎪 Festival | `templater-festival` | Ajouter un festival |
| 🎵 Genre | `templater-genre` | Ajouter un genre musical |
| 🏙️ Ville | `templater-ville` | Ajouter une ville |
| 🌍 Pays | `templater-pays` | Ajouter un pays |

## ⚠️ Points d'attention

### ✅ À FAIRE
- Regarder les suggestions avant de taper
- Accepter les corrections proposées pour éviter les doublons
- Laisser le système créer les entités automatiquement
- Utiliser le format de date YYYY-MM-DD

### ❌ À ÉVITER
- Ne pas créer manuellement les fiches groupes/salles/villes
- Ne pas éditer manuellement Concerts.md
- Ne pas déplacer manuellement les fichiers
- Ne pas ignorer les avertissements de doublons

## 🔧 Raccourcis recommandés

Configurer dans **Settings → Hotkeys** :

```
Ctrl/Cmd + Shift + C → Templater: Insert templater-concert
Ctrl/Cmd + Shift + G → Templater: Insert templater-groupe
Ctrl/Cmd + Shift + S → Templater: Insert templater-salle
```

## 📚 Documentation complète

Pour plus de détails, voir : **[[README-TEMPLATER]]**

## 💡 Astuces

1. **Copier-coller** les noms depuis les suggestions pour éviter les erreurs
2. **Vérifier l'orthographe** avant de valider (le système corrige mais c'est plus rapide)
3. **Grouper les saisies** : Ajouter plusieurs concerts à la fois si vous avez une liste
4. **Faire un backup** avant de commencer (par précaution)

## 🎯 Workflow avancé

### Préparation d'une série de concerts

1. Noter les concerts à ajouter sur papier/fichier texte
2. Pour chaque concert :
   - Lancer le template
   - Copier-coller les infos depuis votre liste
   - Valider
3. Vérifier dans Concerts.md que tout est bien ajouté

### Import massif

Si vous avez beaucoup de concerts à ajouter :
1. Commencer par créer les entités principales (groupes, salles)
2. Ensuite créer les concerts (les entités existeront déjà)
3. Le système ira plus vite car moins de créations

---

**🎸 Prêt à commencer ? Lancez `Ctrl+P` → `Templater: Insert templater-concert` !**
