---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2025-11-23 - Drowned, Stargazer, Liquid Flesh
tags:
- salle
type: salle
ville: Lyon
---

# 🏛️ Brin de Zinc

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