---
concerts: []
continent: Amérique du Nord
festivals: []
groupes-origine: []
salles: []
tags:
- pays
type: pays
villes: []
---

# 🌍 États-Unis

## 📍 Localisation

- **Continent** : Amérique du Nord

## 🏙️ Villes visitées

```dataview
LIST
FROM "contenus/lieux/Villes"
WHERE contains(pays, this.file.name)
```

## 🎪 Concerts & Festivals

```dataview
TABLE date as "Date", groupes as "Artistes", ville as "Ville"
FROM "contenus/musique/Concerts"
WHERE contains(pays, this.file.name)
SORT date DESC
```

## 📝 Notes