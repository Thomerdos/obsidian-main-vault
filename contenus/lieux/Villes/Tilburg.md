---
concerts: []
festivals: []
pays: Pays-Bas
region: null
salles: []
tags:
- ville
type: ville
ville-concerts: 2023-09-16 - Ayreon
ville-festivals: Roadburn Festival
ville-salles: Poppodium 013
---

# 🏙️ Tilburg

## 📍 Localisation

- **Pays** : [[Pays-Bas]]
- **Région** : 

## 🎵 Salles de concert

```dataview
LIST
FROM "contenus/musique/Salles"
WHERE contains(ville, this.file.name)
```

## 🎪 Concerts & Festivals

```dataview
TABLE date as "Date", groupes as "Artistes", salle as "Salle"
FROM "contenus/musique/Concerts"
WHERE contains(ville, this.file.name)
SORT date DESC
```

## 📝 Notes