#!/usr/bin/env python3
"""
Migrate existing vault notes to the new relational system.
Adds relation fields to frontmatter while preserving existing data.
"""

import os
import sys
import yaml
import frontmatter
import json
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VaultMigrator:
    """Manages migration of vault notes to relational system."""
    
    def __init__(self, vault_dir, dry_run=False, backup=True):
        self.vault_dir = Path(vault_dir)
        self.dry_run = dry_run
        self.backup = backup
        self.schemas = {}
        self.notes = {}
        self.stats = defaultdict(int)
        
    def create_backup(self):
        """Create a backup of the vault."""
        if self.dry_run or not self.backup:
            logger.info("[SKIP] Backup disabled")
            return True
        
        backup_dir = self.vault_dir / ".backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"pre-migration-{timestamp}"
        backup_path = backup_dir / backup_name
        
        logger.info(f"Creating backup: {backup_path}")
        
        # Backup key directories
        for dir_name in ['Musique', 'Lieux']:
            src = self.vault_dir / dir_name
            if src.exists():
                dst = backup_path / dir_name
                shutil.copytree(src, dst)
        
        logger.info(f"Backup created: {backup_path}")
        return True
    
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
        
        return True
    
    def scan_notes(self):
        """Scan all notes in the vault."""
        for md_file in self.vault_dir.rglob("*.md"):
            # Skip templates and hidden files
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
                        self.stats[f'scanned_{entity_type}'] += 1
            except Exception as e:
                logger.warning(f"Error reading {md_file}: {e}")
        
        logger.info(f"Scanned {len(self.notes)} notes")
        return True
    
    def migrate_note(self, note_path, note_data):
        """Migrate a single note to add relation fields."""
        fm = note_data['frontmatter']
        entity_type = note_data['type']
        schema = self.schemas[entity_type]
        modified = False
        
        # Get relations for this entity type
        relations = schema.get('relations', {})
        
        for rel_name, rel_config in relations.items():
            # Extract field name from relation name
            # e.g., concert-groupes -> groupes
            parts = rel_name.split('-', 1)
            if len(parts) == 2 and parts[0] == entity_type:
                field_name = parts[1]
            else:
                continue
            
            # Initialize relation field if it doesn't exist
            if field_name not in fm or fm[field_name] is None:
                if rel_config.get('type') == 'list':
                    fm[field_name] = []
                else:
                    fm[field_name] = ""
                modified = True
                self.stats[f'field_added_{field_name}'] += 1
        
        if modified:
            note_data['modified'] = True
            self.stats['notes_modified'] += 1
        
        return modified
    
    def migrate_all(self):
        """Migrate all notes."""
        logger.info("Migrating notes...")
        
        for note_path, note_data in self.notes.items():
            self.migrate_note(note_path, note_data)
        
        logger.info(f"Modified {self.stats['notes_modified']} notes")
        return True
    
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
        """Generate migration report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'dry_run': self.dry_run,
            'backup_created': self.backup,
            'statistics': dict(self.stats),
            'notes_processed': len(self.notes)
        }
        
        report_dir = self.vault_dir / 'logs'
        report_dir.mkdir(exist_ok=True)
        report_file = report_dir / f'migration-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to {report_file}")
        return report
    
    def run(self):
        """Execute migration."""
        logger.info("="*70)
        logger.info("Vault Migration to Relational System")
        logger.info("="*70)
        
        if not self.load_schemas():
            return False
        
        # Ask for confirmation in interactive mode
        if not self.dry_run:
            logger.warning("This will modify your vault files.")
            logger.warning("A backup will be created first.")
            response = input("\nContinue? (yes/no): ").lower()
            if response not in ['yes', 'y']:
                logger.info("Migration cancelled")
                return False
        
        if not self.create_backup():
            return False
        
        if not self.scan_notes():
            return False
        
        if not self.migrate_all():
            return False
        
        if not self.save_notes():
            return False
        
        report = self.generate_report()
        
        logger.info("="*70)
        logger.info("Migration Complete")
        logger.info(f"Notes processed: {len(self.notes)}")
        logger.info(f"Notes modified: {self.stats['notes_modified']}")
        logger.info("="*70)
        
        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Migrate Obsidian vault to relational system'
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
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Skip backup creation (not recommended)'
    )
    
    args = parser.parse_args()
    
    migrator = VaultMigrator(
        args.vault,
        dry_run=args.dry_run,
        backup=not args.no_backup
    )
    
    try:
        success = migrator.run()
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
