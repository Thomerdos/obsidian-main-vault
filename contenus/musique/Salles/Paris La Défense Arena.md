---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2025-07-19 - Iron Maiden
tags:
- salle
type: salle
ville: Paris
---

# 🏛️ Paris La Défense Arena

## 📍 Localisation

- **Ville** : [[Paris]]
- **Pays** : [[France]]
- **Adresse** : 
- **Capacité** : 

## 🎫 Concerts vus ici

```dataview
TABLE date as "Date", groupes as "Artistes"
FROM "contenus/musique/Concerts"
WHERE contains(salle, this.file.name)
SORT date DESC
```

## 💭 Notes



## 🔗 Liens

- [Site officiel]()
- [Google Maps]()