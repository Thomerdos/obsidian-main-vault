#!/usr/bin/env python3
"""
Build and maintain relationships in the Obsidian vault.
Reads .base schema files and creates bidirectional links in frontmatter.
"""

import os
import sys
import yaml
import frontmatter
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import shutil
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RelationBuilder:
    """Manages building and maintaining relationships in the vault."""
    
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
                    logger.info(f"Loaded schema: {entity_type} from {schema_file.relative_to(self.vault_dir)}")
            except Exception as e:
                logger.error(f"Error loading schema {schema_file}: {e}")
                return False
        
        logger.info(f"Loaded {len(self.schemas)} schemas")
        return True
    
    def scan_notes(self):
        """Scan all markdown notes in the vault."""
        for md_file in self.vault_dir.rglob("*.md"):
            # Skip templates and hidden files
            if any(part.startswith('.') or part.startswith('_') for part in md_file.parts):
                continue
            if 'Templates' in md_file.parts or 'template' in md_file.name.lower():
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    note = frontmatter.load(f)
                    if note.get('type') in self.schemas:
                        rel_path = md_file.relative_to(self.vault_dir)
                        self.notes[str(rel_path)] = {
                            'path': md_file,
                            'frontmatter': note,
                            'type': note.get('type')
                        }
                        self.stats[f'notes_{note.get("type")}'] += 1
            except Exception as e:
                logger.warning(f"Error reading {md_file}: {e}")
        
        logger.info(f"Scanned {len(self.notes)} notes")
        return True
    
    def extract_link_name(self, link_text):
        """Extract the display name from a wiki link."""
        # Handle [[Link]] or [[Link|Display]]
        if not link_text:
            return None
        link_text = str(link_text).strip()
        if '|' in link_text:
            return link_text.split('|')[0].strip()
        return link_text
    
    def find_note_by_name(self, name, target_dir=None):
        """Find a note by its base name."""
        if not name:
            return None
        name = self.extract_link_name(name)
        
        for note_path, note_data in self.notes.items():
            note_name = Path(note_data['path']).stem
            if note_name == name:
                if target_dir:
                    if target_dir.rstrip('/') in note_path:
                        return note_path
                else:
                    return note_path
        return None
    
    def build_relations(self):
        """Build relationships based on schemas."""
        logger.info("Building relationships...")
        
        for note_path, note_data in self.notes.items():
            entity_type = note_data['type']
            schema = self.schemas.get(entity_type)
            if not schema:
                continue
            
            relations = schema.get('relations', {})
            fm = note_data['frontmatter']
            modified = False
            
            # Process each relation type
            for rel_name, rel_config in relations.items():
                if not rel_config.get('bidirectional'):
                    continue
                
                # Get source field value
                source_field = self.get_source_field_for_relation(rel_name, entity_type)
                if not source_field:
                    continue
                
                source_values = fm.get(source_field, [])
                if not isinstance(source_values, list):
                    source_values = [source_values] if source_values else []
                
                # For each linked entity, add inverse relation
                for link in source_values:
                    if not link:
                        continue
                    
                    linked_note_path = self.find_note_by_name(link, rel_config.get('target'))
                    if not linked_note_path:
                        continue
                    
                    # Add inverse relation
                    inverse_rel = rel_config.get('inverse')
                    if inverse_rel:
                        self.add_inverse_relation(
                            linked_note_path,
                            inverse_rel,
                            Path(note_data['path']).stem,
                            rel_config.get('type') == 'list'
                        )
                        modified = True
                        self.stats['relations_added'] += 1
        
        logger.info(f"Built {self.stats['relations_added']} relationships")
        return True
    
    def get_source_field_for_relation(self, rel_name, entity_type):
        """Get the frontmatter field name for a relation."""
        # Map relation name to frontmatter field
        # e.g., concert-groupes -> groupes
        parts = rel_name.split('-', 1)
        if len(parts) == 2 and parts[0] == entity_type:
            return parts[1]
        return None
    
    def add_inverse_relation(self, note_path, relation_field, target_name, is_list):
        """Add an inverse relation to a note."""
        if note_path not in self.notes:
            return
        
        note_data = self.notes[note_path]
        fm = note_data['frontmatter']
        
        # Get or create relation field
        current_values = fm.get(relation_field, [])
        if not isinstance(current_values, list):
            current_values = [current_values] if current_values else []
        
        # Add target if not already present
        if target_name not in current_values:
            if is_list:
                current_values.append(target_name)
                fm[relation_field] = current_values
            else:
                fm[relation_field] = target_name
            
            # Mark as modified
            note_data['modified'] = True
    
    def save_notes(self):
        """Save all modified notes."""
        if self.dry_run:
            logger.info("[DRY RUN] Would save modified notes")
            return True
        
        saved_count = 0
        for note_path, note_data in self.notes.items():
            if note_data.get('modified'):
                try:
                    with open(note_data['path'], 'w', encoding='utf-8') as f:
                        f.write(frontmatter.dumps(note_data['frontmatter']))
                    saved_count += 1
                except Exception as e:
                    logger.error(f"Error saving {note_path}: {e}")
        
        logger.info(f"Saved {saved_count} modified notes")
        return True
    
    def generate_report(self):
        """Generate a JSON report of the operation."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'dry_run': self.dry_run,
            'statistics': dict(self.stats),
            'schemas_loaded': list(self.schemas.keys()),
            'notes_processed': len(self.notes)
        }
        
        report_file = self.vault_dir / 'logs' / f'relations-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to {report_file}")
        return report
    
    def run(self):
        """Execute the full relation building process."""
        logger.info("="*70)
        logger.info("Building Relations in Obsidian Vault")
        logger.info("="*70)
        
        if not self.load_schemas():
            return False
        
        if not self.scan_notes():
            return False
        
        if not self.build_relations():
            return False
        
        if not self.save_notes():
            return False
        
        report = self.generate_report()
        
        logger.info("="*70)
        logger.info("Relation Building Complete")
        logger.info(f"Notes processed: {len(self.notes)}")
        logger.info(f"Relations added: {self.stats['relations_added']}")
        logger.info("="*70)
        
        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Build and maintain relationships in Obsidian vault'
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
    
    builder = RelationBuilder(args.vault, dry_run=args.dry_run)
    
    try:
        success = builder.run()
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
