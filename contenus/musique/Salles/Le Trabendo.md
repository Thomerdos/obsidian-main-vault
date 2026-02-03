---
adresse: null
capacite: null
concerts: []
pays: France
tags:
- salle
type: salle
ville: Paris
---

# 🏛️ Le Trabendo

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