---
adresse: null
capacite: null
concerts: []
pays: France
salle-concerts: 2023-03-02 - King Gizzard & The Lizard Wizard
tags:
- salle
type: salle
ville: Paris
---

# 🏛️ Zénith de Paris

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