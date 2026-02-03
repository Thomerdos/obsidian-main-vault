---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2025-05-28 - Steven Wilson
tags:
- salle
type: salle
ville: Lyon
---

# 🏛️ Bourse du Travail

## 📍 Localisation

- **Ville** : [[Lyon]]
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