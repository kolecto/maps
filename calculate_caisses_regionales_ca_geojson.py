import geopandas as gpd
import json

from shapely.geometry import mapping

departements_gdf = gpd.read_file("departements_fr.geojson")

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
    "Charente-Maritime Deux-Sèvres": ["Charente-Maritime", "Deux-Sèvres"],
    "Charente-Périgord": ["Charente", "Dordogne"],
    "Corse": ["Corse-du-Sud", "Haute-Corse"],
    "Côtes d'Armor": ["Côtes-d'Armor"],
    "Finistère": ["Finistère"],
    "Franche-Comté": ["Doubs", "Jura", "Haute-Saône", "Territoire de Belfort"],
    "Guadeloupe": ["Guadeloupe"],
    "Île-de-France": ["Essonne", "Hauts-de-Seine", "Paris", "Seine-Saint-Denis", "Val-de-Marne", "Val-d'Oise", "Yvelines"],
    "Ille-et-Vilaine": ["Ille-et-Vilaine"],
    "Languedoc": ["Aude", "Gard", "Hérault", "Lozère"],
    "Loire Haute-Loire": ["Loire", "Haute-Loire"],
    "Lorraine": ["Meurthe-et-Moselle", "Meuse", "Moselle"],
    "Martinique et Guyane": ["Martinique", "Guyane"],
    "Morbihan": ["Morbihan"],
    "Nord de France": ["Nord", "Pas-de-Calais"],
    "Nord Est": ["Ardennes", "Aisne", "Marne"],
    "Nord Midi Pyrénées": ["Aveyron", "Lot", "Tarn", "Tarn-et-Garonne"],
    "Normandie": ["Calvados", "Manche", "Orne"],
    "Normandie-Seine": ["Seine-Maritime", "Eure"],
    "Provence Côte d'Azur": ["Alpes-de-Haute-Provence", "Alpes-Maritimes", "Var"],
    "Pyrénées Gascogne": ["Gers", "Hautes-Pyrénées", "Pyrénées-Atlantiques"],
    "La Réunion": ["La Réunion", "Mayotte"],
    "Savoie": ["Savoie", "Haute-Savoie"],
    "Sud Méditerranée": ["Ariège", "Pyrénées-Orientales"],
    "Sud Rhône Alpes": ["Drôme", "Ardèche", "Isère"],
    "Toulouse 31": ["Haute-Garonne"],
    "Touraine et Poitou": ["Vienne", "Indre-et-Loire"],
    "Val de France": ["Loir-et-Cher", "Eure-et-Loir"]
}

regions_geoms = []

for region, deps in caisses_regionales_ca.items():
    deps_in_region = departements_gdf[departements_gdf['nom'].isin(deps)]
    region_geom = deps_in_region.union_all()

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
with open(output_path, 'w') as f:
    json.dump(geojson_output, f)
