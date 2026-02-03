# 🎸 Structure de Gestion des Concerts Obsidian

Ce vault contient une structure complète et évolutive pour gérer les concerts, groupes, salles, festivals, villes et pays dans Obsidian, avec des templates réutilisables et des relations automatiques via Dataview.

## 📂 Structure des Dossiers

```
obsidian-main-vault/
├── Musique/
│   ├── Concerts.md              # Index principal des concerts
│   ├── _templates/              # Templates pour nouveaux éléments
│   │   ├── template-concert.md
│   │   ├── template-groupe.md
│   │   ├── template-salle.md
│   │   └── template-festival.md
│   ├── Concerts/                # Fiches individuelles de concerts
│   │   ├── 2013/
│   │   ├── 2015/
│   │   ├── 2016/
│   │   ├── 2017/
│   │   ├── 2018/
│   │   ├── 2019/
│   │   ├── 2022/
│   │   ├── 2023/
│   │   ├── 2024/
│   │   ├── 2025/
│   │   └── 2026/
│   ├── Groupes/                 # Pages des artistes/groupes
│   ├── Festivals/               # Pages des festivals récurrents
│   └── Salles/                  # Pages des lieux de concert
│
└── Lieux/                       # Organisation géographique
    ├── _templates/
    │   ├── template-ville.md
    │   └── template-pays.md
    ├── Villes/
    └── Pays/
```

## 🎯 Utilisation

### 📅 Consulter les Concerts

Le fichier principal [`Musique/Concerts.md`](Musique/Concerts.md) contient :
- Liste complète des concerts passés et à venir
- Liens vers les fiches détaillées de chaque concert
- Queries Dataview pour visualiser les statistiques

### ✍️ Ajouter un Nouveau Concert

1. Copier le template : `Musique/_templates/template-concert.md`
2. Créer un nouveau fichier dans `Musique/Concerts/ANNÉE/` avec le format : `YYYY-MM-DD - Nom.md`
3. Remplir le frontmatter YAML :
   ```yaml
   ---
   type: concert
   date: YYYY-MM-DD
   groupes: ["Groupe 1", "Groupe 2"]
   salle: Nom de la salle
   festival: Nom du festival (si applicable)
   ville: Nom de la ville
   pays: Nom du pays
   rating:
   tags:
     - concert
   ---
   ```
4. Compléter les sections (Setlist, Notes, Photos)
5. Ajouter une ligne dans `Concerts.md` pour référencer le nouveau concert

### 🎤 Ajouter un Nouveau Groupe

1. Copier le template : `Musique/_templates/template-groupe.md`
2. Créer un fichier dans `Musique/Groupes/` avec le nom du groupe
3. La query Dataview affichera automatiquement tous les concerts où ce groupe a joué

### 🏛️ Ajouter une Nouvelle Salle

1. Copier le template : `Musique/_templates/template-salle.md`
2. Créer un fichier dans `Musique/Salles/`
3. Renseigner la ville et le pays dans le frontmatter
4. La query Dataview listera automatiquement tous les concerts dans cette salle

### 🎪 Ajouter un Nouveau Festival

1. Copier le template : `Musique/_templates/template-festival.md`
2. Créer un fichier dans `Musique/Festivals/`
3. Renseigner la ville et le pays
4. Les éditions visitées seront listées automatiquement via Dataview

## 🔗 Relations Automatiques

Grâce aux queries Dataview intégrées dans les templates, les relations sont automatiquement créées :

- **Depuis un Groupe** → Liste de tous les concerts où ce groupe a joué
- **Depuis une Salle** → Liste de tous les concerts dans cette salle
- **Depuis un Festival** → Liste de toutes les éditions visitées
- **Depuis une Ville** → Liste des salles et concerts dans cette ville
- **Depuis un Pays** → Liste des villes visitées et concerts dans ce pays

## 📊 Statistiques Disponibles

Dans [`Musique/Concerts.md`](Musique/Concerts.md), vous trouverez :
- Nombre de concerts par année
- Groupes les plus vus
- Salles préférées
- Festivals visités
- Villes visitées

## 🎨 Fonctionnalités

### Frontmatter Structuré

Chaque type d'entité a son propre frontmatter YAML pour permettre des requêtes avancées :
- **Concerts** : date, groupes, salle, festival, ville, pays, rating
- **Groupes** : genre, pays-origine, formation, site-web
- **Salles** : ville, pays, capacite, adresse
- **Festivals** : ville, pays, periode, editions-vues
- **Villes** : pays, region
- **Pays** : continent

### Queries Dataview

Exemples de queries disponibles :
```dataview
TABLE groupes as "Artistes", salle as "Salle", ville as "Ville"
FROM "Musique/Concerts/2025"
SORT date DESC
```

```dataview
TABLE length(rows.file.link) as "Nombre de fois"
FROM "Musique/Concerts"
FLATTEN groupes as groupe
GROUP BY groupe
SORT length(rows.file.link) DESC
LIMIT 10
```

## 🛠️ Migration

Un script Python (`scripts/migrate-concerts.py`) a été utilisé pour créer automatiquement :
- 56 fiches de concerts individuelles
- 15 pages de salles
- 12 pages de festivals  
- 14 pages de villes
- 5 pages de pays
- 6 templates réutilisables

## 📝 Notes

- Les fichiers existants (groupes, festivals, salles, villes) ont été préservés
- Les anciens dossiers `Villes/` et `Pays/` ont été migrés vers `Lieux/`
- L'ancien dossier `Salles de concert/` a été renommé en `Salles/`
- Tous les liens wiki sont préservés et fonctionnels

## 🚀 Prochaines Étapes

Pour améliorer encore le système :
1. Ajouter des photos aux fiches de concerts
2. Compléter les informations des groupes (genres, albums)
3. Ajouter des liens Spotify/Bandcamp
4. Enrichir les notes de concerts avec setlists détaillés
5. Ajouter des ratings et reviews
