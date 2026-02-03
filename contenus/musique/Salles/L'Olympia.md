---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2025-06-02 - Blue Öyster Cult
tags:
- salle
type: salle
ville: Paris
---

# 🏛️ L'Olympia

## 📍 Localisation

- **Ville** : [[Paris]]
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