---
adresse: null
capacite: null
pays: '[[France]]'
tags:
- salle
type: salle
ville: '[[Paris]]'
parent: '[[Salles]]'
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
FROM "contenus/musique/Concerts"
WHERE contains(salle, this.file.name)
SORT date DESC
```

## 💭 Notes



## 🔗 Liens

- [Site officiel]()
- [Google Maps]()