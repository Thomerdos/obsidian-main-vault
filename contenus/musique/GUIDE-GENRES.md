# 🎵 Guide d'Utilisation des Pages de Genres

## Vue d'ensemble

Les pages de genres permettent de visualiser et naviguer dans votre collection musicale par style musical. Chaque genre agit comme un hub central reliant tous les artistes et concerts associés.

## 📊 Structure des Genres

### 56 Genres Créés

**Metal (17 genres):**
- Heavy Metal, Death Metal, Doom Metal, Sludge Metal
- Progressive Metal, Thrash Metal, Groove Metal
- Industrial Metal, Alternative Metal, Funeral Doom Metal
- Neoclassical Metal, Metalcore, Nu Metal, Funk Metal
- NWOBHM, Neue Deutsche Härte, Drone Metal

**Rock (10 genres):**
- Progressive Rock, Psychedelic Rock, Hard Rock
- Alternative Rock, Indie Rock, Stoner Rock
- Art Rock, Garage Rock, Industrial Rock, Krautrock

**Jazz (7 genres):**
- Jazz, Jazz Fusion, Jazz-Rock
- Latin Jazz, Spiritual Jazz, Acid Jazz
- Instrumental

**Funk/Soul (4 genres):**
- Funk, Soul, Disco, Afrobeat

**Autres (18 genres):**
- Electronic, Experimental, Folk, Pop
- Trip Hop, Alternative, Gothic, Drone
- Hip Hop, Comedy, Progressive, Psychedelic
- Rock, Fusion, Sludge, Zeuhl, Festival, Autre

## 🔗 Relations Automatiques

### De Genre vers Artistes

Chaque page de genre liste automatiquement tous les artistes de ce style :

```dataview
TABLE pays-origine as "Pays", formation as "Formation"
FROM "Musique/Groupes"
WHERE contains(genre, this.file.name)
SORT file.name ASC
```

**Exemple - Heavy Metal:**
- Iron Maiden (Royaume-Uni, 1975)
- Judas Priest (Royaume-Uni, 1969)
- Blue Öyster Cult (États-Unis, 1967)

### De Genre vers Concerts

Chaque page liste aussi les concerts du genre :

```dataview
TABLE date as "Date", groupes as "Artistes", ville as "Ville"
FROM "Musique/Concerts"
FLATTEN groupes as groupe_name
WHERE contains(file(groupe_name).genre, this.file.name)
SORT date DESC
LIMIT 50
```

### D'Artiste vers Genres

Dans chaque fiche artiste, les genres sont maintenant des liens cliquables :

**Avant:**
```markdown
- **Genre** : Progressive Rock, Heavy Metal
```

**Maintenant:**
```markdown
- **Genre** : [[Progressive Rock]], [[Heavy Metal]]
```

## 🎯 Cas d'Usage

### 1. Explorer un Genre

**Objectif:** Voir tous les artistes Progressive Rock de votre collection

**Action:**
1. Ouvrir `Musique/Genres/Progressive Rock.md`
2. La section "Artistes/Groupes" liste automatiquement tous les groupes
3. Cliquer sur un artiste pour voir sa fiche complète

**Résultat:** Vous voyez Porcupine Tree, Steven Wilson, Ange, Ayreon, etc.

### 2. Découvrir des Concerts par Style

**Objectif:** Voir tous vos concerts de Jazz

**Action:**
1. Ouvrir `Musique/Genres/Jazz.md`
2. La section "Concerts de ce genre" liste tous les concerts
3. Filtrage automatique via Dataview

**Résultat:** Jazz à Vienne, concerts de Kamasi Washington, Avishai Cohen, etc.

### 3. Navigation Visuelle

**Objectif:** Visualiser les connexions entre genres, artistes et concerts

**Action:**
1. Activer le Graph View dans Obsidian (Ctrl+G / Cmd+G)
2. Cliquer sur un nœud de genre (ex: "Heavy Metal")
3. Observer les liens vers tous les artistes du genre

**Résultat:** Vue graphique montrant le genre au centre avec tous ses artistes connectés

### 4. Identifier des Patterns

**Objectif:** Quel genre écoutez-vous le plus en concert ?

**Action:**
1. Parcourir les pages de genres
2. Comparer le nombre de concerts listés dans chaque genre
3. Identifier vos préférences

**Exemple:**
- Progressive Rock: 15 concerts
- Heavy Metal: 12 concerts
- Jazz: 10 concerts

## 🎨 Fonctionnalités Avancées

### Genres Liés

Chaque page de genre a une section pour documenter :

**Sous-genres:**
- Heavy Metal → Death Metal, Doom Metal, Thrash Metal

**Genres apparentés:**
- Progressive Rock → Art Rock, Psychedelic Rock
- Jazz → Jazz Fusion, Jazz-Rock

### Artistes Représentatifs

Ajoutez manuellement les artistes emblématiques du genre :

**Heavy Metal:**
- Iron Maiden
- Judas Priest
- Black Sabbath

### Notes et Descriptions

Personnalisez chaque page avec :
- Historique du genre
- Caractéristiques musicales
- Votre relation personnelle avec le style

## 📈 Statistiques par Genre

### Top 5 Genres (par nombre d'artistes)

1. **Jazz** - 8 artistes
2. **Progressive Rock** - 6 artistes
3. **Heavy Metal** - 5 artistes
4. **Funk** - 5 artistes
5. **Progressive Metal** - 4 artistes

### Genres les Plus Vus en Concert

Basé sur les queries Dataview, vous pouvez identifier :
- Quels genres dominent vos concerts
- Quels styles vous explorez le plus
- Évolution de vos goûts dans le temps

## 🔍 Recherche et Filtrage

### Trouver tous les artistes d'un pays ET d'un genre

**Query personnalisée:**
```dataview
TABLE genre, formation
FROM "Musique/Groupes"
WHERE contains(genre, "Progressive Rock") AND pays-origine = "France"
```

**Résultat:** Ange, Magma, etc.

### Concerts d'un genre dans une ville

**Query personnalisée:**
```dataview
TABLE date, groupes
FROM "Musique/Concerts"
FLATTEN groupes as groupe_name
WHERE contains(file(groupe_name).genre, "Jazz") AND ville = "Vienne"
SORT date DESC
```

**Résultat:** Tous les concerts de Jazz à Vienne

## 💡 Conseils d'Utilisation

### 1. Personnalisation

Enrichissez les pages de genres avec :
- Descriptions personnelles
- Liens vers playlists Spotify
- Notes sur votre découverte du genre

### 2. Graph View

Pour une meilleure visualisation :
- Filtrer par tag `#genre`
- Colorer les nœuds par type
- Zoomer sur un genre spécifique

### 3. Maintenance

Lors de l'ajout d'un nouvel artiste :
- Utilisez toujours des liens wiki pour les genres : `[[Genre]]`
- Vérifiez que le genre existe dans `Musique/Genres/`
- Créez un nouveau genre si nécessaire avec le template

### 4. Recherche Rapide

Dans Obsidian :
- `Ctrl+O` / `Cmd+O` pour rechercher rapidement
- Tapez le nom du genre
- Accès immédiat à la page

## 🎼 Exemples Concrets

### Page Heavy Metal

**Artistes automatiquement listés:**
- Iron Maiden (UK, 1975)
- Judas Priest (UK, 1969)
- Blue Öyster Cult (US, 1967)

**Concerts automatiquement listés:**
- 2025-07-19: Iron Maiden @ Paris
- 2023-06-15: Iron Maiden @ Hellfest
- 2019-01-27: Judas Priest @ Paris

### Page Progressive Rock

**Artistes automatiquement listés:**
- Porcupine Tree (UK, 1987)
- Steven Wilson (UK, solo 2008)
- Ange (France, 1969)
- Ayreon (Pays-Bas, 1995)
- Steve Hackett (UK, solo 1975)
- Wishbone Ash (UK, 1969)
- Nick Mason's Saucerful of Secrets (UK, 2018)

**Concerts du genre:** 10+ concerts automatiquement listés

### Page Jazz

**Artistes de Jazz pur + sous-genres:**
- Kamasi Washington (Spiritual Jazz)
- Avishai Cohen (Jazz)
- Ron Carter (Jazz)
- Snarky Puppy (Jazz Fusion)
- Jacob Collier (Jazz/Pop/Soul)

**Concerts:** Jazz à Vienne principalement

## 🚀 Évolutions Futures

### Extensions Possibles

1. **Statistiques par genre**
   - Nombre moyen de concerts par genre/an
   - Évolution temporelle

2. **Playlist automatiques**
   - Liens vers Spotify/YouTube
   - Listes basées sur votre collection

3. **Découverte**
   - Genres à explorer (peu de concerts)
   - Recommandations basées sur les genres liés

4. **Timeline**
   - Visualiser l'évolution de vos goûts
   - Chronologie des genres découverts

## ✅ Avantages du Système

**Organisation:**
- Vue claire de votre collection par style
- Navigation intuitive entre entités

**Découverte:**
- Identifier des patterns dans vos goûts
- Trouver des artistes similaires

**Maintenance:**
- Liens automatiques via Dataview
- Pas de mise à jour manuelle nécessaire

**Visualisation:**
- Graph view montre les connexions
- Vue d'ensemble de votre écosystème musical

**Extensibilité:**
- Facile d'ajouter nouveaux genres
- Template standardisé
- Queries réutilisables
