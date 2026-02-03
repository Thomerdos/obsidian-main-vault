---
continent: Europe
tags:
- pays
type: pays
parent: '[[Pays]]'
---

# 🌍 Royaume-Uni

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