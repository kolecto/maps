import geopandas as gpd
import json

from shapely.geometry import mapping
from shapely.ops import unary_union
from shapely.affinity import translate, scale

departements_gdf = gpd.read_file("departements_full_fr.geojson")

caisses_regionales_ca = {
    "Alpes Provence": ["Bouches-du-Rhône", "Hautes-Alpes", "Vaucluse"],
    "Alsace Vosges": ["Bas-Rhin", "Haut-Rhin", "Vosges"],
    "Anjou et Maine": ["Maine-et-Loire", "Mayenne", "Sarthe"],
    "Aquitaine": ["Gironde", "Landes", "Lot-et-Garonne"],
    "Brie Picardie": ["Seine-et-Marne", "Somme", "Oise"],
    "Atlantique Vendée": ["Loire-Atlantique", "Vendée"],
    "Centre-est": ["Ain", "Rhône", "Saône-et-Loire"],
    "Centre France": ["Allier", "Cantal", "Corrèze", "Creuse", "Puy-de-Dôme"],
    "Centre Loire": ["Cher", "Loiret", "Nièvre"],
    "Centre Ouest": ["Indre", "Haute-Vienne"],
    "Champagne Bourgogne": ["Aube", "Côte-d'Or", "Haute-Marne", "Yonne"],
    "Charente Maritime Deux Sèvres": ["Charente-Maritime", "Deux-Sèvres"],
    "Charente-Périgord": ["Charente", "Dordogne"],
    "Corse": ["Corse-du-Sud", "Haute-Corse"],
    "Côtes d'Armor": ["Côtes-d'Armor"],
    "Finistère": ["Finistère"],
    "Franche-Comté": ["Doubs", "Jura", "Haute-Saône", "Territoire de Belfort"],
    "Guadeloupe": ["Guadeloupe"],
    "Paris et Ile-de-France": ["Essonne", "Hauts-de-Seine", "Paris", "Seine-Saint-Denis", "Val-de-Marne", "Val-d'Oise", "Yvelines"],
    "Ille-et-Vilaine": ["Ille-et-Vilaine"],
    "Languedoc": ["Aude", "Gard", "Hérault", "Lozère"],
    "Loire Haute Loire": ["Loire", "Haute-Loire"],
    "Lorraine": ["Meurthe-et-Moselle", "Meuse", "Moselle"],
    "Martinique-Guyane": ["Martinique", "Guyane"],
    "Morbihan": ["Morbihan"],
    "Nord de France": ["Nord", "Pas-de-Calais"],
    "Nord Est": ["Ardennes", "Aisne", "Marne"],
    "Nord Midi-Pyrénées": ["Aveyron", "Lot", "Tarn", "Tarn-et-Garonne"],
    "Normandie": ["Calvados", "Manche", "Orne"],
    "Normandie-Seine": ["Seine-Maritime", "Eure"],
    "Provence Côte d'Azur": ["Alpes-de-Haute-Provence", "Alpes-Maritimes", "Var"],
    "Pyrénées Gascogne": ["Gers", "Hautes-Pyrénées", "Pyrénées-Atlantiques"],
    "La Réunion - Mayotte": ["La Réunion", "Mayotte"],
    "Des Savoie": ["Savoie", "Haute-Savoie"],
    "Sud Méditerranée": ["Ariège", "Pyrénées-Orientales"],
    "Sud Rhône Alpes": ["Drôme", "Ardèche", "Isère"],
    "Toulouse 31": ["Haute-Garonne"],
    "Touraine et Poitou": ["Vienne", "Indre-et-Loire"],
    "Val de France": ["Loir-et-Cher", "Eure-et-Loir"]
}

encarts_transformations = {
    "Guadeloupe": {"xoff": 56.0,  "yoff": 30.6, "scale": 1},
    "Martinique": {"xoff": 55.5,  "yoff": 31.0, "scale": 1},
    "Guyane":     {"xoff": 47.8,  "yoff": 40.6, "scale": 0.25},
    "La Réunion": {"xoff": -61.0, "yoff": 64.5, "scale": 1},
    "Mayotte":    {"xoff": -50.6, "yoff": 55.4, "scale": 1},
}

regions_geoms = []

for region, deps in caisses_regionales_ca.items():
    geom_list = []
    
    for dep_name in deps:
        dep_row = departements_gdf[departements_gdf['nom'].str.lower() == dep_name.lower()]
        
        if dep_row.empty:
            print(f"⚠️ Attention : Le département '{dep_name}' n'a pas été trouvé dans le GeoJSON.")
            continue
            
        geom = dep_row.geometry.iloc[0]
        
        for target_name, params in encarts_transformations.items():
            if target_name in dep_name:
                if params["scale"] != 1:
                    geom = scale(geom, xfact=params["scale"], yfact=params["scale"], origin='centroid')
                geom = translate(geom, xoff=params["xoff"], yoff=params["yoff"])
                break 
                
        geom_list.append(geom)
    
    if geom_list:
        region_geom = unary_union(geom_list)
        
        regions_geoms.append({
            "type": "Feature",
            "properties": {"region_name": region},
            "geometry": mapping(region_geom)
        })

geojson_output = {
    "type": "FeatureCollection",
    "features": regions_geoms
}

output_path = 'caisses_regionales_ca.geojson'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(geojson_output, f, ensure_ascii=False)

print("✅ Traitement terminé. Le fichier 'caisses_regionales_ca.geojson' a été généré avec succès !")