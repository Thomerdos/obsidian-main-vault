---
type: salle
ville: 
pays: 
capacite: 
adresse: 
tags:
  - salle
---

# 🏛️ 

## 📍 Localisation

- **Ville** : [[]]
- **Pays** : [[]]
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
