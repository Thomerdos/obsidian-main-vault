#!/usr/bin/env python3
"""
Validate that all notes conform to their .base schemas.
Check required fields, data types, and relation integrity.
"""

import os
import sys
import yaml
import frontmatter
import json
from pathlib import Path
from collections import defaultdict
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SchemaValidator:
    """Validates notes against schema definitions."""
    
    def __init__(self, vault_dir):
        self.vault_dir = Path(vault_dir)
        self.schemas = {}
        self.errors = defaultdict(list)
        self.warnings = defaultdict(list)
        self.stats = defaultdict(int)
        
    def load_schemas(self):
        """Load all .base schema files."""
        bases_dir = self.vault_dir / ".bases"
        if not bases_dir.exists():
            logger.error(f"Schemas directory not found: {bases_dir}")
            return False
            
        for schema_file in bases_dir.glob("*.base"):
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema = yaml.safe_load(f)
                    entity_type = schema['type']
                    self.schemas[entity_type] = schema
            except Exception as e:
                logger.error(f"Error loading schema {schema_file}: {e}")
                return False
        
        logger.info(f"Loaded {len(self.schemas)} schemas")
        return True
    
    def validate_note(self, note_path):
        """Validate a single note against its schema."""
        try:
            with open(note_path, 'r', encoding='utf-8') as f:
                note = frontmatter.load(f)
        except Exception as e:
            self.errors[str(note_path)].append(f"Cannot read file: {e}")
            return False
        
        entity_type = note.get('type')
        if not entity_type:
            self.warnings[str(note_path)].append("No 'type' field in frontmatter")
            return True
        
        if entity_type not in self.schemas:
            self.warnings[str(note_path)].append(f"Unknown type: {entity_type}")
            return True
        
        schema = self.schemas[entity_type]
        self.stats[f'validated_{entity_type}'] += 1
        
        # Check required fields
        required_fields = schema.get('required', [])
        for field_def in required_fields:
            if isinstance(field_def, dict):
                field_name = list(field_def.keys())[0]
            else:
                field_name = field_def
            
            if field_name not in note or not note[field_name]:
                self.errors[str(note_path)].append(f"Missing required field: {field_name}")
        
        # Check relations exist
        relations = schema.get('relations', {})
        for rel_name, rel_config in relations.items():
            # Extract field name from relation name
            field_name = rel_name.split('-', 1)[-1] if '-' in rel_name else rel_name
            
            if field_name in note:
                values = note[field_name]
                if not isinstance(values, list):
                    values = [values] if values else []
                
                # Check that linked notes exist
                for link in values:
                    if link and not self.check_link_exists(link, rel_config.get('target')):
                        self.warnings[str(note_path)].append(
                            f"Broken link in {field_name}: {link}"
                        )
        
        return len(self.errors[str(note_path)]) == 0
    
    def check_link_exists(self, link_name, target_dir):
        """Check if a linked note exists."""
        if not link_name:
            return True
        
        # Extract link name
        link_name = str(link_name).strip()
        if '|' in link_name:
            link_name = link_name.split('|')[0].strip()
        if link_name.startswith('[['):
            link_name = link_name[2:]
        if link_name.endswith(']]'):
            link_name = link_name[:-2]
        
        # Search for the file
        search_dirs = [self.vault_dir]
        if target_dir:
            search_dirs = [self.vault_dir / target_dir]
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for md_file in search_dir.rglob(f"{link_name}.md"):
                    return True
        
        return False
    
    def validate_all(self):
        """Validate all notes in the vault."""
        logger.info("Validating all notes...")
        
        valid_count = 0
        for md_file in self.vault_dir.rglob("*.md"):
            # Skip templates and hidden files
            if any(part.startswith('.') or part.startswith('_') for part in md_file.parts):
                continue
            if 'Templates' in md_file.parts or 'template' in md_file.name.lower():
                continue
            
            if self.validate_note(md_file):
                valid_count += 1
        
        logger.info(f"Validated {valid_count} notes successfully")
        return True
    
    def generate_report(self):
        """Generate validation report."""
        report = {
            'total_notes': sum(1 for _ in self.vault_dir.rglob("*.md")),
            'validated': dict(self.stats),
            'errors': len(self.errors),
            'warnings': len(self.warnings),
            'error_details': dict(self.errors),
            'warning_details': dict(self.warnings)
        }
        
        # Print summary
        logger.info("="*70)
        logger.info("Validation Report")
        logger.info("="*70)
        logger.info(f"Notes validated: {sum(self.stats.values())}")
        logger.info(f"Errors: {len(self.errors)}")
        logger.info(f"Warnings: {len(self.warnings)}")
        
        if self.errors:
            logger.error("\nErrors found:")
            for note_path, errors in list(self.errors.items())[:10]:
                logger.error(f"  {note_path}:")
                for error in errors:
                    logger.error(f"    - {error}")
            if len(self.errors) > 10:
                logger.error(f"  ... and {len(self.errors) - 10} more files with errors")
        
        if self.warnings:
            logger.warning("\nWarnings:")
            for note_path, warnings in list(self.warnings.items())[:10]:
                logger.warning(f"  {note_path}:")
                for warning in warnings:
                    logger.warning(f"    - {warning}")
            if len(self.warnings) > 10:
                logger.warning(f"  ... and {len(self.warnings) - 10} more files with warnings")
        
        logger.info("="*70)
        
        # Save report
        report_dir = self.vault_dir / 'logs'
        report_dir.mkdir(exist_ok=True)
        report_file = report_dir / 'validation-report.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Full report saved to: {report_file}")
        
        return report
    
    def run(self):
        """Execute validation."""
        logger.info("="*70)
        logger.info("Schema Validation")
        logger.info("="*70)
        
        if not self.load_schemas():
            return False
        
        if not self.validate_all():
            return False
        
        self.generate_report()
        
        return len(self.errors) == 0


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate Obsidian vault against schemas'
    )
    parser.add_argument(
        '--vault',
        default='.',
        help='Path to vault directory (default: current directory)'
    )
    
    args = parser.parse_args()
    
    validator = SchemaValidator(args.vault)
    
    try:
        success = validator.run()
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
