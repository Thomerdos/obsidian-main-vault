#!/usr/bin/env python3
"""
Script de normalisation des ingrédients pour les recettes Obsidian.
Règles:
- Français uniquement
- Singulier (sauf exceptions)
- Pas d'article
- Pas de quantité
- Pas de préparation
"""

import os
import re
from collections import defaultdict
from pathlib import Path

# Dictionnaire de normalisation des ingrédients
NORMALIZED_INGREDIENTS = {
    # Anglais vers français - Viandes
    'beef': 'boeuf',
    'chicken thigh )': 'cuisse de poulet',
    'chicken stock/broth': 'bouillon de poulet',
    'pork belly )': 'poitrine de porc',
    'pork shoulder butt': 'épaule de porc',
    'ground pork )': 'porc haché',
    
    # Légumes anglais vers français
    'bean sprouts, loosely packed': 'germes de soja',
    'broccoli': 'brocoli',
    'carrots , julienned)': 'carotte',
    'asparagus': 'asperge',
    'green onion/scallion': 'ciboule',
    'green onions, cut into 1" pieces on a bias': 'ciboule',
    'shallot': 'échalote',
    'shallots': 'échalote',
    'shallots )': 'échalote',
    'shallot/scallion stem )': 'ciboule',
    'garlic )': 'ail',
    'clove ail': 'ail',
    'cloves ail': 'ail',
    "d''ail": 'ail',
    "d''ail écrasées": 'ail',
    "d'ail": 'ail',
    "d'ail pressées": 'ail',
    "têtes d''ail": 'ail',
    'ginger': 'gingembre',
    'ginger )': 'gingembre',
    'knob ginger )': 'gingembre',
    'small piece gingembre': 'gingembre',
    'tranches gingembre': 'gingembre',
    'cm de gingembre frais': 'gingembre',
    'onion , blended or finely grated)': 'oignon',
    'red oignon': 'oignon rouge',
    'yellow oignon': 'oignon',
    'oignon, 1-cm': 'oignon',
    'green poivron': 'poivron vert',
    'red poivron': 'poivron rouge',
    'yellow poivron': 'poivron jaune',
    'poivron, any colour. 1-cm-wide strips': 'poivron',
    '¼ red bell pepper': 'poivron rouge',
    'napa cabbage , remove thick outer cabbage leaves)': 'chou chinois',
    'chou blanc )': 'chou blanc',
    'head shanghai bok choy': 'pak choi',
    'korean radish , julienned)': 'radis',
    'petits navets': 'navet',
    'mini cucumber or regular cucumber, halved lengthwise and': 'concombre',
    
    # Ingrédients asiatiques
    'thai basil leaves': 'basilic thaï',
    'thai basilic leaves': 'basilic thaï',
    'thai eggplant )': 'aubergine thaï',
    'thai sriraja panich sauce': 'sauce sriracha',
    '3-4 tbsp thai cooking tamarind': 'tamarin',
    'palm sugar, chopped': 'sucre de palme',
    'fermented shrimp paste': 'pâte de crevette',
    'salted fermented shrimp': 'crevettes fermentées',
    'dried shrimp, medium size, roughly': 'crevettes séchées',
    'ounces pâte de crevette': 'pâte de crevette',
    'dried algue wakame': 'algue wakame',
    'feuille de nori': 'nori',
    'dried chili flakes, to taste': 'piment en flocons',
    'dry chilies': 'piment séché',
    'dry red spur chilies': 'piment rouge séché',
    'fresh red chilies': 'piment rouge',
    'sichuan dried piment flakes': 'piment du Sichuan',
    '1,5 cs de piment moulu': 'piment moulu',
    'petits piment': 'piment',
    'piments forts': 'piment fort',
    "piment d''espelette": "piment d'Espelette",
    'makrut lime leaves )': 'feuille de combava',
    'kaffir lime leaves': 'feuille de combava',
    'kaffir lime skin': 'zeste de combava',
    'lemongrass': 'citronnelle',
    'galangal': 'galanga',
    'piece fingerroot': 'krachai',
    'korean chives , cut in 5 cm / 2 inch length)': 'ciboulette coréenne',
    'korean coarse sea salt , )': 'gros sel',
    'korean sauce de poisson': 'sauce de poisson',
    'gochugaru , )': 'piment coréen',
    'yardlong beans': 'haricot kilomètre',
    '7-10 stalks garlic chives, cut into 2" pieces': 'ciboulette chinoise',
    'stalks cébette': 'ciboule',
    'stem cébette': 'ciboule',
    
    # Sauces et condiments
    'soy sauce )': 'sauce soja',
    'light soy sauce': 'sauce soja claire',
    'dark soy sauce': 'sauce soja foncée',
    'good fish sauce': 'sauce de poisson',
    "sauce huître": "sauce d'huître",
    'rice vinegar': 'vinaigre de riz',
    'white vinegar or riz wine vinegar': 'vinaigre de riz',
    'vinegar': 'vinaigre',
    'cooking wine': 'vin de cuisine',
    'sake': 'saké',
    'sake )': 'saké',
    'mirin': 'mirin',
    'miso': 'miso',
    'miso )': 'miso',
    'doubanjiang': 'pâte de piment',
    'japanese karashi or hot english mustard )': 'moutarde japonaise',
    'japanese sesame paste': 'pâte de sésame',
    'toasted huile de sésame': 'huile de sésame grillée',
    
    # Huiles
    "d''huile": 'huile',
    "d'huile": 'huile',
    'cooking oil': 'huile',
    'neutral oil': 'huile neutre',
    'huile végétale': 'huile',
    "peu d''huile végétale": 'huile',
    "huile d''olive": "huile d'olive",
    "huile d'olive": "huile d'olive",
    "càs d''huile d''olive": "huile d'olive",
    'huile de maïs': 'huile de maïs',
    'huile de sésame': 'huile de sésame',
    
    # Épices et herbes
    'basilicic': 'basilic',
    'basilicic frais': 'basilic',
    'persil haché': 'persil',
    'botte de persil plat lavé et haché': 'persil',
    'bouquet de persil pour obtenir environ ½ tasse de persil une fois ciselé': 'persil',
    'botte coriandre': 'coriandre',
    'thym effeuillé': 'thym',
    'aneth': 'aneth',
    'origan': 'origan',
    "cuillères à soupe d'origan fraîchement ciselé": 'origan',
    'menthe': 'menthe',
    'turmeric': 'curcuma',
    'pointe de curcuma': 'curcuma',
    'paprika': 'paprika',
    'c. à soupe piment doux en poudre': 'piment doux',
    'clous de girofle': 'clou de girofle',
    'piece star anise': 'anis étoilé',
    'muscade': 'noix de muscade',
    'laurier': 'feuille de laurier',
    'bouquet garni': 'bouquet garni',
    
    # Sel et poivre
    'cooking salt , )': 'sel',
    'fine sea sel': 'sel fin',
    'diamond crystal kosher salt )': 'gros sel',
    'ounces sel': 'sel',
    'pinch sel': 'sel',
    'sel de maldon': 'fleur de sel',
    'sel ou sel fin': 'sel',
    'bonne pincée de sel': 'sel',
    'cuillère à café rase de gros sel': 'gros sel',
    'cuillère à soupe de sel': 'sel',
    "ail sel": "sel d'ail",
    'sel et poivre': 'sel',  # sera dédoublé
    'sel et poivre du moulin': 'sel',
    'sel, poivre': 'sel',
    "sel, poivre du moulin, persil 1cuill à soupe d''huile d''olive": 'sel',
    'white poivre': 'poivre blanc',
    'poivre en grains': 'poivre',
    
    # Sucres
    'brown sucre': 'sucre roux',
    'brown sucre, packed': 'sucre roux',
    'raw sucre': 'sucre roux',
    'sugar )': 'sucre',
    'cs sucre': 'sucre',
    '1.5 cuillères à soupe de sucre': 'sucre',
    'cuillère à soupe rase de sucre': 'sucre',
    'vergeoise': 'vergeoise',
    'grosse cuillère à soupe de miel liquide': 'miel',
    
    # Farines et féculents
    'all-purpose flour': 'farine',
    'cuiller de farine': 'farine',
    'glutinous rice flour )': 'farine de riz gluant',
    'fécule de pomme de terre': 'fécule de pomme de terre',
    'maizena': 'fécule de maïs',
    'baking soda': 'bicarbonate de soude',
    
    # Produits laitiers et œufs
    '1-2 œufs': 'oeuf',
    "jaune d''œuf": "jaune d'oeuf",
    'beurre mou': 'beurre',
    'grammes de beurre': 'beurre',
    'graisse de canard ou de beurre clarifié': 'graisse de canard',
    'crème entière': 'crème',
    'crème fraîche': 'crème fraîche',
    'crème fraîche liquide': 'crème liquide',
    'cuiller à soupe de crème épaisse': 'crème épaisse',
    'cuillère à soupe de mayonnaise': 'mayonnaise',
    'unsweetened soy milk )': 'lait de soja',
    
    # Fromages
    'fromages': 'fromage',
    'mozzarella': 'mozzarella',
    'parmesan': 'parmesan',
    
    # Pâtes et nouilles
    'dry rice noodles, medium size, soak in room temp water for 1 hour': 'nouilles de riz',
    'hong kong style pan-fried nouilles': 'nouilles',
    'servings fresh ramen nouilles': 'nouilles ramen',
    'paquet de nouilles': 'nouilles',
    'linguines de semoule ou de spaghettis': 'linguine',
    'spaghetti': 'spaghetti',
    
    # Riz et céréales
    'jasmine riz for serving': 'riz jasmin',
    'riz basmati': 'riz basmati',
    'boulghour': 'boulgour',
    'couscous complet': 'couscous',
    'verre frik': 'frik',
    
    # Légumineuses
    'bol de pois chiches': 'pois chiche',
    'pois chiches': 'pois chiche',
    'petits pois': 'petit pois',
    'haricots verts': 'haricot vert',
    
    # Viandes détaillées
    'boeuf haché': 'boeuf haché',
    'viande de boeuf': 'boeuf',
    'gîte détaillée en fines tranches': 'gîte de boeuf',
    'paleron détaillés en cube de 70 g maximum': 'paleron',
    'macreuse': 'macreuse',
    'rosbif': 'rosbif',
    'veau': 'veau',
    'mouton': 'mouton',
    'pilons de poulet': 'pilon de poulet',
    'poitrine de porc': 'poitrine de porc',
    'poitrine de porc salée': 'poitrine de porc',
    'poitrine de porc salée en tranches larges': 'poitrine de porc',
    'lardons': 'lardon',
    'saucisses fraîches': 'saucisse',
    'saucisses fumées': 'saucisse fumée',
    'saumon': 'saumon',
    'seiches': 'seiche',
    'large shrimp': 'crevette',
    'medium sized shrimp, or as many as you like': 'crevette',
    "poignées de palourdes bien trempées à l''avance": 'palourde',
    
    # Tofu et produits végétaux
    'medium firm tofu, 1" cubed, or another meat of your choice, cut into small bite-sized': 'tofu ferme',
    'soft/silken tofu': 'tofu soyeux',
    'pressed tofu, cut into small pieces': 'tofu pressé',
    
    # Légumes divers
    'botte asperge blanche': 'asperge blanche',
    'échalotes ciselées': 'échalote',
    'grosses échalotes': 'échalote',
    'echalotes': 'échalote',
    'oignon ou échalote': 'oignon',
    'oignon vert': 'oignon vert',
    "bout d''oignons verts ou poireau": 'oignon vert',
    "bouts d''oignons verts ou poireau": 'oignon vert',
    'poireau ou quelques oignons verts': 'poireau',
    'poireaux': 'poireau',
    'céleri': 'céleri',
    'champignon': 'champignon',
    'morilles': 'morille',
    'shitaké séchés': 'champignon shiitake',
    'shitakés séchés': 'champignon shiitake',
    'aubergine': 'aubergine',
    'courgette': 'courgette',
    'pomme de terre': 'pomme de terre',
    'carotte': 'carotte',
    'tomate': 'tomate',
    'bocal de 750 ml de sauce tomate fraiche': 'sauce tomate',
    'concentré de tomate': 'concentré de tomate',
    'cs de tomate concentrée': 'concentré de tomate',
    'pineapple': 'ananas',
    'pineapple, bite-sized pieces': 'ananas',
    'laitue': 'laitue',
    'sucrine': 'sucrine',
    'épinard': 'épinard',
    'tasse de ciboule': 'ciboule',
    
    # Fruits et agrumes
    'citron': 'citron',
    'citron vert': 'citron vert',
    'citron confit': 'citron confit',
    "jus d'un demi-citron": 'jus de citron',
    'cuillère à café de jus de citron frais': 'jus de citron',
    'bout de zeste de citron ou yuzu': 'zeste de citron',
    
    # Noix et graines
    'cashews': 'noix de cajou',
    'roasted peanuts, roughly': 'cacahuète',
    'dash graines de sésame': 'graines de sésame',
    'cuillères à soupe de graines de sésame noir': 'graines de sésame noir',
    
    # Boissons et liquides
    "d''eau": 'eau',
    'water )': 'eau',
    'bouillon de poulet': 'bouillon de poulet',
    'litres de bouillon de cuisson': 'bouillon',
    'fond de veau lié': 'fond de veau',
    'litre de fond de veau lié': 'fond de veau',
    'verre de vin blanc': 'vin blanc',
    'vin blanc': 'vin blanc',
    'vin rouge corsé': 'vin rouge',
    'bouteille de bière jenlain ou de leffe brune': 'bière brune',
    'cognac': 'cognac',
    'lait de coco': 'lait de coco',
    
    # Condiments et pâtes
    'green curry paste': 'pâte de curry vert',
    'red curry paste': 'pâte de curry rouge',
    'ketchup': 'ketchup',
    'moutarde': 'moutarde',
    
    # Vinaigres
    'vinaigre de vin': 'vinaigre de vin',
    'cuillères à soupe de vinaigre blanc': 'vinaigre blanc',
    'cuillères à soupe de vinaigre de riz': 'vinaigre de riz',
    'cuillères à soupe de vinaigre de vin rouge': 'vinaigre de vin rouge',
    
    # Ingrédients japonais spécifiques
    'kombu': 'kombu',
    'piece kombu )': 'kombu',
    'morceau kombu': 'kombu',
    'katsuobushi': 'katsuobushi',
    'katsuobushi )': 'katsuobushi',
    'cs bonite séchée': 'katsuobushi',
    'menma': 'menma',
    'la-yu': 'huile de piment',
    'sweet preserved daikon radish': 'radis daikon confit',
    
    # Divers
    'c. à soupe smen': 'smen',
    'cc de glutamate monosodique': 'glutamate monosodique',
    'cs saké': 'saké',
    "cuillère à soupe d''eau": 'eau',
    "cuillère à soupe d''huile de sésame": 'huile de sésame',
    "tranches de pain d''épices ou de pain rassis": "pain d'épices",
    
    # Supprimer les entrées invalides
    'roughly': None,
    'préparation': None,
    'mixeur': None,
    'sachet plastique pour congélation': None,
    'garnishes and condiments for serving: chili flakes, roasted peanuts, bean sprouts': None,
    "[[cuillère à café de vinaigre de vin blanc ou rouge selon la coloration que vous": None,
    "[[garnishes and condiments for serving: chili flakes, roasted peanuts, bean sprouts": None,
    "[[medium firm tofu, 1\" cubed, or another meat of your choice, cut into small bite-sized": None,
    "[[petit piment rouge : retirer les graines et la membrane intérieure blanche puis": None,
}

def normalize_ingredient(ingredient):
    """Normalise un ingrédient selon les règles définies"""
    # Supprimer les guillemets et crochets mal placés
    ingredient = ingredient.strip("'\"[]")
    
    # Vérifier le dictionnaire de normalisation
    if ingredient in NORMALIZED_INGREDIENTS:
        return NORMALIZED_INGREDIENTS[ingredient]
    
    # Règles génériques de nettoyage
    # Supprimer les parenthèses et leur contenu
    ingredient = re.sub(r'\s*\([^)]*\)', '', ingredient)
    
    # Convertir en minuscule pour traitement
    lower = ingredient.lower()
    
    # Cas spéciaux déjà corrects (légumes pluriels par nature)
    if lower in ['épinards', 'haricots verts', 'petits pois']:
        return lower
    
    return ingredient if ingredient else None

def extract_frontmatter(content):
    """Extrait le frontmatter d'un fichier markdown"""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return None, content

def parse_frontmatter(frontmatter_text):
    """Parse le frontmatter en dictionnaire"""
    result = {}
    current_key = None
    current_list = []
    
    for line in frontmatter_text.split('\n'):
        if ':' in line and not line.startswith(' ') and not line.startswith('-'):
            # Nouvelle clé
            if current_key and current_list:
                result[current_key] = current_list
                current_list = []
            
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if value:
                result[key] = value
                current_key = None
            else:
                current_key = key
        elif line.startswith('- ') and current_key:
            # Élément de liste
            item = line[2:].strip()
            current_list.append(item)
    
    if current_key and current_list:
        result[current_key] = current_list
    
    return result

def serialize_frontmatter(data):
    """Sérialise un dictionnaire en frontmatter YAML"""
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"- {item}")
        else:
            lines.append(f"{key}: {value}")
    return '\n'.join(lines)

def main():
    vault_dir = Path("/home/runner/work/obsidian-main-vault/obsidian-main-vault")
    recettes_dir = vault_dir / "contenus" / "recettes" / "Fiches"
    ingredients_dir = vault_dir / "contenus" / "recettes" / "Ingredients"
    
    # Collecter tous les ingrédients normalisés utilisés
    all_normalized_ingredients = set()
    recettes_to_update = []
    
    print("=== Phase 1: Analyse des recettes ===")
    for recipe_file in recettes_dir.glob("*.md"):
        with open(recipe_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter_text, body = extract_frontmatter(content)
        if not frontmatter_text:
            continue
        
        frontmatter = parse_frontmatter(frontmatter_text)
        
        if 'ingredients' not in frontmatter:
            continue
        
        original_ingredients = frontmatter['ingredients']
        if not isinstance(original_ingredients, list):
            continue
        
        # Normaliser les ingrédients
        normalized = []
        for ing in original_ingredients:
            # Extraire l'ingrédient du wikilink s'il y en a un
            ing_clean = ing.strip("'\"")
            if ing_clean.startswith('[[') and ing_clean.endswith(']]'):
                ing_clean = ing_clean[2:-2]
            
            # Normaliser
            norm = normalize_ingredient(ing_clean)
            if norm:
                normalized.append(f"'[[{norm}]]'")
                all_normalized_ingredients.add(norm)
        
        # Enregistrer pour mise à jour
        if normalized:
            recettes_to_update.append({
                'file': recipe_file,
                'frontmatter': frontmatter,
                'body': body,
                'new_ingredients': normalized
            })
    
    print(f"Ingrédients normalisés uniques: {len(all_normalized_ingredients)}")
    print(f"Recettes à mettre à jour: {len(recettes_to_update)}")
    
    # Afficher les ingrédients normalisés
    print("\n=== Ingrédients normalisés ===")
    for ing in sorted(all_normalized_ingredients):
        print(f"  - {ing}")
    
    print(f"\n=== Phase 2: Mise à jour des recettes ===")
    for item in recettes_to_update:
        item['frontmatter']['ingredients'] = item['new_ingredients']
        
        # Reconstruire le fichier
        new_frontmatter = serialize_frontmatter(item['frontmatter'])
        new_content = f"---\n{new_frontmatter}\n---\n{item['body']}"
        
        with open(item['file'], 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ {item['file'].name}")
    
    print(f"\n=== Phase 3: Nettoyage des pages d'ingrédients ===")
    # Supprimer toutes les pages d'ingrédients existantes
    deleted_count = 0
    for ing_file in ingredients_dir.glob("*.md"):
        ing_file.unlink()
        deleted_count += 1
    print(f"Supprimé {deleted_count} anciennes pages d'ingrédients")
    
    print(f"\n=== Phase 4: Création des nouvelles pages d'ingrédients ===")
    # Créer les nouvelles pages d'ingrédients normalisés
    for ingredient in sorted(all_normalized_ingredients):
        ing_file = ingredients_dir / f"{ingredient}.md"
        content = f"""---
title: {ingredient.capitalize()}
type: ingredient
---

# {ingredient.capitalize()}

Ingrédient utilisé dans les recettes.
"""
        with open(ing_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ {ingredient}")
    
    print(f"\n=== Résumé ===")
    print(f"Recettes mises à jour: {len(recettes_to_update)}")
    print(f"Anciennes pages supprimées: {deleted_count}")
    print(f"Nouvelles pages créées: {len(all_normalized_ingredients)}")

if __name__ == "__main__":
    main()
