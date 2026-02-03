---
adresse: null
capacite: null
pays: '[[Pays-Bas]]'
tags:
- salle
type: salle
ville: '[[Tilburg]]'
parent: '[[Salles]]'
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
FROM "contenus/musique/Concerts"
WHERE contains(salle, this.file.name)
SORT date DESC
```

## 💭 Notes



## 🔗 Liens

- [Site officiel]()
- [Google Maps]()