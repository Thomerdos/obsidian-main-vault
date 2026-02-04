#!/usr/bin/env python3
"""
Script to update ingredient pages with the new Dataview query.
Changes the query from checking file.outlinks to checking ingredients frontmatter field.
"""

import os
import sys
import re
from pathlib import Path
import yaml


def read_file(filepath: Path):
    """Read a file and return (frontmatter, content)."""
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


def write_file(filepath: Path, frontmatter: dict, content: str):
    """Write file with frontmatter and content."""
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


def update_dataview_query(content: str) -> tuple[str, bool]:
    """
    Update the Dataview query from file.outlinks to ingredients field.
    Returns (updated_content, was_modified).
    """
    # Old pattern: WHERE contains(file.outlinks, this.file.link)
    # New pattern: WHERE contains(ingredients, this.file.link)
    
    old_pattern = r'WHERE\s+contains\s*\(\s*file\.outlinks\s*,\s*this\.file\.link\s*\)'
    new_pattern = 'WHERE contains(ingredients, this.file.link)'
    
    updated_content = re.sub(old_pattern, new_pattern, content, flags=re.IGNORECASE)
    
    was_modified = updated_content != content
    return updated_content, was_modified


def update_ingredient_pages(vault_path: Path, dry_run: bool = False):
    """Update all ingredient pages with the new Dataview query."""
    ingredients_dir = vault_path / 'contenus' / 'recettes' / 'Ingredients'
    
    if not ingredients_dir.exists():
        print(f"❌ Ingredients directory not found: {ingredients_dir}")
        return
    
    ingredient_files = list(ingredients_dir.glob('*.md'))
    print(f"🔍 Found {len(ingredient_files)} ingredient files")
    
    if dry_run:
        print("⚠️  DRY RUN MODE - No files will be modified\n")
    
    stats = {
        'total': len(ingredient_files),
        'modified': 0,
        'already_correct': 0,
    }
    
    for i, ingredient_file in enumerate(ingredient_files, 1):
        try:
            frontmatter, content = read_file(ingredient_file)
            
            # Update the Dataview query
            updated_content, was_modified = update_dataview_query(content)
            
            if was_modified:
                stats['modified'] += 1
                print(f"[{i}/{len(ingredient_files)}] ✓ {ingredient_file.name}")
                
                if not dry_run:
                    write_file(ingredient_file, frontmatter, updated_content)
            else:
                stats['already_correct'] += 1
                # Uncomment to see files that are already correct
                # print(f"[{i}/{len(ingredient_files)}] ○ {ingredient_file.name} (already correct)")
            
        except Exception as e:
            print(f"[{i}/{len(ingredient_files)}] ❌ Error processing {ingredient_file.name}: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 UPDATE SUMMARY")
    print("="*60)
    print(f"Total ingredient pages: {stats['total']}")
    print(f"Modified: {stats['modified']}")
    print(f"Already correct: {stats['already_correct']}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Update ingredient pages with new Dataview query'
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
    
    print("🔄 Ingredient Pages Update Script")
    print("="*60)
    print(f"Vault: {vault_path}")
    print(f"Dry run: {'Yes' if args.dry_run else 'No'}")
    print("="*60 + "\n")
    
    update_ingredient_pages(vault_path, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
