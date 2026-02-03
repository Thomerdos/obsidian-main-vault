---
type: ville
pays: Pays-Bas
region: 
tags:
  - ville
---

# 🏙️ Tilburg

## 📍 Localisation

- **Pays** : [[Pays-Bas]]
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


