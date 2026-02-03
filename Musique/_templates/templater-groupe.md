<%*
// ========================================
// TEMPLATER GROUPE - Template interactif avec gestion des doublons
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
const genresExistants = getFilesInFolder("Musique/Genres");
const paysExistants = getFilesInFolder("Lieux/Pays");

// 2. COLLECTE DES INFORMATIONS
const nomGroupe = await tp.system.prompt("Nom du groupe/artiste", "");

let genresInput = await tp.system.prompt(
    `Genre(s) (séparés par des virgules)${genresExistants.length > 0 ? `\n\nExistant: ${genresExistants.slice(0, 10).join(", ")}` : ""}`,
    ""
);

let paysOrigine = await tp.system.prompt(
    `Pays d'origine${paysExistants.length > 0 ? `\n\nExistant: ${paysExistants.slice(0, 10).join(", ")}` : ""}`,
    ""
);

const anneeFormation = await tp.system.prompt("Année de formation (optionnel)", "");
const siteWeb = await tp.system.prompt("Site web (optionnel)", "");

// 3. TRAITEMENT DES GENRES
const genres = genresInput.split(',').map(g => g.trim()).filter(g => g);
const genresFinaux = [];

for (const genre of genres) {
    if (genre && !genresExistants.includes(genre)) {
        const similaires = findSimilar(genre, genresExistants);
        if (similaires.length > 0) {
            const correction = await tp.system.prompt(
                `⚠️ "${genre}" n'existe pas exactement.\nSimilaires: ${similaires.join(", ")}\n\nUtiliser un existant ou confirmer "${genre}"?`,
                similaires[0]
            );
            genresFinaux.push(correction);
        } else {
            genresFinaux.push(genre);
        }
    } else if (genre) {
        genresFinaux.push(genre);
    }
}

// 4. VÉRIFIER LE PAYS
let paysFinal = paysOrigine;
if (paysOrigine && !paysExistants.includes(paysOrigine)) {
    const similaires = findSimilar(paysOrigine, paysExistants);
    if (similaires.length > 0) {
        paysFinal = await tp.system.prompt(
            `⚠️ "${paysOrigine}" n'existe pas exactement.\nSimilaires: ${similaires.join(", ")}\n\nUtiliser un existant ou confirmer "${paysOrigine}"?`,
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

// 6. CRÉER LES GENRES SI NÉCESSAIRES
for (const genre of genresFinaux) {
    const genrePath = `Musique/Genres/${genre}.md`;
    const genreFile = app.vault.getAbstractFileByPath(genrePath);
    if (!genreFile) {
        const genreContent = `---
type: genre
tags:
  - genre
---

# 🎵 ${genre}

## 📊 Description

Genre musical : 

## 🎤 Artistes/Groupes

\`\`\`dataview
TABLE pays-origine as "Pays", formation as "Formation"
FROM "Musique/Groupes"
WHERE contains(genre, this.file.name)
SORT file.name ASC
\`\`\`

## 🎸 Concerts de ce genre

\`\`\`dataview
TABLE date as "Date", groupes as "Artistes", ville as "Ville"
FROM "Musique/Concerts"
FLATTEN groupes as groupe_name
WHERE contains(file(groupe_name).genre, this.file.name)
SORT date DESC
LIMIT 50
\`\`\`

## 🔗 Genres liés

### Sous-genres
- 

### Genres apparentés
- 

## ⭐ Artistes représentatifs

- 

## 📝 Notes


`;
        await app.vault.create(genrePath, genreContent);
    }
}

// 7. DÉPLACER LE FICHIER AU BON ENDROIT
await tp.file.move(`Musique/Groupes/${nomGroupe}`);

-%>
---
type: groupe
genre: [<% genresFinaux.map(g => `"${g}"`).join(", ") %>]
pays-origine: <% paysFinal %>
formation: <% anneeFormation %>
site-web: <% siteWeb %>
tags:
  - groupe
---

# 🎤 <% nomGroupe %>

## 📊 Informations

- **Genre** : <% genresFinaux.map(g => `[[${g}]]`).join(", ") %>
- **Pays** : [[<% paysFinal %>]]
- **Formation** : <% anneeFormation %>
- **Site web** : <% siteWeb ? `[${siteWeb}](${siteWeb})` : "" %>

## 🎸 Albums favoris

- 

## 🎪 Concerts vus

```dataview
TABLE date as "Date", salle as "Salle", ville as "Ville"
FROM "Musique/Concerts"
WHERE contains(groupes, this.file.name)
SORT date DESC
```

## 💭 Notes



## 🔗 Liens

- [Spotify]()
- [Bandcamp]()
- [Site officiel](<% siteWeb %>)
