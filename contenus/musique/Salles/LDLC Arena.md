---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2025-04-26 - Ghost
tags:
- salle
type: salle
ville: Lyon
---

# 🏛️ LDLC Arena

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