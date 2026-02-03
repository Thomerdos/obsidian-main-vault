---
concerts: []
continent: Asoe
festivals: []
groupes-origine: []
salles: []
tags:
- pays
type: pays
villes: []
---

# 🌍 Israël

## 📍 Localisation

- **Continent** : [[Asie]]

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