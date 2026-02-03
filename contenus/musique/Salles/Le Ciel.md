---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2024-04-28 - Bell Witch
tags:
- salle
type: salle
ville: Grenoble
---

# 🏛️ Le Ciel

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