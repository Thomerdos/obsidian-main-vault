#!/usr/bin/env python3
"""
Synchronize bidirectional relationships in the vault.
Ensures all inverse relations are properly maintained.
"""

import os
import sys
import yaml
import frontmatter
from pathlib import Path
from collections import defaultdict
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GraphSynchronizer:
    """Synchronizes bidirectional links in the vault."""
    
    def __init__(self, vault_dir, dry_run=False):
        self.vault_dir = Path(vault_dir)
        self.dry_run = dry_run
        self.schemas = {}
        self.notes = {}
        self.stats = defaultdict(int)
        
    def load_schemas(self):
        """Load all .base schema files recursively from bases/ directory."""
        bases_dir = self.vault_dir / "bases"
        if not bases_dir.exists():
            # Fallback to old .bases directory for compatibility
            bases_dir = self.vault_dir / ".bases"
            if not bases_dir.exists():
                logger.error(f"Schemas directory not found: {bases_dir}")
                return False
            
        # Load schemas recursively
        for schema_file in bases_dir.rglob("*.base"):
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema = yaml.safe_load(f)
                    entity_type = schema['type']
                    self.schemas[entity_type] = schema
            except Exception as e:
                logger.error(f"Error loading schema {schema_file}: {e}")
                return False
        
        return True
    
    def scan_notes(self):
        """Scan all notes in the vault."""
        for md_file in self.vault_dir.rglob("*.md"):
            if any(part.startswith('.') or part.startswith('_') for part in md_file.parts):
                continue
            if 'Templates' in md_file.parts or 'template' in md_file.name.lower():
                continue
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    note = frontmatter.load(f)
                    entity_type = note.get('type')
                    if entity_type in self.schemas:
                        rel_path = md_file.relative_to(self.vault_dir)
                        self.notes[str(rel_path)] = {
                            'path': md_file,
                            'frontmatter': note,
                            'type': entity_type,
                            'name': md_file.stem
                        }
            except Exception as e:
                logger.warning(f"Error reading {md_file}: {e}")
        
        logger.info(f"Scanned {len(self.notes)} notes")
        return True
    
    def sync_relations(self):
        """Synchronize all bidirectional relations."""
        logger.info("Synchronizing relations...")
        
        for note_path, note_data in self.notes.items():
            entity_type = note_data['type']
            schema = self.schemas[entity_type]
            relations = schema.get('relations', {})
            
            for rel_name, rel_config in relations.items():
                if not rel_config.get('bidirectional'):
                    continue
                
                # Get field name
                field_name = rel_name.split('-', 1)[-1] if '-' in rel_name else rel_name
                field_value = note_data['frontmatter'].get(field_name)
                
                if not field_value:
                    continue
                
                # Ensure it's a list
                if not isinstance(field_value, list):
                    field_value = [field_value]
                
                # For each linked entity, ensure inverse relation exists
                for link in field_value:
                    if not link:
                        continue
                    
                    linked_note = self.find_note_by_name(link)
                    if linked_note:
                        self.ensure_inverse_relation(
                            linked_note,
                            rel_config.get('inverse'),
                            note_data['name'],
                            rel_config.get('type') == 'list'
                        )
        
        logger.info(f"Synchronized {self.stats['relations_synced']} relations")
        return True
    
    def find_note_by_name(self, name):
        """Find a note by its name."""
        if not name:
            return None
        
        name = str(name).strip()
        if '|' in name:
            name = name.split('|')[0].strip()
        
        for note_path, note_data in self.notes.items():
            if note_data['name'] == name:
                return note_data
        
        return None
    
    def ensure_inverse_relation(self, target_note, inverse_field, source_name, is_list):
        """Ensure inverse relation exists in target note."""
        if not inverse_field:
            return
        
        fm = target_note['frontmatter']
        current_value = fm.get(inverse_field)
        
        if is_list:
            if not isinstance(current_value, list):
                current_value = [current_value] if current_value else []
            
            if source_name not in current_value:
                current_value.append(source_name)
                fm[inverse_field] = current_value
                target_note['modified'] = True
                self.stats['relations_synced'] += 1
        else:
            if current_value != source_name:
                fm[inverse_field] = source_name
                target_note['modified'] = True
                self.stats['relations_synced'] += 1
    
    def save_notes(self):
        """Save all modified notes."""
        if self.dry_run:
            logger.info("[DRY RUN] Would save modified notes")
            return True
        
        saved_count = 0
        for note_data in self.notes.values():
            if note_data.get('modified'):
                try:
                    with open(note_data['path'], 'w', encoding='utf-8') as f:
                        f.write(frontmatter.dumps(note_data['frontmatter']))
                    saved_count += 1
                except Exception as e:
                    logger.error(f"Error saving {note_data['path']}: {e}")
        
        logger.info(f"Saved {saved_count} modified notes")
        return True
    
    def run(self):
        """Execute synchronization."""
        logger.info("="*70)
        logger.info("Synchronizing Graph Relations")
        logger.info("="*70)
        
        if not self.load_schemas():
            return False
        
        if not self.scan_notes():
            return False
        
        if not self.sync_relations():
            return False
        
        if not self.save_notes():
            return False
        
        logger.info("="*70)
        logger.info("Synchronization Complete")
        logger.info(f"Relations synced: {self.stats['relations_synced']}")
        logger.info("="*70)
        
        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Synchronize bidirectional relations in vault'
    )
    parser.add_argument(
        '--vault',
        default='.',
        help='Path to vault directory (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    
    args = parser.parse_args()
    
    syncer = GraphSynchronizer(args.vault, dry_run=args.dry_run)
    
    try:
        success = syncer.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
