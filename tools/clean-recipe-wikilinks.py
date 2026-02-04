#!/usr/bin/env python3
"""
Script to remove wikilinks from recipe ingredient sections.
This script removes all [[wikilinks]] from the text of the ## Ingrédients section,
restoring the original plain text format.
"""

import os
import sys
import re
from pathlib import Path
import yaml

def read_recipe_file(filepath: Path):
    """Read a recipe file and return (frontmatter, content)."""
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


def write_recipe_file(filepath: Path, frontmatter: dict, content: str):
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


def clean_wikilinks_from_ingredients(content: str) -> tuple[str, int]:
    """
    Remove all wikilinks from the ## Ingrédients section.
    Returns (cleaned_content, count_of_links_removed).
    """
    lines = content.split('\n')
    cleaned_lines = []
    in_ingredients_section = False
    links_removed = 0
    
    for line in lines:
        # Check if we're entering or leaving the ingredients section
        if line.strip().startswith('## Ingrédients') or line.strip().startswith('## Ingredients'):
            in_ingredients_section = True
            cleaned_lines.append(line)
            continue
        elif line.strip().startswith('##') and in_ingredients_section:
            in_ingredients_section = False
        
        if in_ingredients_section and line.strip():
            # Count wikilinks before removing
            before_count = line.count('[[')
            
            # Remove all wikilinks: [[text]] -> text
            # Handle malformed links like [[[[text]]]] too
            cleaned_line = line
            while '[[' in cleaned_line:
                # Remove one layer of brackets at a time
                cleaned_line = re.sub(r'\[\[([^\[\]]*)\]\]', r'\1', cleaned_line)
                after_count = cleaned_line.count('[[')
                # If count didn't decrease, we have a problem - break to avoid infinite loop
                if before_count == after_count:
                    break
                before_count = after_count
            
            links_removed += line.count('[[')
            cleaned_lines.append(cleaned_line)
        else:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines), links_removed


def clean_recipes(vault_path: Path, dry_run: bool = False):
    """Clean all recipe files by removing wikilinks from ingredients sections."""
    recipes_dir = vault_path / 'contenus' / 'recettes' / 'Fiches'
    
    if not recipes_dir.exists():
        print(f"❌ Recipe directory not found: {recipes_dir}")
        return
    
    recipe_files = list(recipes_dir.glob('*.md'))
    print(f"🔍 Found {len(recipe_files)} recipe files")
    
    if dry_run:
        print("⚠️  DRY RUN MODE - No files will be modified\n")
    
    stats = {
        'total': len(recipe_files),
        'modified': 0,
        'total_links_removed': 0,
    }
    
    for i, recipe_file in enumerate(recipe_files, 1):
        try:
            frontmatter, content = read_recipe_file(recipe_file)
            
            # Clean wikilinks from ingredients section
            cleaned_content, links_removed = clean_wikilinks_from_ingredients(content)
            
            if links_removed > 0:
                stats['modified'] += 1
                stats['total_links_removed'] += links_removed
                
                print(f"[{i}/{len(recipe_files)}] {recipe_file.name}")
                print(f"  ✓ Removed {links_removed} wikilink(s)")
                
                if not dry_run:
                    write_recipe_file(recipe_file, frontmatter, cleaned_content)
            
        except Exception as e:
            print(f"[{i}/{len(recipe_files)}] ❌ Error processing {recipe_file.name}: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 CLEANUP SUMMARY")
    print("="*60)
    print(f"Total recipes: {stats['total']}")
    print(f"Modified: {stats['modified']}")
    print(f"Total wikilinks removed: {stats['total_links_removed']}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Remove wikilinks from recipe ingredient sections'
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
    
    vault_path = Path(args.vault).resolve()
    
    print("🧹 Recipe Wikilinks Cleanup Script")
    print("="*60)
    print(f"Vault: {vault_path}")
    print(f"Dry run: {'Yes' if args.dry_run else 'No'}")
    print("="*60 + "\n")
    
    clean_recipes(vault_path, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
