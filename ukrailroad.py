import geopandas as gpd
import osmnx as ox
from shapely.geometry import Point, MultiLineString
from shapely.ops import unary_union, nearest_points
from shapely.geometry import MultiPoint, Point, GeometryCollection
import networkx as nx
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import scipy as sp
import pickle

stations_gdf = gpd.read_feather('dublinrails.feather')
railways_gdf = gpd.read_feather('dublinstation.feather')


G = nx.Graph()
G.graph['crs'] = 'EPSG:4326'
    
for idx, railway in railways_gdf.iterrows():
    if isinstance(railway.geometry, LineString):
        start_point, end_point = railway.geometry.coords[0], railway.geometry.coords[-1]
        
        edge_attributes = {
            'id': railway['@id'],
            'cutting': railway.get('cutting', None),  
            'electrified': railway.get('electrified', None),
            'frequency': railway.get('frequency', None),
            'gauge': railway.get('gauge', None),
            'maxspeed': railway.get('maxspeed', None),
            'name': railway.get('name', None),
            'railway': railway.get('railway', None),
            'ref': railway.get('ref', None),
            'usage': railway.get('usage', None),
            'voltage': railway.get('voltage', None),
            'wikipedia': railway.get('wikipedia', None)
        }
        
        G.add_edge(start_point, end_point, **edge_attributes)


def add_station_to_graph(station, graph, railways_gdf):
    station_point = Point(station.geometry.x, station.geometry.y)
    print(station["name"])
    
    station_attributes = {
        'id': station['@id'],
        'name': station['name'],
        'naptan:AtcoCode': station.get('naptan:AtcoCode', None),
        'network': station.get('network', None),
        'network:website': station.get('network:website', None),
        'network:wikidata': station.get('network:wikidata', None),
        'public_transport': station.get('public_transport', 'station'),
        'railway': station.get('railway', None),
        'ref:crs': station.get('ref:crs', None),
        'train': station.get('train', 'no'),
        'wheelchair': station.get('wheelchair', 'no'),
        'wikidata': station.get('wikidata', None),
        'wikipedia': station.get('wikipedia', None)
    }
    
    min_dist = float('inf')
    nearest_segment = None
    for railway in railways_gdf.geometry:
        point_on_railway = nearest_points(station_point, railway)[1]
        dist = station_point.distance(point_on_railway)
        if dist < min_dist:
            min_dist = dist
            nearest_segment = railway
    
    if nearest_segment:
        nearest_point_on_segment = nearest_points(station_point, nearest_segment)[1]
        
        graph.add_node(nearest_point_on_segment, type='station', name=station['name'])
        print(nearest_point_on_segment)
        
 
i =0 
for idx, station in stations_gdf.iterrows():
    i += 1 
    print(f"Station: {station['name']} Count: {i/3300*100}")
    add_station_to_graph(station, G, railways_gdf)


with open('railway_network.pkl', 'wb') as f:
    pickle.dump(G, f)