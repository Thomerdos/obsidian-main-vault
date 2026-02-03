---
type: salle
ville: Paris
pays: France
capacite: 
adresse: 
tags:
  - salle
---

# 🏛️ Paris La Défense Arena

## 📍 Localisation

- **Ville** : [[Paris]]
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
