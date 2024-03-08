import osmnx as ox
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
import numpy as np
import geopy.distance

stations_gdf = gpd.read_feather('dublinstation.feather')
rails_gdf = gpd.read_feather('dublinrails.feather')


start_end_points = []
for geometry in rails_gdf['geometry']:

    if not geometry.is_empty:
        coords = list(geometry.coords)

        start_end_points.append(coords[0]) 
        start_end_points.append(coords[-1])  

unique_points = set(start_end_points)

import networkx as nx

G = nx.Graph()

coord_to_node = {}
node_id = 0
for point in unique_points:
    G.add_node(node_id, pos=point)
    coord_to_node[point] = node_id
    node_id += 1


for geometry in rails_gdf['geometry']:
    if not geometry.is_empty:
        coords = list(geometry.coords)
        start_node_id = coord_to_node[coords[0]]
        end_node_id = coord_to_node[coords[-1]]
        G.add_edge(start_node_id, end_node_id)

print(G)
import matplotlib.pyplot as plt

pos = {node: data['pos'] for node, data in G.nodes(data=True)}


plt.figure(figsize=(10, 10))  

nx.draw_networkx_nodes(G, pos, node_size=30, node_color='blue', alpha=0.6)


nx.draw_networkx_edges(G, pos, width=1, edge_color='gray', alpha=0.5)


plt.title('Railway Network')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
#plt.xlim(min(pos.values(), key=lambda x: x[0])[0] - 0.01, max(pos.values(), key=lambda x: x[0])[0] + 0.01)
#plt.ylim(min(pos.values(), key=lambda x: x[1])[1] - 0.01, max(pos.values(), key=lambda x: x[1])[1] + 0.01)

plt.show()
"""
ox.config(use_cache=True, log_console=True)
custom_filter = '["railway"~"rail"]'


G1= ox.graph_from_place('Dublin', custom_filter=custom_filter, network_type='all')
#stations_gdf = ox.geometries_from_place(overpass_query)
print(stations_gdf)

print(G1)
"""

def calculate_distance(line):
    if isinstance(line, LineString):
        #return sum(geopy.distance.geodesic((line.coords[i][1], line.coords[i][0]),
                                           #(line.coords[i + 1][1], line.coords[i + 1][0])).meters
                   #for i in range(len(line.coords) - 1))
        return 1
    else:
        return 0


for u, v, key, data in G1.edges(keys=True, data=True):
    if 'geometry' in data:

        data['distance'] = calculate_distance(data['geometry'])
    else:
        point_u = Point(G1.nodes[u]['x'], G1.nodes[u]['y'])
        point_v = Point(G1.nodes[v]['x'], G1.nodes[v]['y'])
        #data['distance'] = geopy.distance.geodesic((point_u.y, point_u.x), (point_v.y, point_v.x)).meters
        data['distance'] = 1


def insert_station_into_nearest_edge(G, station_point, station_attributes):

    nearest_edge = ox.distance.nearest_edges(G, X=station_point.x, Y=station_point.y, return_dist=False)
    print(nearest_edge)
    u,v,key = nearest_edge
    

    edge_geom = G[u][v][key]['geometry'] if 'geometry' in G[u][v][key] else LineString([Point(G.nodes[u]['x'], G.nodes[u]['y']), Point(G.nodes[v]['x'], G.nodes[v]['y'])])

    nearest_point_on_edge = nearest_points(edge_geom, station_point)[0]

    station_node = max(G.nodes()) + 1 
    G.add_node(station_node, x=nearest_point_on_edge.x, y=nearest_point_on_edge.y, **station_attributes)

    if G.has_edge(u, v, key):
        print(f"Edge ({u}, {v}, {key}) exists before removal with attribute")
    else:
        print(f"Edge ({u}, {v}, {key}) does not exist before removal.")


    dictionary_vals = G[u][v][key]
    G.remove_edge(u, v, key)

    # Before removal, check if the edge exists
    if G.has_edge(u, v, key):
        print(f"Edge ({u}, {v}, {key}) exists before removal with attributes: {G[u][v][key]}")
    else:
        print(f"Edge ({u}, {v}, {key}) does not exist before removal.")


    G.add_edge(u, station_node, **dictionary_vals)
    G.add_edge(station_node, v, **dictionary_vals)

for idx, station in stations_gdf.iterrows():
    station_point = Point(station.geometry.x, station.geometry.y)
    station_attributes = {
       'name': station['name'],
       'type': 'station'
    }
    insert_station_into_nearest_edge(G1, station_point, station_attributes)

node_colors = []
i = 0
j = 0 
for node, data in G1.nodes(data=True):
    if data.get('type') == 'station':
        node_colors.append('red')
        i +=1
        print(data.get("name"))
    else:
        j +=1
        node_colors.append('blue') 

print(i)
print(j)

G1 = G1.to_undirected()

fig, ax = ox.plot_graph(G1, node_color=node_colors, node_size=30, edge_linewidth=1, edge_color='gray')

def get_station_node_id(G, station_name):
    for node, data in G.nodes(data=True):
        if data.get('type') == 'station' and data.get('name') == station_name:
            print(data.get('name'))
            return node
    return None

station_a_name = "Raheny"
station_b_name = "Killester"


def find_shortest_path_by_distance(G, station_name_1, station_name_2):
    # Get the node IDs for the given station names
    station_id_1 = get_station_node_id(G, station_name_1)
    station_id_2 = get_station_node_id(G, station_name_2)

    if station_id_1 is None or station_id_2 is None:
        print(f"Could not find one of the stations: {station_name_1} or {station_name_2}")
        return None

    try:
        shortest_path = nx.shortest_path(G, source=station_id_1, target=station_id_2, weight='distance')
        return shortest_path
    except nx.NetworkXNoPath:
        print("No path found between the given stations.")
        return None


shortest_path_nodes = find_shortest_path_by_distance(G1, station_a_name, station_b_name)


if shortest_path_nodes:

    stations_only = [node for node in shortest_path_nodes if G1.nodes[node].get('type') == 'station']


    shortest_path_station_names = [G1.nodes[node]['name'] for node in stations_only]
    print("Shortest path by station names:", shortest_path_station_names)
