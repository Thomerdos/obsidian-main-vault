# 📚 Documentation Templater - Système de Gestion des Concerts

Ce guide explique comment utiliser les templates Templater avancés pour automatiser la création de concerts et gérer votre collection musicale dans Obsidian.

## 🚀 Installation et Configuration

### 1. Installer Templater

1. Ouvrir **Settings** (⚙️) → **Community plugins**
2. Désactiver le "Safe mode" si nécessaire
3. Cliquer sur **Browse** et chercher "Templater"
4. Installer et activer le plugin **Templater**

### 2. Configurer Templater

1. Aller dans **Settings** → **Templater**
2. Configurer les paramètres suivants :
   - **Template folder location** : `Musique/_templates` (ou ajouter `Lieux/_templates`)
   - **Trigger Templater on new file creation** : ✅ Activé
   - **Enable System Commands** : ✅ Activé
   - **Script files folder location** : (optionnel)

### 3. Configuration recommandée

- **Folder templates** : Vous pouvez configurer des templates automatiques par dossier
- **Startup templates** : (optionnel)

## 📝 Templates Disponibles

### Templates Templater (Avancés - Recommandés)

| Template | Fichier | Description |
|----------|---------|-------------|
| 🎸 Concert | `templater-concert.md` | Création interactive de concerts avec auto-création des entités |
| 🎤 Groupe | `templater-groupe.md` | Ajout d'artistes/groupes avec détection de doublons |
| 🏛️ Salle | `templater-salle.md` | Création de salles de concert |
| 🎪 Festival | `templater-festival.md` | Ajout de festivals |
| 🎵 Genre | `templater-genre.md` | Création de genres musicaux |
| 🏙️ Ville | `templater-ville.md` | Ajout de villes |
| 🌍 Pays | `templater-pays.md` | Création de pays |

### Templates Basiques (Conservation)

Les templates basiques (`template-*.md`) restent disponibles pour la rétrocompatibilité et l'utilisation manuelle simple.

## 🎯 Guide d'Utilisation

### Ajouter un Nouveau Concert

#### Méthode 1 : Via la Palette de Commandes (Recommandé)

1. Créer une nouvelle note (n'importe où dans votre vault)
2. Ouvrir la **palette de commandes** : `Ctrl/Cmd + P`
3. Taper : `Templater: Insert templater-concert`
4. Suivre les prompts interactifs :

**Prompts guidés :**

```
📅 Date du concert (YYYY-MM-DD) : [2026-03-15]
🎤 Groupes (séparés par des virgules) : 
   Existant: Ayreon, Ghost, Iron Maiden, ... (+50 de plus)
   → Ghost
   
🏛️ Salle (laisser vide si festival) : 
   Existant: Halle Tony Garnier, Le Sucre, L'Olympia, ...
   → Halle Tony Garnier
   
🎪 Festival (laisser vide si concert en salle) : 
   → [laisser vide]
   
🏙️ Ville : 
   Existant: Lyon, Paris, Grenoble, ...
   → Lyon
   
🌍 Pays : 
   Existant: France, Allemagne, Espagne, ...
   → France
   
📝 Notes initiales (optionnel) : 
   → Super ambiance !
```

**Détection intelligente de doublons :**

Si vous saisissez un nom qui n'existe pas exactement, le système vous propose des suggestions :

```
⚠️ "lyon" n'existe pas exactement.
Similaires trouvés: Lyon

Utiliser un existant ou confirmer "lyon"?
[Lyon] ← suggestion par défaut
```

#### Résultat Automatique

✅ **Fichier créé** : `Musique/Concerts/2026/2026-03-15 - Ghost.md`  
✅ **Frontmatter YAML** généré automatiquement  
✅ **Fichier déplacé** dans le bon dossier (création du dossier de l'année si nécessaire)  
✅ **Concerts.md mis à jour** avec la nouvelle entrée au bon endroit  
✅ **Entités créées automatiquement** si elles n'existent pas :
   - `Musique/Groupes/Ghost.md`
   - `Musique/Salles/Halle Tony Garnier.md` (si nouvelle)
   - `Lieux/Villes/Lyon.md` (si nouvelle)
   - `Lieux/Pays/France.md` (si nouveau)

### Ajouter un Festival avec Plusieurs Groupes

```
📅 Date : 2026-06-20
🎤 Groupes : Gojira, Meshuggah, Tool
🏛️ Salle : [vide]
🎪 Festival : Hellfest
🏙️ Ville : Clisson
🌍 Pays : France
```

**Résultat :**
- Fichier : `Musique/Concerts/2026/2026-06-20 - Hellfest.md`
- 3 fiches groupes créées (si nécessaire)
- Fiche festival créée (si nécessaire)
- Fiche ville créée (si nécessaire)
- Entrée ajoutée à `Concerts.md`

### Ajouter un Groupe/Artiste

1. Palette de commandes → `Templater: Insert templater-groupe`
2. Suivre les prompts :
   - Nom du groupe
   - Genre(s) (avec suggestions)
   - Pays d'origine (avec suggestions)
   - Année de formation
   - Site web

**Fonctionnalités :**
- ✅ Détection de doublons pour genres et pays
- ✅ Création automatique du pays si nécessaire
- ✅ Création automatique des genres si nécessaires
- ✅ Queries Dataview pour voir les concerts du groupe

### Ajouter une Salle

1. Palette de commandes → `Templater: Insert templater-salle`
2. Renseigner :
   - Nom de la salle
   - Ville (avec suggestions)
   - Pays (avec suggestions)
   - Capacité
   - Adresse

**Avantages :**
- ✅ Détection de doublons pour villes et pays
- ✅ Création automatique de la ville et du pays si nécessaire
- ✅ Queries automatiques pour concerts dans cette salle

### Ajouter un Festival

Similaire à l'ajout de salle, avec période habituelle au lieu de capacité.

### Ajouter une Ville

1. Palette de commandes → `Templater: Insert templater-ville`
2. Renseigner :
   - Nom de la ville
   - Pays (avec suggestions)
   - Région

**Fonctionnalités :**
- ✅ Détection de doublons pour le pays
- ✅ Création automatique du pays si nécessaire
- ✅ Queries pour salles et concerts dans cette ville

### Ajouter un Pays

Template simple pour créer une fiche pays avec continent et queries Dataview.

### Ajouter un Genre Musical

Template pour créer une fiche genre avec description et queries pour artistes et concerts.

## ⌨️ Raccourcis Clavier Recommandés

Configurer dans **Settings** → **Hotkeys** :

| Raccourci | Commande |
|-----------|----------|
| `Ctrl/Cmd + Shift + C` | Templater: Insert templater-concert |
| `Ctrl/Cmd + Shift + G` | Templater: Insert templater-groupe |
| `Ctrl/Cmd + Shift + S` | Templater: Insert templater-salle |
| `Ctrl/Cmd + Shift + F` | Templater: Insert templater-festival |

## ✨ Fonctionnalités Avancées

### 1. Suggestions Contextuelles

Chaque prompt affiche les entités existantes pour faciliter la saisie :

```
Ville
Existant: Lyon, Paris, Grenoble, Clisson, Tilburg, ... (25 de plus)
```

### 2. Détection Intelligente de Doublons

Le système détecte automatiquement les correspondances approximatives :
- **"ghost"** → suggère "Ghost"
- **"lyon"** → suggère "Lyon"  
- **"hell fest"** → suggère "Hellfest"

Vous pouvez :
- Accepter la suggestion (appuyer sur Entrée)
- Confirmer votre saisie originale
- Modifier pour un autre existant

### 3. Création Automatique des Dépendances

Quand vous créez un concert, toutes les entités nécessaires sont créées automatiquement :
- Groupes → créés avec référence au pays
- Salle → créée avec référence à la ville et au pays
- Festival → créé avec référence à la ville et au pays
- Ville → créée avec référence au pays
- Pays → créé si nécessaire

### 4. Mise à Jour Automatique de l'Index

`Concerts.md` est mis à jour automatiquement :
- **Insertion au bon endroit** (ordre décroissant par date)
- **Checkbox automatique** : `[x]` pour concerts passés, `[ ]` pour futurs
- **Liens corrects** vers les entités
- **Création de section année** si nécessaire

### 5. Organisation Automatique

- **Création du dossier année** si nécessaire
- **Déplacement automatique** du fichier au bon endroit
- **Nommage standardisé** : `YYYY-MM-DD - Nom`

## 🎨 Avantages vs Templates Basiques

| Critère | Templates Basiques | Templates Templater |
|---------|-------------------|---------------------|
| Saisie | Copier-coller manuel | Prompts guidés |
| Nommage | Manuel | Automatique |
| Emplacement | Manuel | Automatique |
| Création entités | Manuelle | Automatique |
| Mise à jour index | Manuelle | Automatique |
| Détection doublons | ❌ | ✅ |
| Suggestions | ❌ | ✅ |
| Rapidité | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Cohérence | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🔧 Résolution de Problèmes

### Le template ne s'exécute pas

1. Vérifier que Templater est activé
2. Vérifier le "Template folder location"
3. Vérifier que "Enable System Commands" est activé

### Les prompts ne s'affichent pas

1. Vérifier la syntaxe du template (pas d'erreurs JavaScript)
2. Ouvrir la console développeur : `Ctrl/Cmd + Shift + I`
3. Chercher des erreurs dans la console

### Le fichier n'est pas déplacé

1. Vérifier que le dossier parent existe
2. Le template crée automatiquement le dossier de l'année si nécessaire
3. Vérifier les permissions de fichier

### Concerts.md n'est pas mis à jour

1. Vérifier que le fichier `Musique/Concerts.md` existe
2. Vérifier la structure du fichier (sections avec `### ANNÉE`)
3. Le template insère dans la bonne section ou crée une nouvelle section

### Doublons créés malgré la détection

La détection fonctionne sur la correspondance approximative (contient/contenu dans).
Pour des noms très différents, confirmez ou choisissez l'existant manuellement.

## 💡 Conseils et Bonnes Pratiques

### 1. Nommage Cohérent

- **Groupes** : Respecter les majuscules officielles (ex: "Ghost", pas "ghost")
- **Villes** : Utiliser le nom officiel (ex: "Lyon", pas "lyon")
- **Pays** : Utiliser le nom en français (ex: "France", "Allemagne")

### 2. Utilisation des Suggestions

- **Toujours regarder** les suggestions affichées avant de saisir
- **Copier-coller** depuis les suggestions pour éviter les erreurs
- **Accepter les corrections** proposées par le système

### 3. Organisation

- Les dossiers sont créés automatiquement, ne les créez pas à l'avance
- Laissez le système gérer le placement des fichiers
- N'éditez pas manuellement `Concerts.md`, utilisez le template

### 4. Corrections Post-Création

Si vous devez corriger un concert après création :
- Éditer le frontmatter YAML manuellement
- Mettre à jour l'entrée dans `Concerts.md` manuellement
- Ou supprimer et recréer avec le template

### 5. Backup

- Faites des sauvegardes régulières de votre vault
- Utilisez Git pour versionner vos changements
- Les templates modifient `Concerts.md`, gardez un historique

## 📊 Exemples d'Utilisation

### Exemple 1 : Concert Simple

**Saisie :**
```
Date : 2026-03-15
Groupes : Ghost
Salle : Halle Tony Garnier
Festival : 
Ville : Lyon
Pays : France
Notes : Concert incroyable
```

**Fichiers créés/modifiés :**
- ✅ `Musique/Concerts/2026/2026-03-15 - Ghost.md`
- ✅ `Musique/Concerts.md` (ligne ajoutée)
- ✅ Si nouveaux : `Musique/Groupes/Ghost.md`, `Musique/Salles/Halle Tony Garnier.md`

### Exemple 2 : Festival Multi-Groupes

**Saisie :**
```
Date : 2026-06-18
Groupes : Gojira, Meshuggah, Tool, Opeth
Salle : 
Festival : Hellfest
Ville : Clisson
Pays : France
```

**Fichiers créés/modifiés :**
- ✅ `Musique/Concerts/2026/2026-06-18 - Hellfest.md`
- ✅ 4 fiches groupes (si nouvelles)
- ✅ `Musique/Festivals/Hellfest.md` (si nouveau)
- ✅ `Lieux/Villes/Clisson.md` (si nouvelle)

### Exemple 3 : Concert à l'Étranger

**Saisie :**
```
Date : 2026-09-15
Groupes : Ayreon
Salle : Poppodium 013
Festival : 
Ville : Tilburg
Pays : Pays-Bas
```

**Avec détection de doublons :**
- Si vous tapez "Pays-Bas", le système suggère "Pays-Bas" (exact)
- Si vous tapez "pays bas", le système suggère "Pays-Bas" (correction)
- Si nouveau pays, création automatique de `Lieux/Pays/Pays-Bas.md`

## 🎓 Ressources

- **Documentation Templater** : https://silentvoid13.github.io/Templater/
- **Syntaxe Dataview** : https://blacksmithgu.github.io/obsidian-dataview/
- **Communauté Obsidian** : https://forum.obsidian.md/

## 📝 Notes de Version

### v1.0 - Février 2026

**Nouveautés :**
- ✅ Templates Templater interactifs pour tous les types d'entités
- ✅ Détection intelligente de doublons
- ✅ Suggestions contextuelles basées sur l'existant
- ✅ Création automatique des dépendances
- ✅ Mise à jour automatique de `Concerts.md`
- ✅ Organisation automatique des fichiers
- ✅ Conservation des templates basiques pour rétrocompatibilité

---

**Pour toute question ou problème, n'hésitez pas à consulter ce guide ou à ouvrir une issue sur le repository GitHub.**

🎸 **Bon concerts tracking !** 🎸
