---
type: salle
ville: Grenoble
pays: France
capacite: 
adresse: 
tags:
  - salle
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
FROM "Musique/Concerts"
WHERE contains(salle, this.file.name)
SORT date DESC
```

## 💭 Notes



## 🔗 Liens

- [Site officiel]()
- [Google Maps]()
