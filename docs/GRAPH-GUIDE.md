# 🌐 Graph View Guide

Complete guide to visualizing and navigating your vault's relational database using Obsidian's Graph View.

## Table of Contents

1. [Opening Graph View](#opening-graph-view)
2. [Understanding the Graph](#understanding-the-graph)
3. [Filtering and Navigation](#filtering-and-navigation)
4. [Color Coding](#color-coding)
5. [Common Use Cases](#common-use-cases)
6. [Troubleshooting](#troubleshooting)

## Opening Graph View

### Global Graph

View the entire vault:
- **Command**: `Ctrl/Cmd + G` or click the graph icon
- Shows all notes and connections

### Local Graph

View connections for the current note:
- **Command**: Open command palette → "Open local graph"
- Shows only immediate connections
- Adjustable depth (1, 2, 3+ levels)

## Understanding the Graph

### Node Types

Each entity type appears as a distinct node:

| Entity | Icon | Color | Description |
|--------|------|-------|-------------|
| Concert | 🎸 | `#FF6B6B` (Red) | Individual concert events |
| Groupe | 🎤 | `#4ECDC4` (Cyan) | Musical artists/bands |
| Genre | 🎵 | `#95E1D3` (Mint) | Musical genres |
| Salle | 🏛️ | `#F38181` (Pink) | Concert venues |
| Festival | 🎪 | `#AA96DA` (Purple) | Music festivals |
| Ville | 🏙️ | `#FCBAD3` (Rose) | Cities |
| Pays | 🌍 | `#A8E6CF` (Green) | Countries |

### Connection Types

**Solid lines**: Direct wiki-links `[[Page]]`
**Dashed lines**: Backlinks (inverse relations)

### Node Size

Larger nodes = more connections
- Highly connected entities appear larger
- Helps identify central nodes

## Filtering and Navigation

### Basic Filters

Access via the filter icon in Graph View:

**By Type:**
```
path:Musique/Concerts    # Show only concerts
path:Musique/Groupes     # Show only artists
path:Musique/Genres      # Show only genres
path:Lieux/Villes        # Show only cities
```

**By Tag:**
```
tag:#concert    # Concert notes
tag:#groupe     # Artist notes
tag:#festival   # Festival notes
```

**By Name:**
```
file:"Iron Maiden"    # Specific artist
file:"Lyon"           # Specific city
```

### Advanced Filters

**Exclude Templates:**
```
-path:Templates
-path:_templates
```

**Date Range:**
```
path:Musique/Concerts/2024    # 2024 concerts only
path:Musique/Concerts/202     # 2020-2029
```

**Multiple Conditions:**
```
path:Musique/Concerts OR path:Musique/Groupes
```

### Depth Settings

For Local Graph:
- **Depth 1**: Immediate connections only
- **Depth 2**: Friends of friends
- **Depth 3+**: Extended network

## Color Coding

### Setting Up Colors

1. Open Graph View settings
2. Go to "Groups"
3. Add color groups:

```
Group 1: Concerts
Query: path:Musique/Concerts
Color: #FF6B6B

Group 2: Groupes
Query: path:Musique/Groupes
Color: #4ECDC4

Group 3: Genres
Query: path:Musique/Genres
Color: #95E1D3

Group 4: Salles
Query: path:Musique/Salles
Color: #F38181

Group 5: Festivals
Query: path:Musique/Festivals
Color: #AA96DA

Group 6: Villes
Query: path:Lieux/Villes
Color: #FCBAD3

Group 7: Pays
Query: path:Lieux/Pays
Color: #A8E6CF
```

### Pre-configured Setup

Copy this to `.obsidian/graph.json`:
```json
{
  "collapse-filter": true,
  "search": "",
  "showTags": false,
  "showAttachments": false,
  "hideUnresolved": false,
  "showOrphans": true,
  "collapse-color-groups": false,
  "colorGroups": [
    {
      "query": "path:Musique/Concerts",
      "color": {
        "a": 1,
        "rgb": 16737643
      }
    },
    {
      "query": "path:Musique/Groupes",
      "color": {
        "a": 1,
        "rgb": 5164484
      }
    },
    {
      "query": "path:Musique/Genres",
      "color": {
        "a": 1,
        "rgb": 9823699
      }
    },
    {
      "query": "path:Musique/Salles",
      "color": {
        "a": 1,
        "rgb": 15958401
      }
    },
    {
      "query": "path:Musique/Festivals",
      "color": {
        "a": 1,
        "rgb": 11179482
      }
    },
    {
      "query": "path:Lieux/Villes",
      "color": {
        "a": 1,
        "rgb": 16563923
      }
    },
    {
      "query": "path:Lieux/Pays",
      "color": {
        "a": 1,
        "rgb": 11005647
      }
    }
  ],
  "collapse-display": false,
  "showArrow": true,
  "textFadeMultiplier": 0,
  "nodeSizeMultiplier": 1,
  "lineSizeMultiplier": 1,
  "collapse-forces": false,
  "centerStrength": 0.5,
  "repelStrength": 10,
  "linkStrength": 1,
  "linkDistance": 250,
  "scale": 1
}
```

## Common Use Cases

### Explore Music Discovery

**Find similar artists:**
1. Open artist page (e.g., "Tool")
2. View local graph (depth 2)
3. Look for connected artists via:
   - Shared genres (green nodes)
   - Shared concerts (red nodes)

**Discover genre relationships:**
1. Open genre page (e.g., "Progressive Metal")
2. View local graph (depth 2)
3. See parent genres, child genres, and related genres

### Concert History Visualization

**See concert timeline:**
1. Global graph with filter: `path:Musique/Concerts`
2. Adjust forces to spread nodes
3. Larger nodes = more connections (multi-artist shows, festivals)

**Festival editions:**
1. Open festival page
2. Local graph shows all editions as connected concert nodes

### Location-Based Exploration

**Concerts in a city:**
1. Open city page (e.g., "Lyon")
2. Local graph shows:
   - Venues (pink nodes)
   - Concerts (red nodes)
   - Festivals (purple nodes)

**Country overview:**
1. Open country page (e.g., "France")
2. Depth 2 local graph shows:
   - Cities (rose nodes)
   - Artists from this country (cyan nodes)
   - All concerts in country (red nodes)

### Genre Hierarchies

**Visualize genre tree:**
1. Filter: `path:Musique/Genres`
2. Adjust repel strength to 15
3. See parent-child relationships
4. Identify genre clusters

### Artist Networks

**Find tour companions:**
1. Open artist page
2. Look for `groupe-tour-together` connections
3. See which artists frequently play together

**Identify scene connections:**
1. Global graph filtered to specific genres
2. See interconnected artists in a music scene

## Recommended Settings

### For Overview (Global Graph)

```
Repel Strength: 10
Link Strength: 1
Link Distance: 250
Center Strength: 0.5
Node Size: 1.0
Text Fade: 0
Arrows: On
```

### For Detail (Local Graph)

```
Repel Strength: 5
Link Strength: 0.8
Link Distance: 150
Center Strength: 0.7
Node Size: 1.5
Text Fade: -1
Arrows: On
```

### For Clustering

```
Repel Strength: 15
Link Strength: 0.5
Link Distance: 300
Center Strength: 0.3
Node Size: 1.2
```

## Interaction Tips

### Mouse/Trackpad

- **Hover**: Show node name
- **Click**: Open note
- **Right-click**: Context menu
  - Open in new pane
  - Open in new window
  - Open local graph
- **Drag**: Move node (releases after a moment)
- **Scroll**: Zoom in/out
- **Drag background**: Pan view

### Keyboard

- `Ctrl/Cmd + Click`: Open in new pane
- `Ctrl/Cmd + Shift + Click`: Open in new window
- `Space + Drag`: Pan view
- `+/-`: Zoom

## Troubleshooting

### Missing Connections

**Problem**: Notes don't show expected connections

**Solutions:**
1. Check frontmatter has correct wiki-link format: `[[Page Name]]`
2. Run `tools/sync-graph.py` to synchronize bidirectional relations
3. Verify note names match exactly (case-sensitive)
4. Ensure `.md` extension is not in frontmatter links

### Cluttered Graph

**Problem**: Too many nodes, can't see structure

**Solutions:**
1. Use filters to show specific types
2. Increase repel strength (10-15)
3. Hide orphan nodes
4. Use local graph instead of global
5. Filter by date ranges for concerts

### Nodes Too Small/Large

**Problem**: Can't read labels or graph is too spread out

**Solutions:**
1. Adjust node size multiplier (0.5 - 2.0)
2. Adjust text fade (-2 to 2)
3. Zoom in/out
4. Adjust link distance (100-400)

### Colors Not Showing

**Problem**: All nodes are the same color

**Solutions:**
1. Check color groups are configured
2. Verify query syntax in color groups
3. Ensure notes have correct paths
4. Reload Obsidian if needed

### Performance Issues

**Problem**: Graph is slow or laggy

**Solutions:**
1. Use filters to reduce visible nodes
2. Close other resource-intensive applications
3. Reduce link distance
4. Hide orphan nodes
5. Use local graph for large vaults (500+ notes)

## Advanced Techniques

### Temporal Navigation

Create time-based filters:
```
path:Musique/Concerts/2024 OR path:Musique/Concerts/2023
```

See evolution of your concert history over time.

### Hub Identification

Look for nodes with many connections:
- **Concert hubs**: Multi-artist festivals
- **Artist hubs**: Prolific bands you've seen many times
- **Venue hubs**: Frequently visited venues
- **Genre hubs**: Central genres in your taste

### Cluster Analysis

Identify groups of related entities:
1. Use genre-filtered graph
2. Look for tight clusters
3. Represents music scenes or styles
4. Example: "Nordic Black Metal" cluster

### Path Finding

Find connections between entities:
1. Open first entity
2. Local graph (depth 3-4)
3. Look for path to second entity
4. Example: "How am I connected to this artist?"

## Plugins Integration

### Breadcrumbs Plugin

Enhances graph view with explicit hierarchies:
- Parent/child relationships
- Custom relation types
- Hierarchical views

Configuration in `.obsidian/plugins/breadcrumbs/`:
```json
{
  "relations": {
    "parent": ["genre-parent"],
    "child": ["genre-children"],
    "sibling": ["genre-related"]
  }
}
```

### Dataview Integration

Graph view works alongside Dataview:
- Dataview queries show in note
- Graph shows visual connections
- Complementary views of same data

## Best Practices

1. **Regular Sync**: Run `tools/sync-graph.py` weekly
2. **Consistent Naming**: Use exact note names in links
3. **Complete Data**: Fill in all relation fields
4. **Use Tags**: Helps with filtering
5. **Check Orphans**: Find disconnected notes
6. **Color Code**: Makes navigation easier
7. **Adjust Settings**: Find what works for your workflow
8. **Local First**: Use local graph for focused exploration
9. **Filter Often**: Reduce clutter
10. **Save Views**: Document useful filter combinations

## Example Workflows

### Weekly Review

1. Open global graph
2. Filter to current week: `path:Musique/Concerts/2024`
3. See new concerts and connections
4. Check for missing artist/venue pages

### Pre-Concert Research

1. Open artist page
2. Local graph (depth 2)
3. Explore similar artists
4. Check past concerts at same venue
5. Review genre connections

### Genre Exploration

1. Open genre page
2. Local graph (depth 3)
3. Discover new artists in genre
4. See related genres
5. Find genre hierarchies

### Festival Planning

1. Open festival page
2. Local graph shows previous editions
3. See which artists typically play
4. Compare with artist wish list

## See Also

- [SCHEMA.md](SCHEMA.md) - Entity schemas
- [RELATIONS.md](RELATIONS.md) - Relationship details
- [README-RELATIONS.md](../README-RELATIONS.md) - User guide
- [Obsidian Graph View Documentation](https://help.obsidian.md/Plugins/Graph+view)
