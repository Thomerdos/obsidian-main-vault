---
concerts: []
festivals: []
pays: France
region: null
salles: []
tags:
- ville
type: ville
ville-concerts: 2025-08-14 - Motocultor Festival
ville-festivals: Motocultor Festival
---

# 🏙️ Carhaix

## 📍 Localisation

- **Pays** : [[France]]
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