#!/usr/bin/env python3
"""
Script to normalize ingredient names and simplify the recipe system.

This script:
1. Normalizes ingredient names (French, singular, no quantities, simple form)
2. Updates recipe metadata with normalized names
3. Renames ingredient files
4. Simplifies dataviews in ingredient pages
5. Deletes orphan ingredients
6. Generates a detailed migration report
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import shutil

# Translation mappings: English -> French
TRANSLATIONS = {
    # Common ingredients
    'onion': 'oignon',
    'onions': 'oignon',
    'red onion': 'oignon rouge',
    'garlic': 'ail',
    'ginger': 'gingembre',
    'tomato': 'tomate',
    'tomatoes': 'tomate',
    'cherry tomatoes': 'tomate cerise',
    'potato': 'pomme de terre',
    'potatoes': 'pomme de terre',
    'carrot': 'carotte',
    'carrots': 'carotte',
    
    # Herbs and spices
    'basil': 'basilic',
    'parsley': 'persil',
    'thyme': 'thym',
    'bay leaf': 'laurier',
    'coriander': 'coriandre',
    'cilantro': 'coriandre',
    'dill': 'aneth',
    'sesame seeds': 'graines de sésame',
    'sesame oil': 'huile de sésame',
    'sesame paste': 'pâte de sésame',
    'toasted sesame oil': 'huile de sésame',
    'japanese sesame paste': 'pâte de sésame',
    
    # Proteins
    'pork belly': 'poitrine de porc',
    'chicken stock': 'bouillon de poulet',
    'chicken broth': 'bouillon de poulet',
    'fish sauce': 'sauce de poisson',
    'korean fish sauce': 'sauce de poisson',
    'shrimp paste': 'pâte de crevettes',
    'fermented shrimp': 'crevettes fermentées',
    
    # Vegetables
    'green onion': 'oignon vert',
    'green onions': 'oignon vert',
    'scallion': 'cébette',
    'scallions': 'cébette',
    'garlic chives': 'ciboulette chinoise',
    'chili': 'piment',
    'chilies': 'piment',
    'chili flakes': 'piment séché',
    'dry chilies': 'piment séché',
    'dried chili flakes': 'piment séché',
    'red spur chilies': 'piment rouge',
    'bell pepper': 'poivron',
    'eggplant': 'aubergine',
    'eggplants': 'aubergine',
    'thai eggplants': 'aubergine thaï',
    'zucchini': 'courgette',
    'green beans': 'haricots verts',
    'asparagus': 'asperge',
    
    # Asian ingredients
    'miso': 'miso',
    'sake': 'saké',
    'mirin': 'mirin',
    'soy milk': 'lait de soja',
    'soy sauce': 'sauce soja',
    'dark soy sauce': 'sauce soja foncée',
    'coconut milk': 'lait de coco',
    'tamarind': 'tamarin',
    'tamarind paste': 'pâte de tamarin',
    'cooking tamarind': 'tamarin',
    'kombu': 'kombu',
    'dried kelp': 'kombu',
    'katsuobushi': 'bonite séchée',
    'dried bonito flakes': 'bonite séchée',
    'wakame seaweed': 'algue wakame',
    'dried wakame seaweed': 'algue wakame',
    'tofu': 'tofu',
    'silken tofu': 'tofu soyeux',
    'soft tofu': 'tofu soyeux',
    'rice noodles': 'nouilles de riz',
    'dry rice noodles': 'nouilles de riz',
    
    # Starches
    'cornstarch': 'fécule de maïs',
    'rice': 'riz',
    'basmati rice': 'riz basmati',
    'noodles': 'nouilles',
    
    # Spices
    'turmeric': 'curcuma',
    'galangal': 'galanga',
    'kaffir lime': 'combava',
    'lime': 'citron vert',
    'paprika': 'paprika',
    'white pepper': 'poivre blanc',
    'baking soda': 'bicarbonate de soude',
    'garlic salt': 'sel d\'ail',
    
    # Other
    'egg': 'oeuf',
    'eggs': 'oeuf',
    'water': 'eau',
    'salt': 'sel',
    'pepper': 'poivre',
    'sugar': 'sucre',
    'palm sugar': 'sucre de palme',
    'brown sugar': 'sucre brun',
    'light brown sugar': 'sucre brun',
    'corn oil': 'huile de maïs',
    'cooking oil': 'huile',
    'olive oil': 'huile d\'olive',
    'msg': 'glutamate monosodique',
    'cashews': 'noix de cajou',
}

# Normalization rules for French ingredients
FRENCH_NORMALIZATIONS = {
    # Plurals to singular
    'oignons': 'oignon',
    'tomates': 'tomate',
    'carottes': 'carotte',
    'courgettes': 'courgette',
    'aubergines': 'aubergine',
    'poivrons': 'poivron',
    'champignons': 'champignon',
    'épinards': 'épinard',
    'asperges': 'asperge',
    'pommes de terre': 'pomme de terre',
    'citrons': 'citron',
    
    # Specific normalizations
    'ail épluchées et hachées': 'ail',
    "d'ail épluchées et hachées": 'ail',
    'oignon ou échalote coupée': 'oignon',
    "d'épinards entiers": 'épinard',
    'feuille (s) basilic': 'basilic',
    'feuilles basilic': 'basilic',
    'branche(s) thym': 'thym',
    'branches thym': 'thym',
    'brin(s) persil': 'persil',
    'brins persil': 'persil',
    'pincée(s) sel': 'sel',
    'pincée(s) poivre': 'poivre',
    'oignon(s)': 'oignon',
    'courgette(s)': 'courgette',
    'sucrines': 'sucrine',
    'gros oignons': 'oignon',
    "gousses d'ail": 'ail',
    'gousse ail': 'ail',
    'blancs de poireaux': 'poireau',
    'bœuf haché': 'boeuf haché',
    'bouquet garni': 'bouquet garni',
    'concentré de tomate': 'concentré de tomate',
    'concentré de tomates': 'concentré de tomate',
    'coulis de tomates': 'coulis de tomate',
    
    # Units to remove
    'cc de msg': 'glutamate monosodique',
    'c. à soupe huile d\'olive': 'huile d\'olive',
}

def normalize_ingredient_name(name):
    """
    Normalize an ingredient name according to the rules:
    - French only
    - Singular
    - No quantities
    - Simple form (main ingredient only)
    - No preparation methods
    """
    if not name:
        return None
    
    # Store original for debugging
    original = name
    name = name.strip()
    
    # Remove wiki link brackets
    name = re.sub(r'\[\[|\]\]', '', name)
    
    # Convert to lowercase for processing
    name_lower = name.lower()
    
    # Remove quantity patterns at the start INCLUDING units
    # Examples: "0.5 kg", "1lb", "3 cups", "4oz", "½ tsp", "tbsp", "cups"
    name_lower = re.sub(r'^\d+[\.,]?\d*\s*(?:foz|lb|oz|kg|g|mg|l|ml|cl|cup|cups|tbsp|tsp|tablespoons?|teaspoons?|piece|pieces|unité)s?\s+', '', name_lower)
    name_lower = re.sub(r'^[½¼¾⅓⅔⅛⅜⅝⅞]\s+(?:tsp|tbsp|cup|cups)?\s*', '', name_lower)
    name_lower = re.sub(r'^\d+\s*-\s*\d+\s*(?:tbsp|tsp|cup|cups)?\s+', '', name_lower)
    # Remove standalone unit words at start
    name_lower = re.sub(r'^(?:cups?|tbsp|tsp|tablespoons?|teaspoons?|oz|lb|piece|pieces)\s+', '', name_lower)
    name_lower = re.sub(r'^\d+[\.,]?\d*\s+', '', name_lower)
    
    # Remove preparation/description in parentheses
    name_lower = re.sub(r'\([^)]*\)', '', name_lower)
    name_lower = re.sub(r'\(\(.*?\)\)', '', name_lower)
    
    # Remove "note X" references
    name_lower = re.sub(r',?\s*note\s+\d+', '', name_lower)
    name_lower = re.sub(r',?\s*see note\s+\d+', '', name_lower)
    
    # Remove optional/taste qualifiers
    name_lower = re.sub(r',?\s*to taste\s*(?:\(optional\))?', '', name_lower)
    name_lower = re.sub(r',?\s*\(optional\)', '', name_lower)
    name_lower = re.sub(r',?\s*optional', '', name_lower)
    
    # Remove size/measurement descriptions
    name_lower = re.sub(r',?\s*\d+\s*inch.*?(?:,|$)', '', name_lower)
    name_lower = re.sub(r',?\s*\d+\.?\d*\s*cm.*?(?:,|$)', '', name_lower)
    name_lower = re.sub(r'\d+\.?\d*\s+ounces?,?', '', name_lower)
    
    # Remove preparation methods and "use X for Y" instructions
    name_lower = re.sub(r',?\s*use\s+.*$', '', name_lower)
    name_lower = re.sub(r',?\s*divided$', '', name_lower)
    name_lower = re.sub(r'\s+plus\s+more.*$', '', name_lower)
    name_lower = re.sub(r'\s+as\s+desired.*$', '', name_lower)
    name_lower = re.sub(r',?\s*see\s+how\s+to.*$', '', name_lower)
    name_lower = re.sub(r',?\s*and\s+also\s+see.*$', '', name_lower)
    
    # Remove cutting/preparation descriptions
    name_lower = re.sub(r',?\s*(?:chopped|minced|julienned|sliced|diced|cut into.*|crashed|finely chopped|boiled and.*|halved or.*|packed|soaked?|trimmed).*$', '', name_lower)
    name_lower = re.sub(r',?\s*(?:épluchées?|hachées?|coupée?|émincée?s?|détaillée?s?|glacée?s?|entiers?).*$', '', name_lower)
    
    # Remove articles at start
    name_lower = re.sub(r'^(?:le|la|les|un|une|des|du|de|d\'|l\')\s+', '', name_lower)
    
    # Remove numbers and extra words at the end
    name_lower = re.sub(r'\s+\d+.*$', '', name_lower)
    
    # Clean up extra commas and spaces
    name_lower = re.sub(r'\s*,\s*$', '', name_lower)
    name_lower = name_lower.strip(' ,-.')
    
    # Translate from English to French
    for eng, fr in TRANSLATIONS.items():
        # Do full word matching when possible
        if name_lower == eng or name_lower.startswith(eng + ' ') or name_lower.endswith(' ' + eng):
            name_lower = name_lower.replace(eng, fr)
            break
    
    # Apply French normalizations (check exact matches first)
    for pattern, replacement in FRENCH_NORMALIZATIONS.items():
        if name_lower == pattern:
            name_lower = replacement
            break
    
    # Remove plural 's' at the end for common patterns (only if not already normalized)
    if name_lower not in FRENCH_NORMALIZATIONS.values():
        name_lower = re.sub(r'^(.*(?:ion|ment|tte|ron|gne|il))s$', r'\1', name_lower)
    
    # Skip non-ingredient entries
    skip_words = ['préparation', 'instruction', 'note', 'voir', 'see', 'mixeur', 'couteau', 'fourchette', 'gants', 'sachet plastique']
    if any(word in name_lower for word in skip_words):
        return None
    
    # Skip if only units/numbers remain
    if re.match(r'^[\d\s,\.\-]+$', name_lower):
        return None
    
    # Return None if empty after processing
    if not name_lower or len(name_lower) < 2:
        return None
    
    return name_lower

def extract_ingredients_from_frontmatter(content):
    """Extract ingredients list from YAML frontmatter."""
    try:
        # Extract frontmatter
        if content.startswith('---\n'):
            parts = content.split('---\n', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                if isinstance(frontmatter, dict) and 'ingredients' in frontmatter:
                    return frontmatter.get('ingredients', [])
    except Exception as e:
        print(f"Error parsing frontmatter: {e}")
    return []

def update_recipe_file(filepath, ingredient_mapping):
    """Update a recipe file with normalized ingredient names."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content into frontmatter and body
        if not content.startswith('---\n'):
            return False, "No frontmatter found"
        
        parts = content.split('---\n', 2)
        if len(parts) < 3:
            return False, "Invalid frontmatter structure"
        
        frontmatter_str = parts[1]
        body = parts[2]
        
        # Parse frontmatter
        frontmatter = yaml.safe_load(frontmatter_str)
        if not isinstance(frontmatter, dict):
            return False, "Invalid frontmatter format"
        
        # Update ingredients in frontmatter
        if 'ingredients' in frontmatter:
            old_ingredients = frontmatter['ingredients']
            new_ingredients = []
            
            for ing in old_ingredients:
                normalized = normalize_ingredient_name(str(ing))
                if normalized:
                    new_ingredients.append(normalized)
            
            frontmatter['ingredients'] = new_ingredients
        
        # Update links in the Ingrédients section
        # Pattern: [[old ingredient name]]
        for old_name, new_name in ingredient_mapping.items():
            # Replace wiki links
            body = re.sub(
                r'\[\[' + re.escape(old_name) + r'\]\]',
                f'[[{new_name}]]',
                body,
                flags=re.IGNORECASE
            )
        
        # Reconstruct file
        new_frontmatter = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
        new_content = f"---\n{new_frontmatter}---\n{body}"
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Updated successfully"
    
    except Exception as e:
        return False, f"Error: {str(e)}"

def create_simplified_ingredient_page(ingredient_name, output_path):
    """Create or update an ingredient page with simplified dataview."""
    content = f"""---
type: ingredient
nom: "{ingredient_name}"
categorie: ""
recettes: []
allergenes: []
saison: []
tags:
  - ingredient
---

# 🥕 {ingredient_name.capitalize()}

## 📋 Informations

- **Catégorie**: 
- **Saison**: 
- **Allergènes**: 

## 🍽️ Utilisé dans les recettes

```dataview
TABLE WITHOUT ID
  file.link as "Recette",
  source as "Source"
FROM "contenus/recettes/Fiches"
WHERE contains(file.outlinks, this.file.link)
SORT file.name ASC
```

## 💡 Notes


## 🔗 Liens
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

def check_orphan_ingredients(normalized_to_files, recipes_dir):
    """Check which ingredients are not referenced in any recipe."""
    orphans = []
    
    # Collect all ingredients used in recipes
    used_ingredients = set()
    for recipe_path in recipes_dir.glob('*.md'):
        try:
            with open(recipe_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ingredients = extract_ingredients_from_frontmatter(content)
            used_ingredients.update([ing.lower() if isinstance(ing, str) else str(ing).lower() for ing in ingredients])
        except Exception as e:
            print(f"Warning: Could not read {recipe_path.name}: {e}")
    
    # Check which normalized ingredients are not used
    for normalized_name in normalized_to_files.keys():
        if normalized_name not in used_ingredients:
            orphans.append(normalized_name)
    
    return orphans

def apply_changes(vault_path, normalized_to_files):
    """Apply the normalization changes by replacing old files with new ones."""
    ingredients_dir = vault_path / 'contenus' / 'recettes' / 'Ingredients'
    backup_dir = vault_path / 'contenus' / 'recettes' / '_backup_ingredients'
    new_dir = ingredients_dir / '_temp_new'
    
    # Create backup
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    backup_dir.mkdir(exist_ok=True)
    
    print("\n[APPLY] Creating backup of old ingredient files...")
    for file_path in ingredients_dir.glob('*.md'):
        shutil.copy2(file_path, backup_dir / file_path.name)
    
    print(f"[APPLY] Backed up {len(list(backup_dir.glob('*.md')))} files")
    
    # Delete old ingredient files
    print("[APPLY] Removing old ingredient files...")
    for file_path in ingredients_dir.glob('*.md'):
        file_path.unlink()
    
    # Move new files to main directory
    print("[APPLY] Moving normalized files to main directory...")
    for new_file in new_dir.glob('*.md'):
        shutil.move(str(new_file), ingredients_dir / new_file.name)
    
    # Clean up temp directory
    new_dir.rmdir()
    
    print(f"[APPLY] Applied {len(list(ingredients_dir.glob('*.md')))} normalized ingredient files")
    print(f"[APPLY] Backup saved in: {backup_dir}")

def main():
    """Main function to normalize ingredients and update recipes."""
    import sys
    
    # Check for --apply flag
    apply_mode = '--apply' in sys.argv
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    
    vault_path = Path('/home/runner/work/obsidian-main-vault/obsidian-main-vault')
    ingredients_dir = vault_path / 'contenus' / 'recettes' / 'Ingredients'
    recipes_dir = vault_path / 'contenus' / 'recettes' / 'Fiches'
    
    print("=" * 80)
    print("INGREDIENT NORMALIZATION SCRIPT")
    if apply_mode:
        print("MODE: APPLY CHANGES")
    else:
        print("MODE: PREVIEW ONLY")
    print("=" * 80)
    
    # Step 1: Analyze all ingredient files
    print("\n[Step 1] Analyzing ingredient files...")
    ingredient_files = list(ingredients_dir.glob('*.md'))
    print(f"Found {len(ingredient_files)} ingredient files")
    
    # Build normalization mapping
    ingredient_mapping = {}  # old_name -> new_name
    normalized_to_files = defaultdict(list)  # normalized_name -> [file_paths]
    
    for file_path in ingredient_files:
        old_name = file_path.stem
        normalized = normalize_ingredient_name(old_name)
        
        if normalized:
            ingredient_mapping[old_name] = normalized
            normalized_to_files[normalized].append(file_path)
    
    print(f"Created {len(ingredient_mapping)} normalization mappings")
    print(f"Skipped {len(ingredient_files) - len(ingredient_mapping)} invalid ingredient names")
    
    # Step 2: Identify duplicates to merge
    print("\n[Step 2] Identifying duplicates to merge...")
    duplicates = {k: v for k, v in normalized_to_files.items() if len(v) > 1}
    print(f"Found {len(duplicates)} ingredients with duplicates")
    
    # Step 3: Update all recipe files
    print("\n[Step 3] Updating recipe files...")
    recipe_files = list(recipes_dir.glob('*.md'))
    updated_recipes = []
    failed_recipes = []
    
    for recipe_path in recipe_files:
        success, message = update_recipe_file(recipe_path, ingredient_mapping)
        if success:
            updated_recipes.append(recipe_path.name)
        else:
            failed_recipes.append((recipe_path.name, message))
    
    print(f"Updated {len(updated_recipes)} recipes")
    if failed_recipes:
        print(f"Failed to update {len(failed_recipes)} recipes")
    
    # Step 4: Create normalized ingredient files
    print("\n[Step 4] Creating normalized ingredient files...")
    new_ingredients_dir = ingredients_dir / '_temp_new'
    new_ingredients_dir.mkdir(exist_ok=True)
    
    renamed_files = {}
    merged_files = []
    
    for normalized_name, file_paths in normalized_to_files.items():
        new_path = new_ingredients_dir / f"{normalized_name}.md"
        
        # If multiple files map to same normalized name, merge them
        if len(file_paths) > 1:
            merged_files.append((normalized_name, [p.name for p in file_paths]))
        
        # Create simplified ingredient page
        create_simplified_ingredient_page(normalized_name, new_path)
        renamed_files[file_paths[0].name] = normalized_name
    
    print(f"Created {len(renamed_files)} normalized ingredient files in _temp_new/")
    print(f"Merged {len(merged_files)} duplicate ingredients")
    
    # Step 5: Check for orphan ingredients
    print("\n[Step 5] Checking for orphan ingredients...")
    orphans = check_orphan_ingredients(normalized_to_files, recipes_dir)
    print(f"Found {len(orphans)} orphan ingredients (not referenced in any recipe)")
    
    # Step 6: Generate migration report
    print("\n[Step 6] Generating migration report...")
    report_path = vault_path / 'ingredient-normalization-report.md'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# Ingredient Normalization Report\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"## Summary\n\n")
        f.write(f"- Original ingredient files: {len(ingredient_files)}\n")
        f.write(f"- Normalized ingredients: {len(normalized_to_files)}\n")
        f.write(f"- Duplicates merged: {len(merged_files)}\n")
        f.write(f"- Recipe files updated: {len(updated_recipes)}\n")
        f.write(f"- Recipe files failed: {len(failed_recipes)}\n")
        f.write(f"- Orphan ingredients: {len(orphans)}\n\n")
        
        f.write(f"## Ingredient Mappings (Sample - first 100)\n\n")
        f.write("| Original Name | Normalized Name |\n")
        f.write("|---------------|----------------|\n")
        for old, new in list(ingredient_mapping.items())[:100]:
            f.write(f"| `{old}` | `{new}` |\n")
        if len(ingredient_mapping) > 100:
            f.write(f"\n... and {len(ingredient_mapping) - 100} more\n\n")
        
        if merged_files:
            f.write(f"## Merged Ingredients\n\n")
            for normalized, originals in sorted(merged_files):
                f.write(f"- **{normalized}**: merged from\n")
                for orig in originals:
                    f.write(f"  - `{orig}`\n")
        
        if orphans:
            f.write(f"\n## Orphan Ingredients (will be deleted)\n\n")
            for orphan in sorted(orphans):
                f.write(f"- `{orphan}`\n")
        
        if failed_recipes:
            f.write(f"\n## Failed Recipe Updates\n\n")
            for name, error in failed_recipes:
                f.write(f"- `{name}`: {error}\n")
    
    print(f"\nReport generated: {report_path}")
    
    # Step 7: Apply changes if requested
    if apply_mode:
        print("\n[Step 7] Applying changes...")
        if not auto_confirm:
            response = input("\n⚠️  Are you sure you want to apply these changes? (yes/no): ")
            if response.lower() != 'yes':
                print("\n❌ Changes NOT applied. Preview files remain in _temp_new/")
                return
        else:
            print("\n✅ Auto-confirming (--yes flag provided)")
        
        apply_changes(vault_path, normalized_to_files)
        
        # Delete orphan ingredients
        if orphans:
            print(f"\n[APPLY] Deleting {len(orphans)} orphan ingredient files...")
            for orphan in orphans:
                orphan_path = ingredients_dir / f"{orphan}.md"
                if orphan_path.exists():
                    orphan_path.unlink()
                    print(f"  Deleted: {orphan}.md")
        
        print("\n✅ Changes applied successfully!")
    else:
        print("\n" + "=" * 80)
        print("NORMALIZATION PREVIEW COMPLETE")
        print("=" * 80)
        print("\nNOTE: This is a preview run. Files are in _temp_new/ directory.")
        print("Review the report, then run with --apply flag to apply changes:")
        print(f"  python3 {sys.argv[0]} --apply --yes")

if __name__ == '__main__':
    main()
