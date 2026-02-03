---
pays: '[[Italie]]'
region: null
tags:
- ville
type: ville
parent: '[[Villes]]'
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