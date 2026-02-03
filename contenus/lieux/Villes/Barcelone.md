---
concerts: []
festivals: []
pays: Espagne
region: null
salles: []
tags:
- ville
type: ville
ville-concerts: 2016-07-01 - Be Prog! My Friend
ville-festivals: Be Prog! My Friend
---

# 🏙️ Barcelone

## 📍 Localisation

- **Pays** : [[Espagne]]
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