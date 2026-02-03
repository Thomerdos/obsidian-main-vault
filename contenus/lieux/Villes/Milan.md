---
concerts: []
festivals: []
pays: Italie
region: null
salles: []
tags:
- ville
type: ville
ville-concerts: 2024-07-18 - Nick Mason's Saucerful of Secrets
---

# 🏙️ Milan

## 📍 Localisation

- **Pays** : [[Italie]]
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