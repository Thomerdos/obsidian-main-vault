---
formation: null
genre: []
pays-origine: null
site-web: null
tags:
- groupe
type: groupe
parent: '[[Groupes]]'
---

# 🎤 Teodoro Lopes

## 📊 Informations

- **Genre** : 
- **Pays** : [[]]
- **Formation** : 
- **Site web** : 

## 🎸 Albums favoris

- 

## 🎪 Concerts vus

```dataview
TABLE date as "Date", salle as "Salle", ville as "Ville"
FROM "contenus/musique/Concerts"
WHERE contains(groupes, this.file.name)
SORT date DESC
```

## 💭 Notes



## 🔗 Liens

- [Spotify]()
- [Bandcamp]()
- [Site officiel]()