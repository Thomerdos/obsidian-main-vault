#!/usr/bin/env python3
"""
Recipe migration script for Obsidian vault.
Transforms recipes with structured ingredient properties and creates ingredient pages.
"""

import os
import sys
import re
import time
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime
from collections import defaultdict

try:
    import click
    import requests
    from bs4 import BeautifulSoup
    from ratelimit import limits, sleep_and_retry
except ImportError as e:
    print(f"Error: Missing required package. Please run: pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)


# Tag transformation rules
TAG_TO_PROPERTY = {
    # Geographic/origin tags
    'RecetteDuSudOuest': ('origine', 'Sud-Ouest'),
    'RecetteItalienne': ('type_cuisine', 'Italienne'),
    'RecetteFrançaise': ('type_cuisine', 'Française'),
    'RecetteBasque': ('type_cuisine', 'Basque'),
    'RecetteChinoise': ('type_cuisine', 'Chinoise'),
    'RecetteJaponaise': ('type_cuisine', 'Japonaise'),
    'RecetteThaïlandaise': ('type_cuisine', 'Thaïlandaise'),
    'RecetteVietnamienne': ('type_cuisine', 'Vietnamienne'),
    'RecetteIndienne': ('type_cuisine', 'Indienne'),
    'RecetteMexicaine': ('type_cuisine', 'Mexicaine'),
    'RecetteGrec': ('type_cuisine', 'Grecque'),
    'RecetteTurque': ('type_cuisine', 'Turque'),
    'RecetteProvençale': ('origine', 'Provence'),
    'CuisineFrançaise': ('type_cuisine', 'Française'),
    
    # Diet/regime tags
    'RecetteVégétarienne': ('regime', 'végétarien'),
    'RecetteVégétalienne': ('regime', 'végétalien'),
    'RecetteVegan': ('regime', 'végétalien'),
    'SansGluten': ('regime', 'sans gluten'),
    'SansLactose': ('regime', 'sans lactose'),
    
    # Season tags
    "RecetteTouteL'année": ('saison', "toute l'année"),
    'RecetteHiver': ('saison', 'hiver'),
    'RecettePrintemps': ('saison', 'printemps'),
    'RecetteÉté': ('saison', 'été'),
    'RecetteAutomne': ('saison', 'automne'),
    'Hiver': ('saison', 'hiver'),
    'Printemps': ('saison', 'printemps'),
    'Été': ('saison', 'été'),
    'Automne': ('saison', 'automne'),
}

# Tags to ignore (difficulty tags we don't want)
TAGS_TO_IGNORE = {
    'RecetteFacile', 'RecetteMoyenne', 'RecetteDifficile',
    'ChoixDeLaRédaction', 'base'
}

# Properties to remove from old template
PROPERTIES_TO_REMOVE = {'categorie', 'difficulte', 'portions', 'nom', 'etapes', 'photo'}

# Rate limit for scraping: 1 request per 2 seconds
@sleep_and_retry
@limits(calls=1, period=2)
def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch URL content with rate limiting."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  ⚠️  Error fetching {url}: {e}")
        return None


def scrape_instructions(url: str) -> Optional[str]:
    """
    Scrape recipe instructions from various recipe websites.
    Supports: journaldesfemmes.fr, marmiton.org, ricardocuisine.com, 750g.com, etc.
    """
    html = fetch_url(url)
    if not html:
        return None
    
    soup = BeautifulSoup(html, 'lxml')
    instructions = []
    
    # Site-specific selectors
    selectors = [
        # journaldesfemmes.fr
        ('.recipe-steps li', 'text'),
        ('.rec_step', 'text'),
        
        # marmiton.org
        ('.recipe-steps__item', 'text'),
        ('.recipe-step-list__container', 'text'),
        
        # ricardocuisine.com
        ('.recipe__step', 'text'),
        
        # 750g.com
        ('.recipe-step-list__item', 'text'),
        
        # Generic selectors
        ('.instructions li', 'text'),
        ('.directions li', 'text'),
        ('.recipe-instructions li', 'text'),
        ('ol[itemprop="recipeInstructions"] li', 'text'),
    ]
    
    for selector, _ in selectors:
        elements = soup.select(selector)
        if elements:
            for i, elem in enumerate(elements, 1):
                text = elem.get_text(strip=True)
                if text and len(text) > 10:  # Filter out very short steps
                    instructions.append(f"- [ ] {text}")
            if instructions:
                break
    
    return '\n'.join(instructions) if instructions else None


def parse_ingredient_line(line: str) -> Optional[str]:
    """
    Extract ingredient name from a line like:
    - [ ] 600 g oignon
    - [ ] 3 unité poivron
    - [ ] quelque pincée sel
    
    Returns the ingredient name without quantity/unit.
    """
    line = line.strip()
    
    # Remove checkbox markers
    line = re.sub(r'^-\s*\[[ x]\]\s*', '', line)
    line = re.sub(r'^[-*]\s+', '', line)
    
    if not line:
        return None
    
    # Pattern: optional number, optional unit, then ingredient name
    # Match patterns like: "600 g oignon", "3 unité poivron", "quelque pincée sel"
    patterns = [
        r'^[\d,\.]+\s*(?:kg|g|mg|l|ml|cl|dl|unité|gousse|filet|pincée|cuillère|cas|cac|tasse)s?\s+(.+)$',
        r'^quelques?\s+(?:pincée|gousse|unité)s?\s+(.+)$',
        r'^\d+\s+(.+)$',  # Just number and name
        r'^(.+)$',  # Fallback: whole line
    ]
    
    for pattern in patterns:
        match = re.match(pattern, line, re.IGNORECASE)
        if match:
            ingredient = match.group(1).strip()
            # Clean up
            ingredient = re.sub(r'\s+', ' ', ingredient)
            ingredient = ingredient.lower()
            return ingredient
    
    return None


def normalize_ingredient_name(name: str) -> str:
    """
    Normalize ingredient name for consistency.
    Handles plural/singular, removes articles, etc.
    """
    if not name:
        return ""
    
    name = name.strip().lower()
    
    # Remove leading articles
    name = re.sub(r'^(le|la|les|l\'|un|une|des|du|de|d\')\s+', '', name)
    
    # Common plurals to singular (French)
    replacements = {
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
    }
    
    for plural, singular in replacements.items():
        if name == plural:
            return singular
    
    return name


def extract_ingredients_from_content(content: str) -> List[str]:
    """Extract ingredients from the ## Ingrédients section."""
    ingredients = []
    in_ingredients_section = False
    
    for line in content.split('\n'):
        if line.strip().startswith('## Ingrédients'):
            in_ingredients_section = True
            continue
        elif line.strip().startswith('##') and in_ingredients_section:
            break
        
        if in_ingredients_section and line.strip():
            ingredient = parse_ingredient_line(line)
            if ingredient:
                normalized = normalize_ingredient_name(ingredient)
                if normalized and normalized not in ingredients:
                    ingredients.append(normalized)
    
    return ingredients


def transform_tags(tags: List[str]) -> Dict[str, any]:
    """
    Transform tags into structured properties.
    Returns dict with new properties: origine, type_cuisine, regime, saison
    """
    new_props = {
        'origine': None,
        'type_cuisine': None,
        'regime': [],
        'saison': [],
    }
    
    for tag in tags:
        if tag in TAGS_TO_IGNORE:
            continue
        
        if tag in TAG_TO_PROPERTY:
            prop_name, value = TAG_TO_PROPERTY[tag]
            if prop_name in ['regime', 'saison']:
                if value not in new_props[prop_name]:
                    new_props[prop_name].append(value)
            else:
                # For origine and type_cuisine, keep the last one
                new_props[prop_name] = value
    
    return new_props


def read_recipe_file(filepath: Path) -> Tuple[Dict, str]:
    """
    Read a recipe file and return (frontmatter, content).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
    else:
        frontmatter = {}
        body = content
    
    return frontmatter, body


def write_recipe_file(filepath: Path, frontmatter: Dict, content: str):
    """Write recipe file with frontmatter and content."""
    # Clean up frontmatter - remove None values and empty lists
    cleaned_fm = {}
    for key, value in frontmatter.items():
        if value is not None:
            if isinstance(value, list) and len(value) == 0:
                continue
            cleaned_fm[key] = value
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(cleaned_fm, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        f.write('---\n\n')
        f.write(content)


def update_ingredients_section(content: str, ingredients: List[str]) -> str:
    """
    Update the ## Ingrédients section to include wiki links.
    Preserves quantities but adds [[ingredient]] links.
    """
    lines = content.split('\n')
    updated_lines = []
    in_ingredients_section = False
    
    for line in lines:
        if line.strip().startswith('## Ingrédients'):
            in_ingredients_section = True
            updated_lines.append(line)
            continue
        elif line.strip().startswith('##') and in_ingredients_section:
            in_ingredients_section = False
        
        if in_ingredients_section and line.strip():
            # Try to add wiki link to ingredient
            ingredient = parse_ingredient_line(line)
            if ingredient:
                normalized = normalize_ingredient_name(ingredient)
                if normalized:
                    # Replace ingredient name with wiki link
                    # Keep the quantity part
                    line_clean = re.sub(r'^-\s*\[[ x]\]\s*', '- ', line)
                    # Try to find where the ingredient name starts
                    for ing in ingredients:
                        if ing == normalized:
                            # Simple replacement: add [[ ]] around the ingredient
                            if ing in line_clean.lower():
                                # Find the ingredient in the line and wrap it
                                pattern = re.compile(re.escape(ing), re.IGNORECASE)
                                line_clean = pattern.sub(f'[[{ing}]]', line_clean, count=1)
                            break
                    updated_lines.append(line_clean)
                    continue
        
        updated_lines.append(line)
    
    return '\n'.join(updated_lines)


def create_ingredient_page(vault_path: Path, ingredient: str, recipes: List[str]):
    """Create an ingredient page in contenus/recettes/Ingredients/"""
    ingredients_dir = vault_path / 'contenus' / 'recettes' / 'Ingredients'
    ingredients_dir.mkdir(parents=True, exist_ok=True)
    
    # Capitalize first letter for filename
    filename = ingredient.capitalize() + '.md'
    filepath = ingredients_dir / filename
    
    if filepath.exists():
        # Update existing file with new recipes
        frontmatter, content = read_recipe_file(filepath)
        existing_recipes = frontmatter.get('recettes', [])
        for recipe in recipes:
            if recipe not in existing_recipes:
                existing_recipes.append(recipe)
        frontmatter['recettes'] = sorted(existing_recipes)
        write_recipe_file(filepath, frontmatter, content)
        return False  # Not newly created
    
    # Create new ingredient page
    frontmatter = {
        'type': 'ingredient',
        'nom': ingredient,
        'categorie': '',
        'recettes': sorted(recipes),
        'allergenes': [],
        'saison': [],
        'tags': ['ingredient']
    }
    
    content = f"""# 🥕 {ingredient.capitalize()}

## 📋 Informations

- **Catégorie**: 
- **Saison**: 
- **Allergènes**: 

## 🍽️ Utilisé dans les recettes

```dataview
TABLE WITHOUT ID
  file.link as "Recette",
  temps_preparation as "Préparation (min)",
  temps_cuisson as "Cuisson (min)",
  type_cuisine as "Cuisine"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, "{ingredient}")
SORT file.name ASC
```

## 💡 Notes


## 🔗 Liens
"""
    
    write_recipe_file(filepath, frontmatter, content)
    return True  # Newly created


def process_recipe(filepath: Path, vault_path: Path, scrape: bool = False, dry_run: bool = False) -> Dict:
    """
    Process a single recipe file.
    Returns a dict with processing stats and changes.
    """
    result = {
        'filepath': filepath,
        'success': False,
        'ingredients_found': [],
        'properties_added': [],
        'instructions_scraped': False,
        'errors': [],
    }
    
    try:
        # Read recipe
        frontmatter, content = read_recipe_file(filepath)
        
        # Check if it's a recipe - must have either type='recette' or a tag starting with 'Recette'
        tags = frontmatter.get('tags', [])
        is_recipe = (frontmatter.get('type') == 'recette' or 
                    'recette' in tags or
                    any(tag.startswith('Recette') for tag in tags))
        
        if not is_recipe:
            result['errors'].append('Not a recipe file')
            return result
        
        # Extract ingredients from content
        ingredients = extract_ingredients_from_content(content)
        result['ingredients_found'] = ingredients
        
        # Transform tags to properties
        tags = frontmatter.get('tags', [])
        new_props = transform_tags(tags)
        
        # Update frontmatter
        modified = False
        
        # Add ingredients list
        if ingredients and 'ingredients' not in frontmatter:
            frontmatter['ingredients'] = ingredients
            result['properties_added'].append('ingredients')
            modified = True
        
        # Add transformed properties
        for prop, value in new_props.items():
            if value:  # Only add non-empty values
                if prop not in frontmatter or not frontmatter[prop]:
                    frontmatter[prop] = value
                    result['properties_added'].append(prop)
                    modified = True
        
        # Remove deprecated properties
        for prop in PROPERTIES_TO_REMOVE:
            if prop in frontmatter:
                del frontmatter[prop]
                modified = True
        
        # Ensure type is set correctly
        if 'type' not in frontmatter:
            frontmatter['type'] = 'recette'
            modified = True
        
        # Check if instructions are missing or empty
        if scrape and 'source' in frontmatter:
            if '## Instructions' in content:
                # Check if instructions section is empty or minimal
                instructions_match = re.search(r'## Instructions\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
                if instructions_match:
                    instructions_content = instructions_match.group(1).strip()
                    if len(instructions_content) < 50:  # Very minimal instructions
                        print(f"  🌐 Scraping instructions from {frontmatter['source']}")
                        scraped = scrape_instructions(frontmatter['source'])
                        if scraped:
                            # Replace instructions section
                            content = re.sub(
                                r'(## Instructions\s*\n).*?(?=\n##|\Z)',
                                r'\1\n' + scraped + '\n\n',
                                content,
                                flags=re.DOTALL
                            )
                            result['instructions_scraped'] = True
                            modified = True
        
        # Update ingredients section with wiki links
        if ingredients:
            new_content = update_ingredients_section(content, ingredients)
            if new_content != content:
                content = new_content
                modified = True
        
        # Write changes
        if modified and not dry_run:
            write_recipe_file(filepath, frontmatter, content)
        
        result['success'] = True
        result['modified'] = modified
        
    except Exception as e:
        result['errors'].append(str(e))
    
    return result


def migrate_recipes(vault_path: Path, scrape: bool = False, dry_run: bool = False, recipe_name: Optional[str] = None):
    """
    Main migration function.
    """
    recipes_dir = vault_path / 'contenus' / 'recettes' / 'Fiches'
    
    if not recipes_dir.exists():
        print(f"❌ Recipe directory not found: {recipes_dir}")
        return
    
    print(f"🔍 Scanning recipes in {recipes_dir}")
    
    if dry_run:
        print("⚠️  DRY RUN MODE - No files will be modified")
    
    # Get all recipe files
    if recipe_name:
        recipe_files = [f for f in recipes_dir.glob('*.md') if recipe_name.lower() in f.stem.lower()]
        if not recipe_files:
            print(f"❌ No recipe found matching: {recipe_name}")
            return
    else:
        recipe_files = list(recipes_dir.glob('*.md'))
    
    print(f"📚 Found {len(recipe_files)} recipe(s) to process\n")
    
    # Statistics
    stats = {
        'total': len(recipe_files),
        'processed': 0,
        'modified': 0,
        'errors': 0,
        'ingredients_found': set(),
        'ingredients_created': 0,
        'instructions_scraped': 0,
    }
    
    # Track ingredients to recipes mapping
    ingredient_to_recipes = defaultdict(list)
    
    # Process each recipe
    for i, recipe_file in enumerate(recipe_files, 1):
        print(f"[{i}/{len(recipe_files)}] Processing: {recipe_file.name}")
        
        result = process_recipe(recipe_file, vault_path, scrape=scrape, dry_run=dry_run)
        
        if result['success']:
            stats['processed'] += 1
            if result.get('modified'):
                stats['modified'] += 1
            
            # Track ingredients
            for ingredient in result['ingredients_found']:
                stats['ingredients_found'].add(ingredient)
                ingredient_to_recipes[ingredient].append(recipe_file.stem)
            
            if result['instructions_scraped']:
                stats['instructions_scraped'] += 1
            
            # Print what was done
            if result.get('modified') or dry_run:
                if result['properties_added']:
                    print(f"  ✓ Added properties: {', '.join(result['properties_added'])}")
                if result['ingredients_found']:
                    print(f"  ✓ Found {len(result['ingredients_found'])} ingredients")
                if result['instructions_scraped']:
                    print(f"  ✓ Scraped instructions")
        else:
            stats['errors'] += 1
            print(f"  ❌ Error: {', '.join(result['errors'])}")
        
        print()
    
    # Create ingredient pages
    if not dry_run:
        print("\n🥕 Creating ingredient pages...")
        for ingredient, recipes in ingredient_to_recipes.items():
            created = create_ingredient_page(vault_path, ingredient, recipes)
            if created:
                stats['ingredients_created'] += 1
                print(f"  ✓ Created: {ingredient.capitalize()}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 MIGRATION SUMMARY")
    print("="*60)
    print(f"Total recipes: {stats['total']}")
    print(f"Processed: {stats['processed']}")
    print(f"Modified: {stats['modified']}")
    print(f"Errors: {stats['errors']}")
    print(f"Unique ingredients found: {len(stats['ingredients_found'])}")
    print(f"Ingredient pages created: {stats['ingredients_created']}")
    print(f"Instructions scraped: {stats['instructions_scraped']}")
    
    # Generate report
    if not dry_run:
        generate_report(vault_path, stats, ingredient_to_recipes)


def generate_report(vault_path: Path, stats: Dict, ingredient_to_recipes: Dict):
    """Generate migration report."""
    report_path = vault_path / 'migration-report.md'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# Migration Report\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"## Summary\n\n")
        f.write(f"- Total recipes: {stats['total']}\n")
        f.write(f"- Processed: {stats['processed']}\n")
        f.write(f"- Modified: {stats['modified']}\n")
        f.write(f"- Errors: {stats['errors']}\n")
        f.write(f"- Unique ingredients: {len(stats['ingredients_found'])}\n")
        f.write(f"- Ingredient pages created: {stats['ingredients_created']}\n")
        f.write(f"- Instructions scraped: {stats['instructions_scraped']}\n\n")
        
        f.write(f"## Ingredients Found\n\n")
        for ingredient in sorted(stats['ingredients_found']):
            count = len(ingredient_to_recipes[ingredient])
            f.write(f"- **{ingredient}** ({count} recipe{'s' if count > 1 else ''})\n")
    
    print(f"\n📄 Report saved to: {report_path}")


@click.command()
@click.option('--vault', default='.', help='Path to Obsidian vault', type=click.Path(exists=True))
@click.option('--dry-run', is_flag=True, help='Show what would be done without modifying files')
@click.option('--scrape', is_flag=True, help='Scrape missing instructions from source URLs')
@click.option('--recipe', default=None, help='Process only a specific recipe (partial name match)')
def main(vault, dry_run, scrape, recipe):
    """
    Migrate recipe files to new structured format.
    
    This script will:
    - Extract and normalize ingredients
    - Transform tags to structured properties
    - Create ingredient pages
    - Optionally scrape missing instructions
    
    Examples:
        python3 migrate-recipes.py --dry-run
        python3 migrate-recipes.py --scrape
        python3 migrate-recipes.py --recipe "Piperade"
    """
    vault_path = Path(vault).resolve()
    
    print("🍳 Recipe Migration Script")
    print("="*60)
    print(f"Vault: {vault_path}")
    print(f"Scrape instructions: {'Yes' if scrape else 'No'}")
    print(f"Dry run: {'Yes' if dry_run else 'No'}")
    if recipe:
        print(f"Filter: {recipe}")
    print("="*60 + "\n")
    
    migrate_recipes(vault_path, scrape=scrape, dry_run=dry_run, recipe_name=recipe)


if __name__ == '__main__':
    main()
