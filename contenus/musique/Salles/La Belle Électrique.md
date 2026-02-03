---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2015-12-11 - Ghost
tags:
- salle
type: salle
ville: Grenoble
---

# 🏛️ La Belle Électrique

## 📍 Localisation

- **Ville** : [[Grenoble]]
- **Pays** : [[France]]
- **Adresse** : 
- **Capacité** : 

## 🎫 Concerts vus ici

```dataview
TABLE date as "Date", groupes as "Artistes"
FROM "Musique/Concerts"
WHERE contains(salle, this.file.name)
SORT date DESC
```

## 💭 Notes



## 🔗 Liens

- [Site officiel]()
- [Google Maps]()