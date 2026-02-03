---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2026-02-07 - Sinner G's, Teodoro Lopes
tags:
- salle
type: salle
ville: Grenoble
---

# 🏛️ Michel Musique

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