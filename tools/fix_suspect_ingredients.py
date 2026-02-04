#!/usr/bin/env python3
"""
Correction des ingrédients suspects restants
"""

import os
from pathlib import Path

SUSPECT_FIXES = {
    "7-10 stalks garlic chives, cut into 2\" pieces": "ciboulette chinoise",
    "cuillères à soupe d'origan fraîchement ciselé": "origan",
    "d'ail": "ail",
    "d'ail pressées": "ail",
    "d'huile": "huile",
    "jus d'un demi-citron": "jus de citron",
    "medium firm tofu, 1\" cubed, or another meat of your choice, cut into small bite-sized": "tofu ferme",
}

def replace_in_file(filepath, old_name, new_name):
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
    
    print("=== Correction des ingrédients suspects ===\n")
    
    for old_name, new_name in SUSPECT_FIXES.items():
        print(f"Traitement: {old_name} → {new_name}")
        count = 0
        
        # Mettre à jour les recettes
        for recipe_file in recettes_dir.glob("*.md"):
            if replace_in_file(recipe_file, old_name, new_name):
                count += 1
        
        if count > 0:
            print(f"  ✓ Mis à jour dans {count} recette(s)")
        
        # Supprimer l'ancienne page
        old_file = ingredients_dir / f"{old_name}.md"
        if old_file.exists():
            old_file.unlink()
            print(f"  ✓ Supprimé: {old_name}.md")
        
        # Créer/mettre à jour la nouvelle page
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
    
    # Chercher les ingrédients encore suspects
    suspects = [ing for ing in all_ingredients if any(c in ing for c in ['"', ',', '(', ')']) or 
                any(word in ing.lower() for word in ['stalks', 'cubed', 'pieces', 'cuillère', 'cuillères'])]
    
    if suspects:
        print(f"⚠️  {len(suspects)} ingrédient(s) suspect(s) restant(s):")
        for ing in suspects:
            print(f"  - {ing}")
    else:
        print("✓ Aucun ingrédient suspect trouvé!")
    
    print(f"\n✓ Total final: {len(all_ingredients)} ingrédients normalisés")

if __name__ == "__main__":
    main()
