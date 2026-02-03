---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2024-01-31 - The Notwist
tags:
- salle
type: salle
ville: Lyon
---

# 🏛️ L'Épicerie Moderne

## 📍 Localisation

- **Ville** : [[Lyon]]
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