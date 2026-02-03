<%*
// ========================================
// TEMPLATER CONCERT - Template interactif avec gestion des doublons
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

// FONCTION: Prompt avec suggestions
async function promptWithSuggestions(message, existingList, defaultValue = "") {
    if (existingList.length > 0) {
        const listStr = existingList.slice(0, 10).join(", ");
        const suffix = existingList.length > 10 ? `, ... (${existingList.length - 10} de plus)` : "";
        message += `\n\nExistant: ${listStr}${suffix}`;
    }
    return await tp.system.prompt(message, defaultValue);
}

// 1. RÉCUPÉRER LES LISTES EXISTANTES
const groupesExistants = getFilesInFolder("Musique/Groupes");
const sallesExistantes = getFilesInFolder("Musique/Salles");
const festivalsExistants = getFilesInFolder("Musique/Festivals");
const villesExistantes = getFilesInFolder("Lieux/Villes");
const paysExistants = getFilesInFolder("Lieux/Pays");

// 2. COLLECTE DES INFORMATIONS via prompts avec suggestions
const dateInput = await tp.system.prompt("Date du concert (YYYY-MM-DD)", tp.date.now("YYYY-MM-DD"));

const groupesInput = await promptWithSuggestions(
    "Groupes (séparés par des virgules)", 
    groupesExistants
);

const salleInput = await promptWithSuggestions(
    "Salle (laisser vide si festival)", 
    sallesExistantes
);

const festivalInput = await promptWithSuggestions(
    "Festival (laisser vide si concert en salle)", 
    festivalsExistants
);

const villeInput = await promptWithSuggestions(
    "Ville", 
    villesExistantes
);

const paysInput = await promptWithSuggestions(
    "Pays", 
    paysExistants,
    "France"
);

const notesInput = await tp.system.prompt("Notes initiales (optionnel)", "");

// 3. VÉRIFICATION DES DOUBLONS ET CORRECTIONS
const groupes = groupesInput.split(',').map(g => g.trim()).filter(g => g);

// Vérifier les doublons potentiels pour chaque groupe
const groupesFinaux = [];
for (const groupe of groupes) {
    const similaires = findSimilar(groupe, groupesExistants);
    if (similaires.length > 0 && !similaires.includes(groupe)) {
        const correction = await tp.system.prompt(
            `⚠️ "${groupe}" n'existe pas exactement.\nSimilaires trouvés: ${similaires.join(", ")}\n\nUtiliser un existant ou confirmer "${groupe}"?`,
            similaires[0]
        );
        groupesFinaux.push(correction);
    } else {
        groupesFinaux.push(groupe);
    }
}

// Vérifier la salle
let salleFinal = salleInput;
if (salleInput && !sallesExistantes.includes(salleInput)) {
    const similaires = findSimilar(salleInput, sallesExistantes);
    if (similaires.length > 0) {
        salleFinal = await tp.system.prompt(
            `⚠️ "${salleInput}" n'existe pas exactement.\nSimilaires: ${similaires.join(", ")}\n\nUtiliser un existant ou confirmer "${salleInput}"?`,
            similaires[0]
        );
    }
}

// Vérifier le festival
let festivalFinal = festivalInput;
if (festivalInput && !festivalsExistants.includes(festivalInput)) {
    const similaires = findSimilar(festivalInput, festivalsExistants);
    if (similaires.length > 0) {
        festivalFinal = await tp.system.prompt(
            `⚠️ "${festivalInput}" n'existe pas exactement.\nSimilaires: ${similaires.join(", ")}\n\nUtiliser un existant ou confirmer "${festivalInput}"?`,
            similaires[0]
        );
    }
}

// Vérifier la ville
let villeFinal = villeInput;
if (villeInput && !villesExistantes.includes(villeInput)) {
    const similaires = findSimilar(villeInput, villesExistantes);
    if (similaires.length > 0) {
        villeFinal = await tp.system.prompt(
            `⚠️ "${villeInput}" n'existe pas exactement.\nSimilaires: ${similaires.join(", ")}\n\nUtiliser un existant ou confirmer "${villeInput}"?`,
            similaires[0]
        );
    }
}

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

// 4. TRAITEMENT DES DONNÉES
const premierGroupe = groupesFinaux[0] || "Concert";
const lieu = festivalFinal || salleFinal || villeFinal;
const isPassé = dateInput <= tp.date.now("YYYY-MM-DD");
const checkbox = isPassé ? "[x]" : "[ ]";

// 5. EXTRAIRE L'ANNÉE POUR LE CHEMIN
const année = dateInput.substring(0, 4);

// 6. GÉNÉRER LE NOM DU FICHIER
const nomFichier = festivalFinal ? `${dateInput} - ${festivalFinal}` : `${dateInput} - ${premierGroupe}`;

// 7. CRÉER LE DOSSIER DE L'ANNÉE SI NÉCESSAIRE
const dossierAnnée = `Musique/Concerts/${année}`;
const dossierAbsolu = app.vault.getAbstractFileByPath(dossierAnnée);
if (!dossierAbsolu) {
    await app.vault.createFolder(dossierAnnée);
}

// 8. CRÉER LES ENTITÉS LIÉES SI ELLES N'EXISTENT PAS

// 8.1. Créer les groupes
for (const groupe of groupesFinaux) {
    const groupePath = `Musique/Groupes/${groupe}.md`;
    const groupeFile = app.vault.getAbstractFileByPath(groupePath);
    if (!groupeFile) {
        const groupeContent = `---
type: groupe
genre: []
pays-origine: ${paysFinal}
formation: 
site-web: 
tags:
  - groupe
---

# 🎤 ${groupe}

## 📊 Informations

- **Genre** : 
- **Pays** : [[${paysFinal}]]
- **Formation** : 
- **Site web** : 

## 🎸 Albums favoris

- 

## 🎪 Concerts vus

\`\`\`dataview
TABLE date as "Date", salle as "Salle", ville as "Ville"
FROM "Musique/Concerts"
WHERE contains(groupes, this.file.name)
SORT date DESC
\`\`\`

## 💭 Notes



## 🔗 Liens

- [Spotify]()
- [Bandcamp]()
- [Site officiel]()
`;
        await app.vault.create(groupePath, groupeContent);
    }
}

// 8.2. Créer la salle si nécessaire
if (salleFinal) {
    const sallePath = `Musique/Salles/${salleFinal}.md`;
    const salleFile = app.vault.getAbstractFileByPath(sallePath);
    if (!salleFile) {
        const salleContent = `---
type: salle
ville: ${villeFinal}
pays: ${paysFinal}
capacite: 
adresse: 
tags:
  - salle
---

# 🏛️ ${salleFinal}

## 📍 Localisation

- **Ville** : [[${villeFinal}]]
- **Pays** : [[${paysFinal}]]
- **Adresse** : 
- **Capacité** : 

## 🎫 Concerts vus ici

\`\`\`dataview
TABLE date as "Date", groupes as "Artistes"
FROM "Musique/Concerts"
WHERE contains(salle, this.file.name)
SORT date DESC
\`\`\`

## 💭 Notes



## 🔗 Liens

- [Site officiel]()
- [Google Maps]()
`;
        await app.vault.create(sallePath, salleContent);
    }
}

// 8.3. Créer le festival si nécessaire
if (festivalFinal) {
    const festivalPath = `Musique/Festivals/${festivalFinal}.md`;
    const festivalFile = app.vault.getAbstractFileByPath(festivalPath);
    if (!festivalFile) {
        const festivalContent = `---
type: festival
ville: ${villeFinal}
pays: ${paysFinal}
periode: 
editions-vues: []
tags:
  - festival
---

# 🎪 ${festivalFinal}

## 📊 Informations

- **Lieu** : [[${villeFinal}]] - [[${paysFinal}]]
- **Période habituelle** : 
- **Site web** : 

## 🗓️ Éditions visitées

\`\`\`dataview
TABLE date as "Date", groupes as "Groupes vus"
FROM "Musique/Concerts"
WHERE contains(festival, this.file.name)
SORT date DESC
\`\`\`

## 💭 Notes & Souvenirs



## 🔗 Liens

- [Site officiel]()
`;
        await app.vault.create(festivalPath, festivalContent);
    }
}

// 8.4. Créer le pays si nécessaire
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

// 8.5. Créer la ville si nécessaire
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

// 9. METTRE À JOUR CONCERTS.MD
const concertsPath = "Musique/Concerts.md";
const concertsFile = app.vault.getAbstractFileByPath(concertsPath);
if (concertsFile) {
    let concertsContent = await app.vault.read(concertsFile);
    
    // Créer le chemin relatif du fichier
    const fileRelPath = `Musique/Concerts/${année}/${nomFichier}`;
    
    // Formater les groupes pour l'affichage
    const groupesDisplay = groupesFinaux.map(g => `[[${g}]]`).join(", ");
    
    // Créer la nouvelle ligne
    const lieuDisplay = festivalFinal ? `[[${festivalFinal}]]` : (salleFinal ? `[[${salleFinal}]]` : villeFinal);
    const newLine = `- ${checkbox} **${dateInput}** : [[${fileRelPath}|${groupesFinaux.join(", ")}]] - *${lieuDisplay}*`;
    
    // Trouver la section de l'année
    const yearSection = `### ${année}`;
    const yearIndex = concertsContent.indexOf(yearSection);
    
    if (yearIndex !== -1) {
        // Trouver où insérer la ligne (après la section dataview)
        let insertPos = concertsContent.indexOf("```", yearIndex);
        insertPos = concertsContent.indexOf("```", insertPos + 3);
        insertPos = concertsContent.indexOf("\n", insertPos) + 1;
        
        // Chercher la bonne position en ordre décroissant
        const lines = concertsContent.substring(insertPos).split('\n');
        let insertOffset = 0;
        let inserted = false;
        
        for (let i = 0; i < lines.length; i++) {
            const match = lines[i].match(/^- \[.\] \*\*(\d{4}-\d{2}-\d{2})\*\*/);
            if (match) {
                const lineDate = match[1];
                if (dateInput > lineDate) {
                    insertOffset = lines.slice(0, i).join('\n').length;
                    inserted = true;
                    break;
                }
            } else if (lines[i].startsWith('###') || lines[i].startsWith('---')) {
                // On a atteint la fin de la section
                insertOffset = lines.slice(0, i).join('\n').length;
                inserted = true;
                break;
            }
        }
        
        if (!inserted) {
            // Ajouter à la fin de la section
            insertOffset = lines.slice(0, lines.findIndex(l => l.startsWith('###') || l.startsWith('---'))).join('\n').length;
        }
        
        const finalInsertPos = insertPos + insertOffset;
        concertsContent = concertsContent.slice(0, finalInsertPos) + newLine + '\n' + concertsContent.slice(finalInsertPos);
    } else {
        // L'année n'existe pas encore, ajouter une nouvelle section
        const archivesIndex = concertsContent.indexOf("## 🏛️ Archives des Concerts & Festivals");
        if (archivesIndex !== -1) {
            let insertPos = concertsContent.indexOf("\n", archivesIndex) + 1;
            insertPos = concertsContent.indexOf("\n", insertPos) + 1;
            
            const newSection = `### ${année}\n\n\`\`\`dataview\nTABLE groupes as "Artistes", salle as "Salle", ville as "Ville"\nFROM "Musique/Concerts/${année}"\nSORT date DESC\n\`\`\`\n\n${newLine}\n\n`;
            
            concertsContent = concertsContent.slice(0, insertPos) + newSection + concertsContent.slice(insertPos);
        }
    }
    
    await app.vault.modify(concertsFile, concertsContent);
}

// 10. DÉPLACER LE FICHIER AU BON ENDROIT
await tp.file.move(`${dossierAnnée}/${nomFichier}`);

-%>
---
type: concert
date: <% dateInput %>
groupes: [<% groupesFinaux.map(g => `"${g}"`).join(", ") %>]
salle: <% salleFinal %>
festival: <% festivalFinal %>
ville: <% villeFinal %>
pays: <% paysFinal %>
rating:
tags:
  - concert
---

# 🎸 Concert

## 📅 Informations

- **Date** : <% dateInput %>
- **Groupes** : <% groupesFinaux.map(g => `[[${g}]]`).join(", ") %>
- **Lieu** : <% festivalFinal ? `[[${festivalFinal}]]` : (salleFinal ? `[[${salleFinal}]] - [[${villeFinal}]]` : `[[${villeFinal}]]`) %>
- **Type** : <% festivalFinal ? "Festival" : "Concert" %>

## 🎵 Setlist

- 

## 💭 Notes & Impressions

<% notesInput %>

## 📷 Photos & Souvenirs



## 🔗 Liens

- [[Concerts|Retour à l'index des concerts]]
