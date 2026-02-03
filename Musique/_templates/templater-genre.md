<%*
// ========================================
// TEMPLATER GENRE - Template interactif
// ========================================

// 1. COLLECTE DES INFORMATIONS
const nomGenre = await tp.system.prompt("Nom du genre musical", "");
const description = await tp.system.prompt("Description du genre (optionnel)", "");

// 2. DÉPLACER LE FICHIER AU BON ENDROIT
await tp.file.move(`Musique/Genres/${nomGenre}`);

-%>
---
type: genre
tags:
  - genre
---

# 🎵 <% nomGenre %>

## 📊 Description

<% description || "Genre musical : " %>

## 🎤 Artistes/Groupes

```dataview
TABLE pays-origine as "Pays", formation as "Formation"
FROM "Musique/Groupes"
WHERE contains(genre, this.file.name)
SORT file.name ASC
```

## 🎸 Concerts de ce genre

```dataview
TABLE date as "Date", groupes as "Artistes", ville as "Ville"
FROM "Musique/Concerts"
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


