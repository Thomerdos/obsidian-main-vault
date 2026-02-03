# 🎸 Obsidian Concert Vault

A structured Obsidian vault for tracking concert attendance with automatic relationship management via Dataview.

## 🚀 Quick Start

### View Concerts
- **Main Index**: [`Musique/Concerts.md`](Musique/Concerts.md) - All concerts with statistics
- **By Year**: `Musique/Concerts/YYYY/` - Individual concert files
- **By Artist**: `Musique/Groupes/` - Artist pages with concert history
- **By Venue**: `Musique/Salles/` - Venue pages with concerts held there

### Add a Concert

#### Manual Method
1. Copy template: `Musique/_templates/template-concert.md`
2. Create file: `Musique/Concerts/YYYY/YYYY-MM-DD - Event.md`
3. Fill frontmatter:
   ```yaml
   type: concert
   date: 2026-02-03
   groupes: ["Artist Name"]
   salle: Venue Name
   festival: 
   ville: City
   pays: Country
   ```
4. Add line to `Musique/Concerts.md`

#### Semi-Automated Method (GitHub Actions)
1. Create GitHub Issue with concert details
2. Use "Add Concert" workflow (coming soon)
3. Workflow creates files and updates index

## 📂 Structure

```
Musique/
├── Concerts.md              # Main index with statistics
├── _templates/              # 5 templates (concert, groupe, salle, festival, genre)
├── Concerts/YYYY/           # Concert files by year (56 total)
├── Groupes/                 # Artist pages (67 total)
├── Genres/                  # Musical genre pages (56 total)
├── Festivals/               # Festival pages (12 total)
└── Salles/                  # Venue pages (15 total)

Lieux/
├── _templates/              # Location templates
├── Villes/                  # City pages (14 total)
└── Pays/                    # Country pages (5 total)
```

## 🔗 Automatic Relationships

All pages include Dataview queries that auto-generate relationships:

- **Artist pages** → List all concerts where they played
- **Genre pages** → List all artists and concerts of that genre
- **Venue pages** → List all concerts at that venue
- **Festival pages** → List all editions attended
- **City pages** → List venues and concerts in that city
- **Country pages** → List cities and concerts in that country

## 📊 Statistics

Current vault contains:
- **56 concerts** (2013-2026)
- **67 artists/groups**
- **56 musical genres**
- **15 venues** across 5 countries
- **12 festivals**
- **14 cities** with concert activity

Top locations:
- 🇫🇷 France: 44 concerts
- 🏙️ Vienne: 13 concerts (Jazz à Vienne)
- 🏙️ Lyon: 11 concerts

## 🛠️ Automation

### GitHub Actions (Planned)

Workflows in `.github/workflows/`:
- **validate-yaml.yml** - Check frontmatter syntax on PRs
- **add-concert.yml** - Create concert files from GitHub Issues
- **check-links.yml** - Verify all wiki links resolve
- **update-stats.yml** - Auto-update statistics in Concerts.md

### Python Scripts (Planned)

Tools for vault management:
- `add-concert.py` - Interactive CLI to add concerts
- `validate-vault.py` - Check data consistency
- `generate-stats.py` - Regenerate statistics
- `find-missing-entities.py` - Find artists/venues without pages

## 📖 Documentation

- **[Structure Guide](Musique/README-STRUCTURE.md)** - Detailed usage and templates
- **[Location Verification](Musique/VERIFICATION-LOCALISATION.md)** - Location data audit
- **[Copilot Instructions](.github/copilot/instructions.md)** - For AI assistance

## 🔐 Data Quality

All concert files include:
- ✅ Complete frontmatter (type, date, location)
- ✅ Valid YAML syntax
- ✅ Location mappings (ville/pays)
- ✅ Artist lists
- ✅ Wiki-style links to entities

Last verified: 2026-02-03 (100% complete)

## 🤝 Contributing

### Adding Concerts

1. Use templates from `_templates/` directories
2. Follow naming convention: `YYYY-MM-DD - Event.md`
3. Ensure all frontmatter fields are filled
4. Create missing entity pages (artists, venues) if needed
5. Update main index `Concerts.md`

### Maintaining Consistency

- Use lowercase-with-hyphens for YAML keys: `pays-origine`
- Use JSON arrays in YAML: `groupes: ["Artist1", "Artist2"]`
- Use wiki links: `[[Page Name]]`
- Date format: `YYYY-MM-DD`
- Include emoji icons: 🎸 (concerts), 🎤 (groups), 🏛️ (venues)

## 📱 Obsidian Setup

### Required Plugins
- **Dataview** - For automatic relationship queries

### Recommended Plugins
- **Templater** - For quick template insertion
- **Calendar** - For date-based navigation
- **Excalidraw** - For concert memory drawings

### Theme Compatibility
Works with all Obsidian themes. Tested with:
- Default theme
- Minimal theme
- Things theme

## 🗺️ Roadmap

- [ ] GitHub Actions for automated concert addition
- [ ] Python CLI tool for interactive concert entry
- [ ] Data validation workflow
- [ ] Statistics auto-update workflow
- [ ] Wiki link checker workflow
- [ ] Backup/export functionality
- [ ] Concert photo gallery integration
- [ ] Setlist import from setlist.fm API

## 📜 License

This is a personal vault. All concert data is original content by the vault owner.

## 🙋 Support

For questions about structure or automation:
1. Check [Copilot Instructions](.github/copilot/instructions.md)
2. Review [Structure Guide](Musique/README-STRUCTURE.md)
3. Open a GitHub Issue for bugs or feature requests
