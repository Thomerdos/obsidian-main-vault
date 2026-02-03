<%*
// ========================================
// TEMPLATER FESTIVAL - Template interactif avec gestion des doublons
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
const villesExistantes = getFilesInFolder("Lieux/Villes");
const paysExistants = getFilesInFolder("Lieux/Pays");

// 2. COLLECTE DES INFORMATIONS
const nomFestival = await tp.system.prompt("Nom du festival", "");

let ville = await tp.system.prompt(
    `Ville${villesExistantes.length > 0 ? `\n\nExistant: ${villesExistantes.slice(0, 10).join(", ")}` : ""}`,
    ""
);

let pays = await tp.system.prompt(
    `Pays${paysExistants.length > 0 ? `\n\nExistant: ${paysExistants.slice(0, 10).join(", ")}` : ""}`,
    "France"
);

const periode = await tp.system.prompt("Période habituelle (ex: 'Juin', 'Mi-juillet')", "");

// 3. VÉRIFIER LA VILLE
let villeFinal = ville;
if (ville && !villesExistantes.includes(ville)) {
    const similaires = findSimilar(ville, villesExistantes);
    if (similaires.length > 0) {
        villeFinal = await tp.system.prompt(
            `⚠️ "${ville}" n'existe pas exactement.\nSimilaires: ${similaires.join(", ")}\n\nUtiliser un existant ou confirmer "${ville}"?`,
            similaires[0]
        );
    }
}

// 4. VÉRIFIER LE PAYS
let paysFinal = pays;
if (pays && !paysExistants.includes(pays)) {
    const similaires = findSimilar(pays, paysExistants);
    if (similaires.length > 0) {
        paysFinal = await tp.system.prompt(
            `⚠️ "${pays}" n'existe pas exactement.\nSimilaires: ${similaires.join(", ")}\n\nUtiliser un existant ou confirmer "${pays}"?`,
            similaires[0]
        );
    }
}

// 5. CRÉER LE PAYS SI NÉCESSAIRE
if (paysFinal) {
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
}

// 6. CRÉER LA VILLE SI NÉCESSAIRE
if (villeFinal) {
    const villePath = `Lieux/Villes/${villeFinal}.md`;
    const villeFile = app.vault.getAbstractFileByPath(villePath);
    if (!villeFile) {
        const villeContent = `---
type: ville
pays: ${paysFinal}
region: 
tags:
  - ville
---

# 🏙️ ${villeFinal}

## 📍 Localisation

- **Pays** : [[${paysFinal}]]
- **Région** : 

## 🎵 Salles de concert

\`\`\`dataview
LIST
FROM "Musique/Salles"
WHERE contains(ville, this.file.name)
\`\`\`

## 🎪 Concerts & Festivals

\`\`\`dataview
TABLE date as "Date", groupes as "Artistes", salle as "Salle"
FROM "Musique/Concerts"
WHERE contains(ville, this.file.name)
SORT date DESC
\`\`\`

## 📝 Notes


`;
        await app.vault.create(villePath, villeContent);
    }
}

// 7. DÉPLACER LE FICHIER AU BON ENDROIT
await tp.file.move(`Musique/Festivals/${nomFestival}`);

-%>
---
type: festival
ville: <% villeFinal %>
pays: <% paysFinal %>
periode: <% periode %>
editions-vues: []
tags:
  - festival
---

# 🎪 <% nomFestival %>

## 📊 Informations

- **Lieu** : [[<% villeFinal %>]] - [[<% paysFinal %>]]
- **Période habituelle** : <% periode %>
- **Site web** : 

## 🗓️ Éditions visitées

```dataview
TABLE date as "Date", groupes as "Groupes vus"
FROM "Musique/Concerts"
WHERE contains(festival, this.file.name)
SORT date DESC
```

## 💭 Notes & Souvenirs



## 🔗 Liens

- [Site officiel]()
