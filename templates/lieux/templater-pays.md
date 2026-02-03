<%*
// ========================================
// TEMPLATER PAYS - Template interactif
// ========================================

// 1. COLLECTE DES INFORMATIONS
const nomPays = await tp.system.prompt("Nom du pays", "");
const continent = await tp.system.prompt("Continent", "");

// 2. DÉPLACER LE FICHIER AU BON ENDROIT
await tp.file.move(`Lieux/Pays/${nomPays}`);

-%>
---
type: pays
continent: <% continent %>
tags:
  - pays
---

# 🌍 <% nomPays %>

## 📍 Localisation

- **Continent** : <% continent %>

## 🏙️ Villes visitées

```dataview
LIST
FROM "Lieux/Villes"
WHERE contains(pays, this.file.name)
```

## 🎪 Concerts & Festivals

```dataview
TABLE date as "Date", groupes as "Artistes", ville as "Ville"
FROM "Musique/Concerts"
WHERE contains(pays, this.file.name)
SORT date DESC
```

## 📝 Notes


