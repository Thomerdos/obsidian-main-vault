#!/usr/bin/env python3
"""
Correction manuelle des derniers cas problématiques
"""

import re
from pathlib import Path

def main():
    vault_dir = Path("/home/runner/work/obsidian-main-vault/obsidian-main-vault")
    recettes_dir = vault_dir / "contenus" / "recettes" / "Fiches"
    ingredients_dir = vault_dir / "contenus" / "recettes" / "Ingredients"
    
    # Mappings à corriger
    fixes = [
        ('7-10 stalks garlic chives, cut into 2" pieces', 'ciboulette chinoise'),
        ("cuillères à soupe d'origan fraîchement ciselé", 'origan'),
        ("d'ail", 'ail'),
        ("d'ail pressées", 'ail'),
        ("d'huile", 'huile'),
        ("jus d'un demi-citron", 'jus de citron'),
        ('medium firm tofu, 1" cubed, or another meat of your choice, cut into small bite-sized', 'tofu ferme'),
    ]
    
    print("=== Correction manuelle des recettes ===\n")
    
    for old_name, new_name in fixes:
        print(f"Recherche: {old_name}")
        found_count = 0
        
        for recipe_file in recettes_dir.glob("*.md"):
            with open(recipe_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chercher toutes les variations possibles
            patterns = [
                f"'[[{old_name}]]'",
                f'[[{old_name}]]',
                f"- '[[{old_name}]]'",
            ]
            
            modified = False
            for pattern in patterns:
                if pattern in content:
                    content = content.replace(pattern, f"'[[{new_name}]]'")
                    modified = True
            
            if modified:
                with open(recipe_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ Corrigé dans: {recipe_file.name}")
                found_count += 1
        
        if found_count > 0:
            # Supprimer l'ancien fichier d'ingrédient
            old_file = ingredients_dir / f"{old_name}.md"
            if old_file.exists():
                old_file.unlink()
                print(f"  ✓ Supprimé: {old_name}.md")
            
            # S'assurer que le nouveau existe
            new_file = ingredients_dir / f"{new_name}.md"
            if not new_file.exists():
                with open(new_file, 'w', encoding='utf-8') as f:
                    f.write(f"""---
title: {new_name.capitalize()}
type: ingredient
---

# {new_name.capitalize()}

Ingrédient utilisé dans les recettes.
""")
                print(f"  ✓ Créé: {new_name}.md")
        print()
    
    # Vérification finale
    print("\n=== Vérification finale ===")
    all_ingredients = sorted([f.stem for f in ingredients_dir.glob("*.md")])
    print(f"Total: {len(all_ingredients)} ingrédients")
    
    # Chercher les suspects
    suspects = []
    for ing in all_ingredients:
        if any(c in ing for c in ['"', ',', '(', ')']):
            suspects.append(ing)
        elif any(word in ing.lower() for word in ['stalks', 'cubed', 'pieces', 'cut into']):
            suspects.append(ing)
    
    if suspects:
        print(f"\n⚠️  {len(suspects)} suspect(s):")
        for ing in suspects:
            print(f"  - {ing}")
    else:
        print("\n✓ Aucun suspect!")

if __name__ == "__main__":
    main()
