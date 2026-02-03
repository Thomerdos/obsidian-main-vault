#!/usr/bin/env python3
"""
Generate statistics about vault relationships and structure.
"""

import os
import sys
import yaml
import frontmatter
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StatsGenerator:
    """Generate vault statistics."""
    
    def __init__(self, vault_dir):
        self.vault_dir = Path(vault_dir)
        self.schemas = {}
        self.notes = {}
        self.stats = {
            'entity_counts': defaultdict(int),
            'relation_counts': defaultdict(int),
            'most_connected': defaultdict(list),
            'density': {}
        }
        
    def load_schemas(self):
        """Load all .base schema files recursively from bases/ directory."""
        bases_dir = self.vault_dir / "bases"
        if not bases_dir.exists():
            # Fallback to old .bases directory for compatibility
            bases_dir = self.vault_dir / ".bases"
            if not bases_dir.exists():
                logger.warning(f"Schemas directory not found: {bases_dir}")
                return True
            
        # Load schemas recursively
        for schema_file in bases_dir.rglob("*.base"):
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema = yaml.safe_load(f)
                    entity_type = schema['type']
                    self.schemas[entity_type] = schema
            except Exception as e:
                logger.error(f"Error loading schema {schema_file}: {e}")
        
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
                    if entity_type:
                        rel_path = md_file.relative_to(self.vault_dir)
                        self.notes[str(rel_path)] = {
                            'path': md_file,
                            'frontmatter': note,
                            'type': entity_type,
                            'name': md_file.stem
                        }
                        self.stats['entity_counts'][entity_type] += 1
            except Exception as e:
                logger.warning(f"Error reading {md_file}: {e}")
        
        logger.info(f"Scanned {len(self.notes)} notes")
        return True
    
    def calculate_stats(self):
        """Calculate relationship statistics."""
        logger.info("Calculating statistics...")
        
        connection_counts = defaultdict(int)
        
        for note_path, note_data in self.notes.items():
            entity_type = note_data['type']
            fm = note_data['frontmatter']
            
            # Count connections
            total_connections = 0
            for key, value in fm.metadata.items():
                if isinstance(value, list) and value:
                    total_connections += len(value)
                    self.stats['relation_counts'][f'{entity_type}_{key}'] += len(value)
                elif value and key not in ['type', 'tags', 'date', 'formation', 'continent', 
                                            'capacite', 'rating', 'adresse', 'region', 
                                            'periode', 'site-web', 'description']:
                    total_connections += 1
                    self.stats['relation_counts'][f'{entity_type}_{key}'] += 1
            
            connection_counts[note_data['name']] = total_connections
        
        # Find most connected nodes by type
        for entity_type in self.stats['entity_counts'].keys():
            type_notes = [(name, count) for name, count in connection_counts.items()
                          if any(n['name'] == name and n['type'] == entity_type 
                                for n in self.notes.values())]
            type_notes.sort(key=lambda x: x[1], reverse=True)
            self.stats['most_connected'][entity_type] = type_notes[:10]
        
        # Calculate density
        for entity_type, count in self.stats['entity_counts'].items():
            if count > 0:
                avg_connections = sum(connection_counts[n['name']] 
                                     for n in self.notes.values() 
                                     if n['type'] == entity_type) / count
                self.stats['density'][entity_type] = round(avg_connections, 2)
        
        return True
    
    def generate_report(self):
        """Generate and save report."""
        report = {
            'generated': datetime.now().isoformat(),
            'entity_counts': dict(self.stats['entity_counts']),
            'relation_counts': dict(self.stats['relation_counts']),
            'most_connected': {k: v for k, v in self.stats['most_connected'].items()},
            'density': dict(self.stats['density'])
        }
        
        # Print summary
        logger.info("="*70)
        logger.info("Vault Statistics")
        logger.info("="*70)
        logger.info("\nEntity Counts:")
        for entity_type, count in sorted(self.stats['entity_counts'].items()):
            logger.info(f"  {entity_type}: {count}")
        
        logger.info("\nAverage Connections (Density):")
        for entity_type, density in sorted(self.stats['density'].items()):
            logger.info(f"  {entity_type}: {density} connections/node")
        
        logger.info("\nMost Connected Nodes:")
        for entity_type, nodes in self.stats['most_connected'].items():
            if nodes:
                logger.info(f"  {entity_type}:")
                for name, count in nodes[:3]:
                    logger.info(f"    {name}: {count} connections")
        
        logger.info("="*70)
        
        # Save JSON report
        report_dir = self.vault_dir / 'logs'
        report_dir.mkdir(exist_ok=True)
        report_file = report_dir / f'stats-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to: {report_file}")
        
        return report
    
    def run(self):
        """Execute statistics generation."""
        logger.info("="*70)
        logger.info("Generating Vault Statistics")
        logger.info("="*70)
        
        self.load_schemas()
        
        if not self.scan_notes():
            return False
        
        if not self.calculate_stats():
            return False
        
        self.generate_report()
        
        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate vault statistics'
    )
    parser.add_argument(
        '--vault',
        default='.',
        help='Path to vault directory (default: current directory)'
    )
    
    args = parser.parse_args()
    
    generator = StatsGenerator(args.vault)
    
    try:
        success = generator.run()
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
