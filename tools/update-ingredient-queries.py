#!/usr/bin/env python3
"""
Script to update Dataview queries in ingredient files.

Replaces:
  WHERE contains(ingredients, "ingredient-name")

With:
  WHERE contains(file.outlinks, this.file.link)
"""

import os
import re
from pathlib import Path


def update_ingredient_file(filepath: Path) -> bool:
    """
    Update a single ingredient file.
    Returns True if file was modified.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match the old query
        # WHERE contains(ingredients, "anything")
        # Use [^"]+ to allow apostrophes and other characters inside quotes
        old_pattern = r'WHERE contains\(ingredients,\s*"([^"]+)"\)'
        new_replacement = r'WHERE contains(file.outlinks, this.file.link)'
        
        # Replace the pattern
        content = re.sub(old_pattern, new_replacement, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ Error processing {filepath.name}: {e}")
        return False


def main():
    """Main entry point."""
    vault_path = Path('.')
    ingredients_dir = vault_path / "contenus" / "recettes" / "Ingredients"
    
    if not ingredients_dir.exists():
        print(f"❌ Ingredients directory not found: {ingredients_dir}")
        return
    
    print("="*70)
    print("🔄 UPDATING INGREDIENT DATAVIEW QUERIES")
    print("="*70)
    print(f"\n🔍 Scanning ingredients in: {ingredients_dir}\n")
    
    ingredient_files = sorted(ingredients_dir.glob("*.md"))
    total_files = len(ingredient_files)
    modified_count = 0
    
    for filepath in ingredient_files:
        print(f"Processing: {filepath.name}")
        was_modified = update_ingredient_file(filepath)
        if was_modified:
            modified_count += 1
            print(f"  ✅ Updated")
        else:
            print(f"  ⏭️  No changes needed")
    
    print("\n" + "="*70)
    print("\n📊 SUMMARY")
    print("="*70)
    print(f"Total ingredient files: {total_files}")
    print(f"Files modified: {modified_count}")
    print(f"Files unchanged: {total_files - modified_count}")


if __name__ == '__main__':
    main()
