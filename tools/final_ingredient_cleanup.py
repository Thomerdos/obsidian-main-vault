#!/usr/bin/env python3
"""
Nettoyage final des ingrédients
"""

import os
import re
from pathlib import Path

# Liste des ingrédients à corriger manuellement
FINAL_FIXES = {
    "7-10 stalks garlic chives, cut into 2\" pieces": "ciboulette chinoise",
    "cuillères à soupe d'origan fraîchement ciselé": "origan",
    "d'ail": "ail",
    "d'ail pressées": "ail",
    "d'huile": "huile",
    "jus d'un demi-citron": "jus de citron",
    "medium firm tofu, 1\" cubed, or another meat of your choice, cut into small bite-sized": "tofu ferme",
}

def fix_ingredient_in_file(filepath, old_name, new_name):
    """Remplace un ingrédient dans un fichier"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
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
    
    print("=== Nettoyage final ===")
    
    # Corriger les fichiers de recettes
    for old_name, new_name in FINAL_FIXES.items():
        count = 0
        for recipe_file in recettes_dir.glob("*.md"):
            if fix_ingredient_in_file(recipe_file, old_name, new_name):
                count += 1
        
        if count > 0:
            print(f"✓ Corrigé: {old_name} → {new_name} ({count} recettes)")
            
            # Supprimer l'ancienne page
            old_file = ingredients_dir / f"{old_name}.md"
            if old_file.exists():
                old_file.unlink()
                print(f"  Supprimé: {old_name}.md")
            
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
                print(f"  Créé: {new_name}.md")
    
    print("\n=== Liste finale des ingrédients ===")
    all_ingredients = sorted([f.stem for f in ingredients_dir.glob("*.md")])
    print(f"Total: {len(all_ingredients)} ingrédients\n")
    
    # Afficher les ingrédients suspects (non français, avec ponctuation étrange)
    suspects = []
    for ing in all_ingredients:
        # Vérifier si contient des caractères suspects
        if any(c in ing for c in ['"', ':', ',', '(', ')']):
            suspects.append(ing)
        # Vérifier si c'est de l'anglais non traduit
        elif any(word in ing.lower() for word in ['stalks', 'cubed', 'cuillère', 'cuillères']):
            suspects.append(ing)
    
    if suspects:
        print("⚠️  Ingrédients suspects restants:")
        for ing in suspects:
            print(f"  - {ing}")
    
    # Lister tous les ingrédients
    print("\n=== Tous les ingrédients ===")
    for ing in all_ingredients:
        print(f"  - {ing}")

if __name__ == "__main__":
    main()
