---
concerts: []
continent: Europe
festivals: []
groupes-origine: []
pays-concerts: 2023-07-23 - Guitare en Scène
pays-villes: Lyon
salles: []
tags:
- pays
type: pays
villes: []
---

# 🌍 France

## 📍 Localisation

- **Continent** : Europe

## 🏙️ Villes visitées

```dataview
LIST
FROM "Lieux/Villes"
WHERE contains(pays, this.file.name)
```

## 🎪 Concerts & Festivals

```dataview
TABLE date as "Date", groupes as "Artistes", ville as "Ville"
FROM "Musique/Concerts"
WHERE contains(pays, this.file.name)
SORT date DESC
```

## 📝 Notes