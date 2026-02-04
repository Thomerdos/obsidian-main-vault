#!/usr/bin/env python3
"""
Rapport final de la normalisation des ingrédients
"""

import re
from pathlib import Path
from collections import defaultdict

def main():
    vault_dir = Path("/home/runner/work/obsidian-main-vault/obsidian-main-vault")
    recettes_dir = vault_dir / "contenus" / "recettes" / "Fiches"
    ingredients_dir = vault_dir / "contenus" / "recettes" / "Ingredients"
    
    # Compter les ingrédients
    all_ingredients = sorted([f.stem for f in ingredients_dir.glob("*.md")])
    
    # Statistiques des recettes
    recipes_with_ingredients = 0
    recipes_without_ingredients = 0
    ingredient_usage = defaultdict(int)
    
    for recipe_file in recettes_dir.glob("*.md"):
        with open(recipe_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraire le frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            continue
        
        frontmatter = match.group(1)
        
        # Chercher ingredients:
        if 'ingredients:' in frontmatter:
            recipes_with_ingredients += 1
            
            # Compter les ingrédients utilisés
            for line in frontmatter.split('\n'):
                if line.startswith("- '[[") and line.endswith("]]'"):
                    ing = line[5:-3]
                    ingredient_usage[ing] += 1
        else:
            recipes_without_ingredients += 1
    
    # Afficher le rapport
    print("=" * 70)
    print("RAPPORT FINAL DE NORMALISATION DES INGRÉDIENTS")
    print("=" * 70)
    
    print(f"\n📊 STATISTIQUES GÉNÉRALES")
    print(f"  • Total d'ingrédients normalisés: {len(all_ingredients)}")
    print(f"  • Recettes avec ingrédients: {recipes_with_ingredients}")
    print(f"  • Recettes sans ingrédients: {recipes_without_ingredients}")
    print(f"  • Total de recettes: {recipes_with_ingredients + recipes_without_ingredients}")
    
    print(f"\n📋 INGRÉDIENTS LES PLUS UTILISÉS (Top 20)")
    sorted_usage = sorted(ingredient_usage.items(), key=lambda x: x[1], reverse=True)
    for ing, count in sorted_usage[:20]:
        print(f"  • {ing}: {count} recette(s)")
    
    print(f"\n🔍 VÉRIFICATION DE LA QUALITÉ")
    
    # Vérifier les ingrédients suspects
    suspects = []
    for ing in all_ingredients:
        # Caractères suspects
        if any(c in ing for c in ['"', ',', '(', ')', ':']):
            suspects.append(('Caractère suspect', ing))
        # Mots anglais communs
        elif any(word in ing.lower() for word in ['and', 'or', 'the', 'of', 'pieces', 'cubed', 'chopped', 'stalks']):
            suspects.append(('Mot anglais', ing))
        # Quantités
        elif re.search(r'\d+', ing):
            suspects.append(('Contient chiffre', ing))
        # Articles français
        elif any(ing.lower().startswith(art) for art in ['le ', 'la ', 'les ', 'du ', 'de la ', 'des ']):
            suspects.append(('Article', ing))
        # Prépositions courantes
        elif ' de ' in ing.lower() or ' à ' in ing.lower():
            # Mais certains sont OK comme "sauce de poisson", "sel d'ail"
            if ing not in ['sauce de poisson', 'sauce d\'huître', 'sel d\'ail', 'piment d\'Espelette', 
                          'sucre de palme', 'huile de sésame', 'huile de maïs', 'huile de piment',
                          'vin de cuisine', 'vinaigre de riz', 'vinaigre de vin', 'vinaigre de vin rouge',
                          'sauce de poisson', 'bouillon de poulet', 'feuille de laurier', 'feuille de combava',
                          'noix de cajou', 'noix de muscade', 'clou de girofle', 'zeste de citron',
                          'zeste de combava', 'farine de riz gluant', 'jus de citron', 'pain d\'épices',
                          'jaune d\'oeuf', 'graines de sésame', 'graines de sésame noir', 'pâte de crevette',
                          'pâte de piment', 'pâte de sésame', 'pâte de curry rouge', 'pâte de curry vert',
                          'radis daikon confit', 'concentré de tomate', 'bicarbonate de soude', 'bière brune',
                          'saucisse fumée', 'fécule de maïs', 'fécule de pomme de terre', 'huile de sésame grillée',
                          'cuisse de poulet', 'pilon de poulet', 'gîte de boeuf', 'épaule de porc',
                          'poitrine de porc', 'graisse de canard', 'boeuf haché', 'porc haché', 
                          'germes de soja', 'lait de coco', 'lait de soja', 'piment du Sichuan',
                          'piment en flocons', 'champignon shiitake', 'chou chinois', 'chou blanc',
                          'riz basmati', 'riz jasmin', 'nouilles de riz', 'nouilles ramen',
                          'pomme de terre', 'haricot vert', 'haricot kilomètre', 'petit pois',
                          'oignon rouge', 'oignon vert', 'poivron rouge', 'poivron vert', 'poivron jaune',
                          'piment rouge', 'piment séché', 'piment rouge séché', 'piment coréen',
                          'piment fort', 'piment moulu', 'piment doux', 'crevettes fermentées',
                          'crevettes séchées', 'bouquet garni', 'fond de veau', 'vin blanc', 'vin rouge',
                          'sauce tomate', 'sauce soja', 'sauce soja claire', 'sauce soja foncée',
                          'sauce sriracha', 'huile d\'olive', 'algue wakame', 'anis étoilé',
                          'asperge blanche', 'aubergine thaï', 'basilic thaï', 'citron vert', 'citron confit',
                          'sel fin', 'gros sel', 'fleur de sel', 'poivre blanc', 'sucre roux',
                          'crème fraîche', 'crème liquide', 'crème épaisse', 'tofu pressé', 'tofu soyeux',
                          'tofu ferme', 'moutarde japonaise', 'ciboulette chinoise', 'ciboulette coréenne',
                          'piment végétarien']:
                suspects.append(('Préposition suspect', ing))
    
    if suspects:
        print(f"  ⚠️  {len(suspects)} ingrédient(s) à vérifier:")
        for reason, ing in suspects:
            print(f"    • [{reason}] {ing}")
    else:
        print("  ✓ Tous les ingrédients semblent correctement normalisés!")
    
    print(f"\n✅ LISTE COMPLÈTE DES INGRÉDIENTS ({len(all_ingredients)})")
    for i, ing in enumerate(all_ingredients, 1):
        print(f"  {i:3d}. {ing}")
    
    print(f"\n" + "=" * 70)
    print("NORMALISATION TERMINÉE!")
    print("=" * 70)

if __name__ == "__main__":
    main()
