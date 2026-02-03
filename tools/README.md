# 🛠️ Obsidian Concert Vault Tools

Python scripts and utilities for managing the concert vault.

## Available Tools

### 🎸 add-concert.py

Interactive CLI tool to add new concerts to the vault.

**Usage:**
```bash
python3 tools/add-concert.py
```

**Features:**
- Interactive prompts for concert details
- Automatic location inference from venue/festival
- Date validation
- File existence checking
- Automatic YAML frontmatter generation
- Creates properly formatted concert files

**Example Session:**
```
Date (YYYY-MM-DD): 2026-03-15
Artists/Bands (comma-separated): Tool, King Crimson
Venue: L'Olympia
  💡 Inferred city: Paris
City [Paris]: 
  💡 Inferred country: France
Country [France]: 

✅ Concert file created: Musique/Concerts/2026/2026-03-15 - Tool, King Crimson.md
```

## Location Mappings

The tools include built-in location mappings for automatic inference:

### Known Venues (Salles)
- Brin de Zinc, Le Sucre, LDLC Arena → Lyon
- L'Olympia, Zénith de Paris → Paris
- Poppodium 013 → Tilburg
- Le Ciel, La Belle Électrique → Grenoble

### Known Festivals
- Hellfest → Clisson
- Jazz à Vienne → Vienne
- Roadburn Festival → Tilburg
- Motocultor Festival → Carhaix

### Cities to Countries
- Lyon, Paris, Vienne → France
- Tilburg → Pays-Bas
- Milan → Italie
- Barcelone → Espagne

## Adding New Mappings

To add new venues, festivals, or cities:

1. Edit `add-concert.py`
2. Add entries to the relevant dictionary:
   - `SALLE_TO_VILLE` for venues
   - `FESTIVAL_TO_VILLE` for festivals
   - `VILLE_TO_PAYS` for cities

Example:
```python
SALLE_TO_VILLE = {
    "New Venue Name": "City Name",
    # ... existing entries
}
```

## Requirements

- Python 3.6+
- No external dependencies (uses stdlib only)

## Future Tools

Planned utilities:
- `validate-vault.py` - Check data consistency across all files
- `generate-stats.py` - Regenerate statistics in Concerts.md
- `find-missing-entities.py` - List artists/venues without pages
- `backup-vault.py` - Create vault backup
- `import-setlist.py` - Import setlists from setlist.fm API

## Integration with GitHub Actions

These tools can be used both locally and in GitHub Actions workflows. See `.github/workflows/` for automated versions.
