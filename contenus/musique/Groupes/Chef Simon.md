---
formation: null
genre:
- '[[Autre]]'
pays-origine: '[[France]]'
site-web: null
tags:
- groupe
type: groupe
parent: '[[Groupes]]'
---

# 🎤 Chef Simon

## 📊 Informations

- **Genre** : [[Autre]]
- **Pays** : [[France]]
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