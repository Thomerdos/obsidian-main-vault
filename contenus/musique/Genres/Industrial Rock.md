---
children: []
groupes: []
parent: ''
related: []
tags:
- genre
type: genre
---

# 🎵 Industrial Rock

## 📊 Description

Genre musical : Industrial Rock

## 🎤 Artistes/Groupes

```dataview
TABLE pays-origine as "Pays", formation as "Formation"
FROM "contenus/musique/Groupes"
WHERE contains(genre, this.file.name)
SORT file.name ASC
```

## 🎸 Concerts de ce genre

```dataview
TABLE date as "Date", groupes as "Artistes", ville as "Ville"
FROM "contenus/musique/Concerts"
FLATTEN groupes as groupe_name
WHERE contains(file(groupe_name).genre, this.file.name)
SORT date DESC
LIMIT 50
```

## 🔗 Genres liés

### Sous-genres
- 

### Genres apparentés
- 

## ⭐ Artistes représentatifs

- 

## 📝 Notes