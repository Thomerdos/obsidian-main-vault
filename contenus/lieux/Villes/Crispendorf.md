---
concerts: []
festivals: []
pays: Allemagne
region: null
salles: []
tags:
- ville
type: ville
ville-concerts: 2025-07-17 - Chaos Descends Festival
ville-festivals: Chaos Descends Festival
---

# 🏙️ Crispendorf

## 📍 Localisation

- **Pays** : [[Allemagne]]
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