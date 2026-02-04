<%*
/**
 * Post-Webclipper Recipe Processing Template
 * 
 * This template processes a recipe after it has been clipped with Webclipper.
 * It extracts ingredients from the text, normalizes them, updates frontmatter,
 * and creates ingredient pages.
 * 
 * Usage:
 * 1. Clip a recipe using the webclipper-recette.md template
 * 2. Run this template on the clipped recipe note
 * 3. The template will parse ingredients and update the note
 */

// Helper functions
function parseIngredientLine(line) {
    line = line.trim();
    
    // Remove checkbox markers and list markers
    line = line.replace(/^-\s*\[[ x]\]\s*/, '');
    line = line.replace(/^[-*]\s+/, '');
    
    if (!line) return null;
    
    // Pattern to extract ingredient name (after quantity and unit)
    const patterns = [
        /^[\d,\.]+\s*(?:kg|g|mg|l|ml|cl|dl|unité|gousse|filet|pincée|cuillère|cas|cac|tasse)s?\s+(.+)$/i,
        /^quelques?\s+(?:pincée|gousse|unité)s?\s+(.+)$/i,
        /^\d+\s+(.+)$/,  // Just number and name
        /^(.+)$/,  // Fallback: whole line
    ];
    
    for (const pattern of patterns) {
        const match = line.match(pattern);
        if (match) {
            let ingredient = match[1].trim();
            // Clean up
            ingredient = ingredient.replace(/\s+/g, ' ');
            return ingredient.toLowerCase();
        }
    }
    
    return null;
}

function normalizeIngredient(name) {
    if (!name) return "";
    
    name = name.trim().toLowerCase();
    
    // Remove leading articles
    name = name.replace(/^(le|la|les|l'|un|une|des|du|de|d')\s+/, '');
    
    // Common plurals to singular (French)
    const replacements = {
        'oignons': 'oignon',
        'tomates': 'tomate',
        'carottes': 'carotte',
        'pommes de terre': 'pomme de terre',
        "gousses d'ail": 'ail',
        'ail': 'ail',
        'piments': 'piment',
        'poivrons': 'poivron',
        'aubergines': 'aubergine',
        'courgettes': 'courgette',
        'champignons': 'champignon',
    };
    
    if (replacements[name]) {
        return replacements[name];
    }
    
    return name;
}

async function createIngredientPage(ingredient) {
    const ingredientsFolder = app.vault.getAbstractFileByPath("contenus/recettes/Ingredients");
    if (!ingredientsFolder) {
        await app.vault.createFolder("contenus/recettes/Ingredients");
    }
    
    const ingredientName = ingredient.charAt(0).toUpperCase() + ingredient.slice(1);
    const ingredientPath = `contenus/recettes/Ingredients/${ingredientName}.md`;
    
    const existingFile = app.vault.getAbstractFileByPath(ingredientPath);
    if (existingFile) {
        return false; // Already exists
    }
    
    const template = `---
type: ingredient
nom: "${ingredient}"
categorie: ""
recettes: []
allergenes: []
saison: []
tags:
  - ingredient
---

# 🥕 ${ingredientName}

## 📋 Informations

- **Catégorie**: 
- **Saison**: 
- **Allergènes**: 

## 🍽️ Utilisé dans les recettes

\`\`\`dataview
TABLE WITHOUT ID
  file.link as "Recette",
  temps_preparation as "Préparation (min)",
  temps_cuisson as "Cuisson (min)",
  type_cuisine as "Cuisine"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, "${ingredient}")
SORT file.name ASC
\`\`\`

## 💡 Notes


## 🔗 Liens
`;
    
    await app.vault.create(ingredientPath, template);
    return true; // Newly created
}

// Main processing
const file = tp.file.find_tfile(tp.file.title);
const content = await app.vault.read(file);

// Extract ingredients from the Ingrédients section
const ingredientsMatch = content.match(/## Ingrédients\s*\n(.*?)(?=\n##|\n---|\Z)/s);
let ingredients = [];

if (ingredientsMatch) {
    const ingredientsText = ingredientsMatch[1];
    const lines = ingredientsText.split('\n');
    
    for (const line of lines) {
        if (line.trim()) {
            const ingredient = parseIngredientLine(line);
            if (ingredient) {
                const normalized = normalizeIngredient(ingredient);
                if (normalized && !ingredients.includes(normalized)) {
                    ingredients.push(normalized);
                }
            }
        }
    }
}

// Update frontmatter with ingredients
if (ingredients.length > 0) {
    await tp.file.update_frontmatter((fm) => {
        fm.ingredients = ingredients;
    });
    
    tR += `✅ Extracted ${ingredients.length} ingredients:\n`;
    tR += ingredients.map(ing => `- ${ing}`).join('\n');
    tR += '\n\n';
    
    // Create ingredient pages
    let created = 0;
    for (const ingredient of ingredients) {
        const wasCreated = await createIngredientPage(ingredient);
        if (wasCreated) {
            created++;
        }
    }
    
    if (created > 0) {
        tR += `\n✅ Created ${created} new ingredient page(s)\n`;
    }
    
    // Update the ingredients section with wiki links
    let newContent = content;
    if (ingredientsMatch) {
        const oldSection = ingredientsMatch[0];
        const lines = ingredientsMatch[1].split('\n');
        const newLines = lines.map(line => {
            if (!line.trim()) return line;
            
            const ingredient = parseIngredientLine(line);
            if (ingredient) {
                const normalized = normalizeIngredient(ingredient);
                if (normalized && ingredients.includes(normalized)) {
                    // Add wiki link
                    const lineClean = line.replace(/^-\s*\[[ x]\]\s*/, '- ');
                    // Find and wrap the ingredient name
                    const pattern = new RegExp(normalized, 'i');
                    return lineClean.replace(pattern, `[[${normalized}]]`);
                }
            }
            return line;
        });
        
        const newSection = `## Ingrédients\n\n${newLines.join('\n')}`;
        newContent = newContent.replace(oldSection, newSection);
        
        await app.vault.modify(file, newContent);
        tR += '\n✅ Updated ingredient links in the recipe\n';
    }
    
} else {
    tR += '⚠️  No ingredients found in the recipe. Please add them manually.\n';
}

tR += '\n---\n';
tR += '**Note**: Remember to fill in the frontmatter properties (type_cuisine, origine, regime, saison, temps_preparation, temps_cuisson)\n';
%>
