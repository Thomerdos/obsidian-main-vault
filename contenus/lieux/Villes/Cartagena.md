---
concerts: []
festivals: []
pays: Espagne
region: null
salles: []
tags:
- ville
type: ville
ville-concerts: 2024-06-21 - Rock Imperium Festival
ville-festivals: Rock Imperium Festival
---

# 🏙️ Cartagena

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