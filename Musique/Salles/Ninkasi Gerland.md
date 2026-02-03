---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2023-05-10 - Wishbone Ash
tags:
- salle
type: salle
ville: Lyon
---

# 🏛️ Ninkasi Gerland

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