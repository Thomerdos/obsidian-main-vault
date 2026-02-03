---
concerts: []
continent: Europe
festivals: []
groupes-origine: []
pays-concerts: 2016-07-01 - Be Prog! My Friend
pays-villes: Cartagena
salles: []
tags:
- pays
type: pays
villes: []
---

# 🌍 Espagne

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