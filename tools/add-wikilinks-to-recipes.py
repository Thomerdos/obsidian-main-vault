#!/usr/bin/env python3
"""
Script to add wikilinks [[ingredient]] to recipe files.

This script:
1. Reads ingredient list from frontmatter
2. Finds ingredients in the "## Ingrédients" section
3. Adds wikilinks [[ingredient]] if not already present
4. Handles plurals, articles, and other linguistic variations
5. Generates a detailed migration report
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple, Optional


class WikilinkAdder:
    """Main class to handle wikilink addition to recipes."""
    
    def __init__(self, vault_path: str, dry_run: bool = False):
        self.vault_path = Path(vault_path)
        self.recipes_dir = self.vault_path / "contenus" / "recettes" / "Fiches"
        self.dry_run = dry_run
        self.stats = {
            'total_recipes': 0,
            'recipes_modified': 0,
            'wikilinks_added': 0,
            'wikilinks_fixed': 0,
            'errors': []
        }
        self.details = []
    
    def normalize_ingredient(self, ingredient: str) -> str:
        """Normalize ingredient name for matching."""
        # Remove extra spaces
        ingredient = ' '.join(ingredient.split())
        # Remove leading articles
        ingredient = re.sub(r"^(d'|de |des |du |la |le |les |l'|un |une )", '', ingredient, flags=re.IGNORECASE)
        return ingredient.strip().lower()
    
    def generate_ingredient_patterns(self, ingredient: str) -> List[str]:
        """
        Generate possible variations of an ingredient name.
        Returns patterns to search for in the text.
        """
        patterns = []
        ingredient_lower = ingredient.lower()
        
        # Base form
        patterns.append(ingredient_lower)
        
        # Common plural forms
        if not ingredient_lower.endswith('s'):
            patterns.append(ingredient_lower + 's')
        if ingredient_lower.endswith('au'):
            patterns.append(ingredient_lower + 'x')
        if ingredient_lower.endswith('al'):
            patterns.append(ingredient_lower[:-2] + 'aux')
        
        # With articles
        patterns.extend([
            f"d'{ingredient_lower}",
            f"de {ingredient_lower}",
            f"des {ingredient_lower}",
            f"du {ingredient_lower}",
            f"la {ingredient_lower}",
            f"le {ingredient_lower}",
            f"les {ingredient_lower}",
            f"l'{ingredient_lower}",
            f"un {ingredient_lower}",
            f"une {ingredient_lower}",
        ])
        
        # Sort by length (longest first) to match longer patterns first
        patterns.sort(key=len, reverse=True)
        
        return patterns
    
    def find_ingredient_in_line(self, ingredient: str, line: str) -> Optional[Tuple[str, int, int]]:
        """
        Find an ingredient in a line of text.
        Returns (matched_text, start_pos, end_pos) or None.
        """
        patterns = self.generate_ingredient_patterns(ingredient)
        line_lower = line.lower()
        
        for pattern in patterns:
            # Look for the pattern not already in wikilinks
            # Search for pattern that's not between [[ ]]
            pos = 0
            while pos < len(line_lower):
                idx = line_lower.find(pattern, pos)
                if idx == -1:
                    break
                
                # Check if this is already inside wikilinks
                # Look backwards for [[ and forwards for ]]
                before = line[:idx]
                after = line[idx + len(pattern):]
                
                # Count [[ and ]] before this position
                open_count = before.count('[[') - before.count(']]')
                
                # If open_count > 0, we're inside wikilinks, skip this match
                if open_count > 0:
                    pos = idx + 1
                    continue
                
                # Found a valid match
                # Get the actual matched text from original line (preserving case)
                matched_text = line[idx:idx + len(pattern)]
                return (matched_text, idx, idx + len(pattern))
        
        return None
    
    def fix_malformed_wikilinks(self, line: str) -> Tuple[str, int]:
        """
        Fix malformed wikilinks like [[[[ingredient]]]] to [[ingredient]].
        Returns (fixed_line, number_of_fixes).
        """
        fixes = 0
        # Fix multiple opening brackets
        while '[[[[' in line:
            line = line.replace('[[[[', '[[')
            fixes += 1
        # Fix multiple closing brackets
        while ']]]]' in line:
            line = line.replace(']]]]', ']]')
            fixes += 1
        return line, fixes
    
    def add_wikilink_to_line(self, line: str, ingredient: str) -> Tuple[str, bool]:
        """
        Add wikilink around ingredient in line if not already present.
        Returns (modified_line, was_modified).
        """
        # First fix any malformed wikilinks
        line, fixes = self.fix_malformed_wikilinks(line)
        was_modified = fixes > 0
        
        if fixes > 0:
            self.stats['wikilinks_fixed'] += fixes
        
        # Find the ingredient in the line
        match = self.find_ingredient_in_line(ingredient, line)
        
        if match:
            matched_text, start, end = match
            # Add wikilinks
            new_line = line[:start] + '[[' + matched_text + ']]' + line[end:]
            return new_line, True
        
        return line, was_modified
    
    def extract_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """
        Extract YAML frontmatter from markdown content.
        Returns (frontmatter_dict, remaining_content).
        """
        # Match frontmatter between --- markers
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if not match:
            return {}, content
        
        frontmatter_text = match.group(1)
        remaining = match.group(2)
        
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter or {}, remaining
        except yaml.YAMLError as e:
            print(f"  ⚠️  YAML parsing error: {e}")
            return {}, content
    
    def process_ingredients_section(self, content: str, ingredients: List[str]) -> Tuple[str, int]:
        """
        Process the ## Ingrédients section and add wikilinks.
        Returns (modified_content, number_of_wikilinks_added).
        """
        lines = content.split('\n')
        wikilinks_added = 0
        in_ingredients_section = False
        result_lines = []
        
        for line in lines:
            # Check if we're entering or leaving the ingredients section
            if re.match(r'^##\s+Ingrédients\s*$', line, re.IGNORECASE):
                in_ingredients_section = True
                result_lines.append(line)
                continue
            elif in_ingredients_section and re.match(r'^##\s+', line):
                # Entering a new section, stop processing
                in_ingredients_section = False
                result_lines.append(line)
                continue
            
            # Process ingredient lines
            if in_ingredients_section and line.strip():
                # This is an ingredient line
                modified_line = line
                line_modified = False
                
                # Try to add wikilinks for each ingredient
                for ingredient in ingredients:
                    new_line, was_modified = self.add_wikilink_to_line(modified_line, ingredient)
                    if was_modified and new_line != modified_line:
                        wikilinks_added += 1
                        line_modified = True
                    modified_line = new_line
                
                result_lines.append(modified_line)
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines), wikilinks_added
    
    def process_recipe_file(self, filepath: Path) -> bool:
        """
        Process a single recipe file.
        Returns True if file was modified.
        """
        try:
            # Read the file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            frontmatter, body = self.extract_frontmatter(content)
            
            # Get ingredients list
            ingredients = frontmatter.get('ingredients', [])
            if not ingredients:
                return False
            
            # Normalize ingredients
            normalized_ingredients = [self.normalize_ingredient(ing) for ing in ingredients]
            
            # Process the ingredients section
            modified_body, wikilinks_added = self.process_ingredients_section(body, normalized_ingredients)
            
            if wikilinks_added > 0 or modified_body != body:
                # Reconstruct the file
                frontmatter_text = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
                new_content = f"---\n{frontmatter_text}---\n{modified_body}"
                
                # Write back to file (unless dry-run)
                if not self.dry_run:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                
                self.stats['wikilinks_added'] += wikilinks_added
                self.details.append({
                    'recipe': filepath.name,
                    'wikilinks_added': wikilinks_added,
                    'ingredients': normalized_ingredients
                })
                
                return True
            
            return False
            
        except Exception as e:
            error_msg = f"{filepath.name}: {str(e)}"
            self.stats['errors'].append(error_msg)
            print(f"  ❌ Error processing {filepath.name}: {e}")
            return False
    
    def process_all_recipes(self):
        """Process all recipe files in the recipes directory."""
        if not self.recipes_dir.exists():
            print(f"❌ Recipes directory not found: {self.recipes_dir}")
            return
        
        print(f"🔍 Scanning recipes in: {self.recipes_dir}")
        print(f"{'[DRY RUN] ' if self.dry_run else ''}Processing...\n")
        
        recipe_files = sorted(self.recipes_dir.glob("*.md"))
        self.stats['total_recipes'] = len(recipe_files)
        
        for filepath in recipe_files:
            print(f"Processing: {filepath.name}")
            was_modified = self.process_recipe_file(filepath)
            if was_modified:
                self.stats['recipes_modified'] += 1
                print(f"  ✅ Modified")
            else:
                print(f"  ⏭️  No changes needed")
        
        print("\n" + "="*70)
        self.print_summary()
        self.generate_report()
    
    def print_summary(self):
        """Print summary statistics."""
        print("\n📊 SUMMARY")
        print("="*70)
        print(f"Total recipes processed: {self.stats['total_recipes']}")
        print(f"Recipes modified: {self.stats['recipes_modified']}")
        print(f"Wikilinks added: {self.stats['wikilinks_added']}")
        print(f"Wikilinks fixed (malformed): {self.stats['wikilinks_fixed']}")
        print(f"Errors: {len(self.stats['errors'])}")
        
        if self.stats['errors']:
            print("\n⚠️  ERRORS:")
            for error in self.stats['errors']:
                print(f"  - {error}")
    
    def generate_report(self):
        """Generate a detailed migration report."""
        report_path = self.vault_path / "wikilinks-migration-report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Rapport d'ajout de wikilinks aux recettes\n\n")
            f.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Mode : {'DRY RUN (aucune modification)' if self.dry_run else 'EXECUTION (fichiers modifiés)'}\n\n")
            
            f.write("## Résumé\n\n")
            f.write(f"- Recettes traitées : {self.stats['total_recipes']}\n")
            f.write(f"- Recettes modifiées : {self.stats['recipes_modified']}\n")
            f.write(f"- Wikilinks ajoutés : {self.stats['wikilinks_added']}\n")
            f.write(f"- Wikilinks corrigés : {self.stats['wikilinks_fixed']}\n")
            f.write(f"- Erreurs : {len(self.stats['errors'])}\n\n")
            
            if self.details:
                f.write("## Détails par recette\n\n")
                for detail in self.details:
                    f.write(f"### {detail['recipe']}\n\n")
                    f.write(f"- Wikilinks ajoutés : {detail['wikilinks_added']}\n")
                    f.write(f"- Ingrédients : {', '.join(f'[[{ing}]]' for ing in detail['ingredients'])}\n\n")
            
            if self.stats['errors']:
                f.write("## Erreurs\n\n")
                for error in self.stats['errors']:
                    f.write(f"- {error}\n")
        
        print(f"\n📄 Report generated: {report_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Add wikilinks to recipe ingredients sections"
    )
    parser.add_argument(
        '--vault',
        default='.',
        help='Path to Obsidian vault (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without modifying files'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("🔗 WIKILINKS ADDER FOR RECIPES")
    print("="*70)
    
    adder = WikilinkAdder(args.vault, args.dry_run)
    adder.process_all_recipes()


if __name__ == '__main__':
    main()
