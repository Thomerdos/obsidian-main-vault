#!/usr/bin/env python3
"""
Correction manuelle des ingrédients encore mal normalisés
"""

import os
import re
from pathlib import Path

# Corrections supplémentaires
ADDITIONAL_FIXES = {
    "7-10 stalks garlic chives, cut into 2\" pieces": "ciboulette chinoise",
    "cuillère à café de vinaigre de vin blanc ou rouge selon la coloration que vous": "vinaigre de vin",
    "cuillères à soupe d'origan fraîchement ciselé": "origan",
    "d'ail": "ail",
    "d'ail pressées": "ail",
    "d'huile": "huile",
    "jus d'un demi-citron": "jus de citron",
    "medium firm tofu, 1\" cubed, or another meat of your choice, cut into small bite-sized": "tofu ferme",
    "petit piment rouge : retirer les graines et la membrane intérieure blanche puis": "piment rouge",
    "œufs": "oeuf",
    "huile d'olive": "huile d'olive",  # Dédupliquer
    "piments végétariens": "piment végétarien",
}

def fix_ingredient_in_file(filepath, old_name, new_name):
    """Remplace un ingrédient dans un fichier"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer dans le frontmatter
    old_wikilink = f"'[[{old_name}]]'"
    new_wikilink = f"'[[{new_name}]]'"
    
    if old_wikilink in content:
        content = content.replace(old_wikilink, new_wikilink)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    vault_dir = Path("/home/runner/work/obsidian-main-vault/obsidian-main-vault")
    recettes_dir = vault_dir / "contenus" / "recettes" / "Fiches"
    ingredients_dir = vault_dir / "contenus" / "recettes" / "Ingredients"
    
    print("=== Correction des ingrédients restants ===")
    
    # Corriger les fichiers de recettes
    for old_name, new_name in ADDITIONAL_FIXES.items():
        if old_name == new_name:
            continue
            
        count = 0
        for recipe_file in recettes_dir.glob("*.md"):
            if fix_ingredient_in_file(recipe_file, old_name, new_name):
                count += 1
        
        if count > 0:
            print(f"✓ {old_name} → {new_name} ({count} recettes)")
            
            # Supprimer l'ancienne page d'ingrédient
            old_file = ingredients_dir / f"{old_name}.md"
            if old_file.exists():
                old_file.unlink()
            
            # S'assurer que la nouvelle existe
            new_file = ingredients_dir / f"{new_name}.md"
            if not new_file.exists():
                content = f"""---
title: {new_name.capitalize()}
type: ingredient
---

# {new_name.capitalize()}

Ingrédient utilisé dans les recettes.
"""
                with open(new_file, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    # Supprimer les doublons d'huile d'olive
    duplicate = ingredients_dir / "huile d'olive.md"
    if duplicate.exists():
        print(f"Suppression du doublon: huile d'olive")
        duplicate.unlink()
    
    print("\n=== Statistiques finales ===")
    remaining = len(list(ingredients_dir.glob("*.md")))
    print(f"Pages d'ingrédients totales: {remaining}")

if __name__ == "__main__":
    main()
