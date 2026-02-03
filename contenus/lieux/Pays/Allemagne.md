---
concerts: []
continent: Europe
festivals: []
groupes-origine: []
pays-concerts: 2025-07-17 - Chaos Descends Festival
pays-villes: Crispendorf
salles: []
tags:
- pays
type: pays
villes: []
---

# 🌍 Allemagne

## 📍 Localisation

- **Continent** : Europe

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