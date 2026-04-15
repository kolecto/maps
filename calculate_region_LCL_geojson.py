import geopandas as gpd
import json
from shapely.geometry import mapping

# 1. Chargement de la carte des départements
departements_gdf = gpd.read_file("departements_fr.geojson")

# 2. Définition des directions de réseau LCL basées sur l'organigramme officiel
regions_lcl = {

    "EST": [
        "Ardennes", "Aube", "Marne", "Haute-Marne", "Meurthe-et-Moselle", "Meuse", 
        "Moselle", "Bas-Rhin", "Haut-Rhin", "Vosges", "Côte-d'Or", "Doubs", 
        "Jura", "Nièvre", "Haute-Saône", "Saône-et-Loire", "Yonne", "Territoire de Belfort"
    ],
    

    "NORD OUEST": [
        "Aisne", "Nord", "Oise", "Pas-de-Calais", "Somme", 
        "Eure", "Seine-Maritime"
    ],
    
    "OUEST": [
        "Côtes-d'Armor", "Finistère", "Ille-et-Vilaine", "Morbihan", "Loire-Atlantique", 
        "Maine-et-Loire", "Mayenne", "Sarthe", "Vendée", "Cher", "Eure-et-Loir", 
        "Indre", "Indre-et-Loire", "Loir-et-Cher", "Loiret", "Calvados", "Manche", "Orne"
    ],

    "GRAND SUD OUEST": [
        "Charente", "Charente-Maritime", "Corrèze", "Creuse", "Dordogne", "Gironde", 
        "Landes", "Lot-et-Garonne", "Pyrénées-Atlantiques", "Deux-Sèvres", "Vienne", 
        "Haute-Vienne", "Ariège", "Aveyron", "Haute-Garonne", "Gers", "Lot", 
        "Hautes-Pyrénées", "Tarn", "Tarn-et-Garonne"
    ],
    
    "MÉDITERRANÉE": [
        "Alpes-de-Haute-Provence", "Hautes-Alpes", "Alpes-Maritimes", "Bouches-du-Rhône", 
        "Var", "Vaucluse", "Corse-du-Sud", "Haute-Corse", "Aude", "Gard", "Hérault", 
        "Lozère", "Pyrénées-Orientales"
    ],

    "AUVERGNE RHÔNE ALPES": [
        "Ain", "Allier", "Ardèche", "Cantal", "Drôme", "Isère", "Loire", 
        "Haute-Loire", "Puy-de-Dôme", "Rhône", "Savoie", "Haute-Savoie"
    ],
    
    "GRAND PARIS NORD & OUEST": [
        "Yvelines", "Hauts-de-Seine", "Val-d'Oise", "Paris" 
    ],
    
    "GRAND PARIS SUD & EST": [
        "Seine-et-Marne", "Essonne", "Seine-Saint-Denis", "Val-de-Marne"
    ]
}

regions_geoms = []

# 3. Fusion géométrique des départements
for region, deps in regions_lcl.items():
    deps_in_region = departements_gdf[departements_gdf['nom'].isin(deps)]
    
    if not deps_in_region.empty:
        region_geom = deps_in_region.union_all()

        regions_geoms.append({
            "type": "Feature",
            "properties": {"region_name": region},
            "geometry": mapping(region_geom)
        })

# 4. Sauvegarde
geojson_output = {
    "type": "FeatureCollection",
    "features": regions_geoms
}

output_path = 'regions_lcl_metropole.geojson'
with open(output_path, 'w') as f:
    json.dump(geojson_output, f)

print(f"✅ La carte officielle a été générée : {output_path}")