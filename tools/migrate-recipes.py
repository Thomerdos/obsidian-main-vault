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
    Extract ONLY the main ingredient name from a line like:
    - [ ] 600 g oignon
    - [ ] 3 unité poivron
    - [ ] 1¾ cups coconut milk (divided)
    - [ ] 2 Tablespoons finely chopped palm sugar
    
    Returns ONLY the main ingredient name without quantity/unit/preparation/notes.
    Example: "2 tbsp finely chopped fresh basil" → "basil"
    """
    line = line.strip()
    
    # Remove checkbox markers
    line = re.sub(r'^-\s*\[[ x]\]\s*', '', line)
    line = re.sub(r'^[-*]\s+', '', line)
    
    # Remove existing wikilinks (clean up malformed ones too)
    line = re.sub(r'\[\[+', '', line)
    line = re.sub(r'\]\]+', '', line)
    
    if not line or len(line) < 2:
        return None
    
    # Remove notes in parentheses first (like "(divided)", "(see note 1)")
    line_without_notes = re.sub(r'\([^)]*\)', '', line).strip()
    
    # Pattern: optional number/fraction, optional unit, then ingredient name
    # Extended to handle English units and more complex patterns
    patterns = [
        # French units with "de"
        r'^[\d,\.¼½¾⅓⅔⅛⅜⅝⅞]+\s*(?:kg|g|mg|l|ml|cl|dl|unité|unités|gousse|gousses|filet|filets|pincée|pincées|cuillère|cuillères|cas|cac|tasse|tasses|branche|branches|feuille|feuilles|brin|brins)s?\s+(?:de\s+)?(.+)$',
        # English units with "of"
        r'^[\d,\.¼½¾⅓⅔⅛⅜⅝⅞/\s-]+(?:cup|cups|tablespoon|tablespoons|tbsp|tsp|teaspoon|teaspoons|ounce|ounces|oz|pound|pounds|lb|lbs|serving|servings|stalk|stalks|piece|pieces|clove|cloves|pinch)s?\s+(?:of\s+)?(.+)$',
        # Words like "quelques"
        r'^quelques?\s+(?:pincée|pincées|gousse|gousses|unité|unités|branche|branches|feuille|feuilles|brin|brins)s?\s+(?:de\s+)?(.+)$',
        # Just number and name
        r'^[\d,\.¼½¾⅓⅔⅛⅜⅝⅞/\s-]+(.+)$',
    ]
    
    ingredient = None
    for pattern in patterns:
        match = re.match(pattern, line_without_notes, re.IGNORECASE)
        if match:
            ingredient = match[1].strip()
            break
    
    # Fallback: if line doesn't start with number, might be just the ingredient
    if not ingredient:
        if not re.match(r'^[\d,\.\s-]', line_without_notes):
            ingredient = line_without_notes
    
    if not ingredient or len(ingredient) < 2:
        return None
    
    # Clean up whitespace
    ingredient = re.sub(r'\s+', ' ', ingredient)
    
    # Remove preparation descriptors at the start
    ingredient = re.sub(r'^(?:finely\s+|roughly\s+|thinly\s+|thickly\s+|coarsely\s+)?(?:chopped|diced|minced|sliced|grated|shredded|crushed|pressed|cut|torn|packed|peeled|washed|cleaned|trimmed|drained|rinsed|soaked)\s+', '', ingredient, flags=re.IGNORECASE)
    
    # Remove preparation descriptors after commas (e.g., "sugar, chopped" → "sugar")
    ingredient = re.sub(r',\s*(?:finely\s+|roughly\s+|thinly\s+)?(?:chopped|diced|minced|sliced|grated|shredded|crushed|cut|torn|packed).*$', '', ingredient, flags=re.IGNORECASE)
    
    # Remove "cut into..." or "sliced into..." patterns
    ingredient = re.sub(r',?\s+(?:cut|sliced|chopped|diced)\s+into\s+.*$', '', ingredient, flags=re.IGNORECASE)
    
    # Remove size/quality descriptors at the start (medium, large, small, fresh, dried, etc.)
    ingredient = re.sub(r'^(?:small|medium|large|extra-large|fresh|dried|dry|frozen|canned|bottled|unsalted|salted|raw|cooked|roasted|toasted)\s+', '', ingredient, flags=re.IGNORECASE)
    
    # Remove "size" after ingredient (e.g., "onion, medium size" → "onion")
    ingredient = re.sub(r',?\s*(?:medium|large|small)\s+size.*$', '', ingredient, flags=re.IGNORECASE)
    
    # Remove measurement-related endings (e.g., "soak in room temp water for 1 hour")
    ingredient = re.sub(r',?\s+(?:soak|soaked)\s+in\s+.*$', '', ingredient, flags=re.IGNORECASE)
    
    # Skip if it starts with "à " (like "à soupe") or "of " or "to " or "for "
    if ingredient.lower().startswith(('à ', 'of ', 'to ', 'for ', 'into ', 'about ')):
        return None
    
    # Skip if still has numbers at the start (like "1/4 chou")
    if re.match(r'^[\d/\s-]+$', ingredient) or re.match(r'^[\d/]', ingredient):
        return None
    
    # Skip very short results
    if len(ingredient) < 2:
        return None
    
    # Clean trailing dots, commas, etc.
    ingredient = ingredient.rstrip('.,;:')
    
    return ingredient.lower()


# English to French ingredient mappings (for normalization)
INGREDIENT_MAPPINGS = {
    # Liquids & Dairy
    'coconut milk': 'lait de coco',
    'chicken stock': 'bouillon de poulet',
    'fish sauce': 'sauce de poisson',
    'soy sauce': 'sauce soja',
    'oyster sauce': 'sauce huître',
    'heavy cream': 'crème épaisse',
    'milk': 'lait',
    'water': 'eau',
    
    # Sugars & Sweeteners
    'palm sugar': 'sucre de palme',
    'brown sugar': 'sucre brun',
    'sugar': 'sucre',
    
    # Proteins
    'chicken thigh': 'cuisses de poulet',
    'chicken thighs': 'cuisses de poulet',
    'chicken breast': 'blanc de poulet',
    'shrimp': 'crevettes',
    'dried shrimp': 'crevettes séchées',
    'tofu': 'tofu',
    'pressed tofu': 'tofu pressé',
    
    # Vegetables
    'thai eggplant': 'aubergine thaï',
    'eggplant': 'aubergine',
    'thai basil': 'basilic thaï',
    'basil': 'basilic',
    'garlic': 'ail',
    'garlic chives': 'ail chives',
    'onion': 'oignon',
    'onions': 'oignon',
    'tomato': 'tomate',
    'tomatoes': 'tomate',
    'carrot': 'carotte',
    'carrots': 'carotte',
    'bell pepper': 'poivron',
    'bell peppers': 'poivron',
    'green beans': 'haricots verts',
    'bean sprouts': 'germes de soja',
    
    # Spices & Seasonings
    'makrut lime leaves': 'feuilles de combava',
    'lime leaves': 'feuilles de combava',
    'chili': 'piment',
    'chili flakes': 'piment en flocons',
    'dried chili flakes': 'piment séché en flocons',
    'salt': 'sel',
    'pepper': 'poivre',
    'black pepper': 'poivre noir',
    
    # Noodles & Rice
    'rice noodles': 'nouilles de riz',
    'dry rice noodles': 'nouilles de riz sèches',
    'rice': 'riz',
    
    # Others
    'tamarind': 'tamarin',
    'thai cooking tamarind': 'tamarin thaïlandais',
    'peanuts': 'cacahuètes',
    'roasted peanuts': 'cacahuètes grillées',
    'lime': 'citron vert',
    'lemon': 'citron',
    'oil': 'huile',
    'vegetable oil': 'huile végétale',
    'olive oil': "huile d'olive",
    'butter': 'beurre',
    'eggs': 'oeufs',
    'egg': 'oeuf',
}

def normalize_ingredient_name(name: str) -> str:
    """
    Normalize ingredient name for consistency.
    Handles plural/singular, removes articles, translates English to French.
    Priority: French names, singular form, no articles.
    """
    if not name:
        return ""
    
    name = name.strip().lower()
    
    # Remove leading articles (French and English)
    name = re.sub(r'^(le|la|les|l\'|un|une|des|du|de|d\'|the|a|an|some)\s+', '', name)
    
    # Check if it's in our English-to-French mapping
    if name in INGREDIENT_MAPPINGS:
        return INGREDIENT_MAPPINGS[name]
    
    # Common plurals to singular (French)
    replacements = {
        'oignons': 'oignon',
        'tomates': 'tomate',
        'carottes': 'carotte',
        'pommes de terre': 'pomme de terre',
        "gousses d'ail": 'ail',
        'gousses ail': 'ail',
        'piments': 'piment',
        'poivrons': 'poivron',
        'aubergines': 'aubergine',
        'courgettes': 'courgette',
        'champignons': 'champignon',
        'échalotes': 'échalote',
        'oeufs': 'oeuf',
    }
    
    # Check exact match first
    if name in replacements:
        return replacements[name]
    
    # Try removing 's' at the end for English plurals and check mapping again
    if name.endswith('s') and len(name) > 3:
        singular = name[:-1]
        if singular in INGREDIENT_MAPPINGS:
            return INGREDIENT_MAPPINGS[singular]
    
    return name


def extract_ingredients_from_content(content: str) -> List[str]:
    """Extract ingredients from the ## Ingrédients section."""
    ingredients = []
    in_ingredients_section = False
    
    for line in content.split('\n'):
        if line.strip().startswith('## Ingrédients') or line.strip().startswith('## Ingredients'):
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
    
    if tags is None:
        return new_props
    
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


def create_ingredient_page(vault_path: Path, ingredient: str, recipes: List[str]):
    """Create an ingredient page in contenus/recettes/Ingredients/"""
    ingredients_dir = vault_path / 'contenus' / 'recettes' / 'Ingredients'
    ingredients_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize filename - remove invalid characters
    ingredient_clean = ingredient.replace('/', '-').replace('\\', '-').strip()
    # Remove special characters that are invalid in filenames
    ingredient_clean = re.sub(r'[<>:"|?*]', '', ingredient_clean)
    # Remove parentheses for cleaner filenames
    ingredient_clean = re.sub(r'[()]', '', ingredient_clean)
    # Limit length for filename
    if len(ingredient_clean) > 100:
        ingredient_clean = ingredient_clean[:100]
    
    # Capitalize first letter for filename
    filename = ingredient_clean.capitalize() + '.md'
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
  source as "Source",
  temps_preparation as "Préparation",
  temps_cuisson as "Cuisson"
FROM "contenus/recettes/Fiches"
WHERE contains(ingredients, this.file.link)
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
        
        # Check if it's a recipe - be lenient
        tags = frontmatter.get('tags', [])
        if tags is None:
            tags = []
        
        # It's a recipe if:
        # 1. Has type='recette', OR
        # 2. Has 'recette' tag, OR
        # 3. Has any tag starting with 'Recette', OR
        # 4. Has an ## Ingrédients section (most reliable indicator)
        is_recipe = (
            frontmatter.get('type') == 'recette' or 
            'recette' in tags or
            any(tag.startswith('Recette') for tag in tags) or
            '## Ingrédients' in content or
            '## Ingredients' in content
        )
        
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
        
        # Add/update ingredients list with wikilinks in frontmatter ONLY
        if ingredients:
            # Create wikilinks for frontmatter
            ingredients_with_links = [f"[[{ing}]]" for ing in ingredients]
            
            # Always update if ingredients changed
            existing_ingredients = frontmatter.get('ingredients', [])
            if existing_ingredients != ingredients_with_links:
                frontmatter['ingredients'] = ingredients_with_links
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
        
        # NOTE: We DO NOT modify the text of the ingredients section
        # Wikilinks are ONLY in the frontmatter
        
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
