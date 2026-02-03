---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2018-07-01 - Steve Hackett
tags:
- salle
type: salle
ville: Grenoble
---

# 🏛️ Radiant-Bellevue

## 📍 Localisation

- **Ville** : [[Grenoble]]
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