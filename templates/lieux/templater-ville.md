<%*
// ========================================
// TEMPLATER VILLE - Template interactif avec gestion des doublons
// ========================================

// FONCTION: Récupérer tous les fichiers d'un dossier
function getFilesInFolder(folderPath) {
    const folder = app.vault.getAbstractFileByPath(folderPath);
    if (!folder || !folder.children) return [];
    return folder.children
        .filter(f => f.extension === 'md')
        .map(f => f.basename)
        .sort();
}

// FONCTION: Trouver des correspondances approximatives
function findSimilar(input, list) {
    if (!input || input.length < 2) return [];
    const inputLower = input.toLowerCase();
    return list.filter(item => 
        item.toLowerCase().includes(inputLower) || 
        inputLower.includes(item.toLowerCase())
    );
}

// 1. RÉCUPÉRER LES LISTES EXISTANTES
const paysExistants = getFilesInFolder("Lieux/Pays");

// 2. COLLECTE DES INFORMATIONS
const nomVille = await tp.system.prompt("Nom de la ville", "");

let paysInput = await tp.system.prompt(
    `Pays${paysExistants.length > 0 ? `\n\nExistant: ${paysExistants.slice(0, 10).join(", ")}` : ""}`, 
    "France"
);

// Vérifier le pays
let paysFinal = paysInput;
if (paysInput && !paysExistants.includes(paysInput)) {
    const similaires = findSimilar(paysInput, paysExistants);
    if (similaires.length > 0) {
        paysFinal = await tp.system.prompt(
            `⚠️ "${paysInput}" n'existe pas exactement.\nSimilaires: ${similaires.join(", ")}\n\nUtiliser un existant ou confirmer "${paysInput}"?`,
            similaires[0]
        );
    }
}

const region = await tp.system.prompt("Région (optionnel)", "");

// 3. CRÉER LE PAYS SI NÉCESSAIRE
const paysPath = `Lieux/Pays/${paysFinal}.md`;
const paysFile = app.vault.getAbstractFileByPath(paysPath);
if (!paysFile) {
    const paysContent = `---
type: pays
continent: 
tags:
  - pays
---

# 🌍 ${paysFinal}

## 📍 Localisation

- **Continent** : 

## 🏙️ Villes visitées

\`\`\`dataview
LIST
FROM "Lieux/Villes"
WHERE contains(pays, this.file.name)
\`\`\`

## 🎪 Concerts & Festivals

\`\`\`dataview
TABLE date as "Date", groupes as "Artistes", ville as "Ville"
FROM "Musique/Concerts"
WHERE contains(pays, this.file.name)
SORT date DESC
\`\`\`

## 📝 Notes


`;
    await app.vault.create(paysPath, paysContent);
}

// 4. DÉPLACER LE FICHIER AU BON ENDROIT
await tp.file.move(`Lieux/Villes/${nomVille}`);

-%>
---
type: ville
pays: <% paysFinal %>
region: <% region %>
tags:
  - ville
---

# 🏙️ <% nomVille %>

## 📍 Localisation

- **Pays** : [[<% paysFinal %>]]
- **Région** : <% region %>

## 🎵 Salles de concert

```dataview
LIST
FROM "Musique/Salles"
WHERE contains(ville, this.file.name)
```

## 🎪 Concerts & Festivals

```dataview
TABLE date as "Date", groupes as "Artistes", salle as "Salle"
FROM "Musique/Concerts"
WHERE contains(ville, this.file.name)
SORT date DESC
```

## 📝 Notes


