---
concerts: []
festivals: []
pays: Italie
region: null
salles: []
tags:
- ville
type: ville
ville-concerts: 2017-09-01 - 2Days Prog + 1
ville-festivals: 2Days Prog + 1
---

# 🏙️ Veruno

## 📍 Localisation

- **Pays** : [[Italie]]
- **Région** : 

## 🎵 Salles de concert

```dataview
LIST
FROM "Musique/Salles"
WHERE contains(ville, this.file.name)
```

## 🎪 Concerts & Festivals

```dataview
TABLE date as "Date", groupes as "Artistes", salle as "Salle"
FROM "Musique/Concerts"
WHERE contains(ville, this.file.name)
SORT date DESC
```

## 📝 Notes