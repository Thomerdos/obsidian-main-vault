#!/usr/bin/env python3
"""
Interactive CLI tool to add new concerts to the Obsidian vault.
Provides validation, location inference, and automatic entity creation.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import re

# Location mappings
VILLE_TO_PAYS = {
    "Lyon": "France",
    "Paris": "France",
    "Grenoble": "France",
    "Carhaix": "France",
    "Clisson": "France",
    "St-Julien-en-Genevois": "France",
    "Plozévet": "France",
    "Vienne": "France",
    "Tilburg": "Pays-Bas",
    "Crispendorf": "Allemagne",
    "Milan": "Italie",
    "Barcelone": "Espagne",
    "Veruno": "Italie",
    "Cartagena": "Espagne",
}

SALLE_TO_VILLE = {
    "Brin de Zinc": "Lyon",
    "Le Sucre": "Lyon",
    "Bourse du Travail": "Lyon",
    "LDLC Arena": "Lyon",
    "Halle Tony Garnier": "Lyon",
    "Ninkasi Gerland": "Lyon",
    "L'Épicerie Moderne": "Lyon",
    "L'Olympia": "Paris",
    "Zénith de Paris": "Paris",
    "Paris La Défense Arena": "Paris",
    "Le Trabendo": "Paris",
    "Poppodium 013": "Tilburg",
    "Le Ciel": "Grenoble",
    "La Belle Électrique": "Grenoble",
    "Michel Musique": "Grenoble",
    "Radiant-Bellevue": "Grenoble",
}

FESTIVAL_TO_VILLE = {
    "Motocultor Festival": "Carhaix",
    "Jazz à Vienne": "Vienne",
    "Hellfest": "Clisson",
    "Courts of Chaos Festival": "Plozévet",
    "Nuits de Fourvière": "Lyon",
    "Nuits sonores": "Lyon",
    "Roadburn Festival": "Tilburg",
    "Chaos Descends Festival": "Crispendorf",
    "Rock Imperium Festival": "Cartagena",
    "Guitare en Scène": "St-Julien-en-Genevois",
    "Be Prog! My Friend": "Barcelone",
    "2Days Prog + 1": "Veruno",
}

TEMPLATE_CONCERT = """---
type: concert
date: {date}
groupes: [{groupes}]
salle: {salle}
festival: {festival}
ville: {ville}
pays: {pays}
rating:
tags:
  - concert
---

# 🎸 Concert

## 📅 Informations

- **Date** : {date}
- **Groupes** : {groupes_display}
- **Lieu** : {lieu_display}
- **Type** : {type_event}

## 🎵 Setlist

- 

## 💭 Notes & Impressions



## 📷 Photos & Souvenirs



## 🔗 Liens

- [[Concerts|Retour à l'index des concerts]]
"""


def get_input(prompt, default="", required=True):
    """Get user input with optional default value."""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        value = input(prompt).strip()
        if not value and default:
            return default
        if not value and required:
            print("  ⚠️  This field is required. Please enter a value.")
            continue
        return value


def get_list_input(prompt):
    """Get comma-separated list input."""
    value = input(f"{prompt} (comma-separated): ").strip()
    if not value:
        return []
    return [item.strip() for item in value.split(',')]


def infer_location(salle="", festival=""):
    """Infer ville and pays from salle or festival."""
    ville = ""
    pays = ""
    
    if festival and festival in FESTIVAL_TO_VILLE:
        ville = FESTIVAL_TO_VILLE[festival]
        pays = VILLE_TO_PAYS.get(ville, "")
    elif salle and salle in SALLE_TO_VILLE:
        ville = SALLE_TO_VILLE[salle]
        pays = VILLE_TO_PAYS.get(ville, "")
    
    return ville, pays


def create_concert_file(date, groupes, salle, festival, ville, pays, vault_dir):
    """Create a concert markdown file."""
    year = date.split('-')[0]
    
    # Generate title
    if festival:
        title = festival
    elif groupes:
        title = ", ".join(groupes[:3])
        if len(groupes) > 3:
            title += f" (+{len(groupes)-3} autres)"
    else:
        title = "Concert"
    
    # Create filename
    filename = f"{date} - {title}.md"
    filename = filename.replace('/', '-').replace(':', '').replace('?', '')
    
    # Create directory
    concert_dir = vault_dir / "Musique" / "Concerts" / year
    concert_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = concert_dir / filename
    
    # Check if exists
    if file_path.exists():
        print(f"\n  ⚠️  File already exists: {file_path}")
        overwrite = input("  Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            return None
    
    # Format data
    groupes_yaml = '", "'.join(groupes)
    if groupes_yaml:
        groupes_yaml = f'"{groupes_yaml}"'
    
    groupes_display = ", ".join([f"[[{g}]]" for g in groupes])
    
    if festival:
        lieu_display = f"[[{festival}]]"
        if ville:
            lieu_display += f" - [[{ville}]]"
        type_event = "Festival"
    elif salle:
        lieu_display = f"[[{salle}]]"
        if ville:
            lieu_display += f" - [[{ville}]]"
        type_event = "Concert"
    else:
        lieu_display = f"[[{ville}]]" if ville else ""
        type_event = "Concert"
    
    # Create content
    content = TEMPLATE_CONCERT.format(
        date=date,
        groupes=groupes_yaml,
        salle=salle,
        festival=festival,
        ville=ville,
        pays=pays,
        groupes_display=groupes_display,
        lieu_display=lieu_display,
        type_event=type_event
    )
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return file_path


def main():
    """Main interactive function."""
    print("\n" + "="*70)
    print("🎸 Add New Concert to Obsidian Vault")
    print("="*70 + "\n")
    
    # Determine vault directory
    vault_dir = Path(__file__).parent.parent
    print(f"Vault directory: {vault_dir}\n")
    
    # Get concert details
    print("📅 Concert Details\n")
    
    # Date
    while True:
        date = get_input("Date (YYYY-MM-DD)")
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            break
        print("  ⚠️  Invalid date format. Use YYYY-MM-DD")
    
    # Artists
    groupes = get_list_input("Artists/Bands")
    
    # Venue
    salle = get_input("Venue", required=False)
    if salle:
        print(f"  Known venues: {', '.join(list(SALLE_TO_VILLE.keys())[:5])}...")
    
    # Festival
    festival = get_input("Festival", required=False)
    if festival:
        print(f"  Known festivals: {', '.join(list(FESTIVAL_TO_VILLE.keys())[:5])}...")
    
    # Infer location
    ville_inferred, pays_inferred = infer_location(salle, festival)
    
    # City
    if ville_inferred:
        print(f"  💡 Inferred city: {ville_inferred}")
        ville = get_input("City", default=ville_inferred)
    else:
        ville = get_input("City")
    
    # Country
    if pays_inferred:
        print(f"  💡 Inferred country: {pays_inferred}")
        pays = get_input("Country", default=pays_inferred)
    else:
        pays = get_input("Country")
    
    # Summary
    print("\n" + "="*70)
    print("📋 Summary")
    print("="*70)
    print(f"Date:     {date}")
    print(f"Artists:  {', '.join(groupes) if groupes else '(none)'}")
    print(f"Venue:    {salle if salle else '(none)'}")
    print(f"Festival: {festival if festival else '(none)'}")
    print(f"City:     {ville}")
    print(f"Country:  {pays}")
    print("="*70 + "\n")
    
    # Confirm
    confirm = input("Create concert file? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Cancelled.")
        return
    
    # Create file
    file_path = create_concert_file(date, groupes, salle, festival, ville, pays, vault_dir)
    
    if file_path:
        print(f"\n✅ Concert file created: {file_path}")
        print("\n📝 Next steps:")
        print("  1. Review the file in Obsidian")
        print("  2. Add setlist, notes, and photos")
        print("  3. Add a line to Musique/Concerts.md")
        print("  4. Create missing entity pages if needed\n")
    else:
        print("\n❌ Concert file not created.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
