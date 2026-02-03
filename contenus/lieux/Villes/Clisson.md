---
concerts: []
festivals: []
pays: France
region: null
salles: []
tags:
- ville
type: ville
ville-concerts: 2023-06-15 - Hellfest
ville-festivals: Hellfest
---

# 🏙️ Clisson

## 📍 Localisation

- **Pays** : [[France]]
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