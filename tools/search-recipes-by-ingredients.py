#!/usr/bin/env python3
"""
Script de recherche de recettes par ingrédients.
Trouve les recettes basées sur une liste d'ingrédients disponibles.
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

try:
    import click
except ImportError:
    print("Error: Missing required package. Please run: pip install -r requirements.txt")
    sys.exit(1)


def read_recipe_file(filepath: Path) -> Tuple[Dict, str]:
    """Read a recipe file and return (frontmatter, content)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
    else:
        frontmatter = {}
        body = content
    
    return frontmatter, body


def normalize_ingredient(ingredient: str) -> str:
    """Normalize ingredient name for comparison."""
    return ingredient.strip().lower()


def calculate_match_score(recipe_ingredients: List[str], search_ingredients: List[str]) -> Tuple[int, List[str], List[str]]:
    """
    Calculate how many search ingredients match the recipe.
    Returns: (score, matched_ingredients, missing_ingredients)
    """
    recipe_norm = set(normalize_ingredient(ing) for ing in recipe_ingredients)
    search_norm = [normalize_ingredient(ing) for ing in search_ingredients]
    
    matched = []
    missing = []
    
    for search_ing in search_norm:
        # Check if search ingredient is in any recipe ingredient
        found = False
        for recipe_ing in recipe_norm:
            if search_ing in recipe_ing or recipe_ing in search_ing:
                matched.append(search_ing)
                found = True
                break
        
        if not found:
            missing.append(search_ing)
    
    return len(matched), matched, missing


def search_recipes_by_ingredients(
    vault_path: Path,
    search_ingredients: List[str],
    min_score: int = 1,
    show_missing: bool = False,
    exact_match: bool = False
) -> List[Dict]:
    """
    Search for recipes that contain the given ingredients.
    
    Args:
        vault_path: Path to Obsidian vault
        search_ingredients: List of ingredients to search for
        min_score: Minimum number of ingredients that must match
        show_missing: Show which ingredients are missing from each recipe
        exact_match: Only show recipes that have ALL the ingredients
    
    Returns:
        List of matching recipes with scores
    """
    recipes_dir = vault_path / 'contenus' / 'recettes' / 'Fiches'
    
    if not recipes_dir.exists():
        print(f"❌ Recipe directory not found: {recipes_dir}")
        return []
    
    results = []
    
    for recipe_file in recipes_dir.glob('*.md'):
        try:
            frontmatter, _ = read_recipe_file(recipe_file)
            
            # Skip if not a recipe or no ingredients
            recipe_ingredients = frontmatter.get('ingredients', [])
            if not recipe_ingredients:
                continue
            
            # Calculate match score
            score, matched, missing = calculate_match_score(recipe_ingredients, search_ingredients)
            
            # Apply filters
            if exact_match and len(missing) > 0:
                continue
            
            if score < min_score:
                continue
            
            # Prepare result
            result = {
                'name': recipe_file.stem,
                'score': score,
                'total_search': len(search_ingredients),
                'matched': matched,
                'missing': missing,
                'total_ingredients': len(recipe_ingredients),
                'all_ingredients': recipe_ingredients,
                'cuisine': frontmatter.get('type_cuisine', ''),
                'regime': frontmatter.get('regime', []),
                'temps_preparation': frontmatter.get('temps_preparation', 0),
                'temps_cuisson': frontmatter.get('temps_cuisson', 0),
            }
            
            results.append(result)
        
        except Exception as e:
            print(f"⚠️  Error reading {recipe_file.name}: {e}")
            continue
    
    # Sort by score (descending), then by name
    results.sort(key=lambda x: (-x['score'], x['name']))
    
    return results


def print_results(results: List[Dict], show_missing: bool = False, verbose: bool = False):
    """Print search results in a nice format."""
    if not results:
        print("\n❌ Aucune recette trouvée avec ces ingrédients.\n")
        return
    
    print(f"\n✅ {len(results)} recette(s) trouvée(s)\n")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        score_pct = (result['score'] / result['total_search']) * 100
        
        print(f"\n{i}. {result['name']}")
        print(f"   Score: {result['score']}/{result['total_search']} ({score_pct:.0f}%)")
        
        if result['cuisine']:
            print(f"   Cuisine: {result['cuisine']}")
        
        if result['regime']:
            print(f"   Régime: {', '.join(result['regime'])}")
        
        temps_total = result['temps_preparation'] + result['temps_cuisson']
        if temps_total > 0:
            print(f"   Temps: {result['temps_preparation']}min préparation + {result['temps_cuisson']}min cuisson = {temps_total}min total")
        
        print(f"   Ingrédients trouvés: {', '.join(result['matched'])}")
        
        if show_missing and result['missing']:
            print(f"   ⚠️  Ingrédients manquants: {', '.join(result['missing'])}")
        
        if verbose:
            print(f"   Total ingrédients dans la recette: {result['total_ingredients']}")
            print(f"   Tous les ingrédients: {', '.join(result['all_ingredients'][:10])}" + 
                  ("..." if len(result['all_ingredients']) > 10 else ""))
    
    print("\n" + "=" * 80)


@click.command()
@click.argument('ingredients', nargs=-1, required=True)
@click.option('--vault', default='.', help='Chemin vers le vault Obsidian', type=click.Path(exists=True))
@click.option('--min-score', default=1, help='Score minimum (nombre d\'ingrédients correspondants)', type=int)
@click.option('--exact', is_flag=True, help='Ne montrer que les recettes avec TOUS les ingrédients')
@click.option('--show-missing', is_flag=True, help='Afficher les ingrédients manquants')
@click.option('--verbose', '-v', is_flag=True, help='Affichage détaillé')
@click.option('--top', default=None, help='Limiter aux N meilleures recettes', type=int)
def main(ingredients, vault, min_score, exact, show_missing, verbose, top):
    """
    Rechercher des recettes par ingrédients.
    
    Exemples:
    
        # Recettes avec tomate et oignon
        python3 search-recipes-by-ingredients.py tomate oignon
        
        # Recettes avec au moins 3 des ingrédients listés
        python3 search-recipes-by-ingredients.py --min-score 3 tomate oignon ail basilic
        
        # Recettes avec TOUS ces ingrédients
        python3 search-recipes-by-ingredients.py --exact tomate basilic mozzarella
        
        # Afficher les ingrédients manquants
        python3 search-recipes-by-ingredients.py --show-missing tomate oignon
        
        # Top 10 des meilleures correspondances
        python3 search-recipes-by-ingredients.py --top 10 poulet riz
    """
    vault_path = Path(vault).resolve()
    
    print("🔍 Recherche de Recettes par Ingrédients")
    print("=" * 80)
    print(f"Vault: {vault_path}")
    print(f"Ingrédients recherchés: {', '.join(ingredients)}")
    print(f"Score minimum: {min_score}")
    if exact:
        print("Mode: TOUS les ingrédients requis")
    print("=" * 80)
    
    # Search recipes
    results = search_recipes_by_ingredients(
        vault_path,
        list(ingredients),
        min_score=min_score,
        show_missing=show_missing,
        exact_match=exact
    )
    
    # Limit results if requested
    if top and len(results) > top:
        results = results[:top]
    
    # Print results
    print_results(results, show_missing=show_missing, verbose=verbose)
    
    # Summary
    if results:
        print(f"\n💡 Astuce: Utilisez --show-missing pour voir quels ingrédients manquent")
        print(f"💡 Astuce: Utilisez --exact pour ne voir que les recettes complètes")
        print(f"💡 Astuce: Utilisez --top N pour limiter les résultats\n")


if __name__ == '__main__':
    main()
