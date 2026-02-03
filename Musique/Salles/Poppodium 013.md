---
type: salle
ville: Tilburg
pays: Pays-Bas
capacite: 
adresse: 
tags:
  - salle
---

# 🏛️ Poppodium 013

## 📍 Localisation

- **Ville** : [[Tilburg]]
- **Pays** : [[Pays-Bas]]
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
