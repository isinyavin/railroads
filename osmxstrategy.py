import osmnx as ox
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
import numpy as np
import geopy.distance
import matplotlib.pyplot as plt




stations_gdf = gpd.read_feather('dublinstation.feather')
rails_gdf = gpd.read_feather('dublinrails.feather')



ox.config(use_cache=True, log_console=True)
custom_filter = '["railway"~"rail"]'


G1= ox.graph_from_place('Dublin', custom_filter=custom_filter, network_type='all')




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
    # Find the nearest edges (returns the closest edge by default)
    nearest_edge = ox.distance.nearest_edges(G, X=station_point.x, Y=station_point.y, return_dist=False)
    u1, v1, key1 = nearest_edge
    nearest_edges =[]
    nearest_edges.append(nearest_edge)
    G.remove_edge(u1, v1, key1)
    nearest_edge2 = ox.distance.nearest_edges(G, X=station_point.x, Y=station_point.y, return_dist=False)
    nearest_edges.append(nearest_edge2)
    G.add_edge(u1,v1,key1)
    print(nearest_edges)
    # Initialize a list to store the new station nodes
    new_station_nodes = []

    for edge in nearest_edges:
        u, v, key = edge
        
        edge_geom = G[u][v][key]['geometry'] if 'geometry' in G[u][v][key] else LineString([Point(G.nodes[u]['x'], G.nodes[u]['y']), Point(G.nodes[v]['x'], G.nodes[v]['y'])])
        nearest_point_on_edge = nearest_points(edge_geom, station_point)[0]
        
        # Create a new station node
        station_node = max(G.nodes()) + 1 
        G.add_node(station_node, x=nearest_point_on_edge.x, y=nearest_point_on_edge.y, **station_attributes)
        new_station_nodes.append(station_node)

        # Store the original edge attributes
        dictionary_vals = G[u][v][key].copy()

        # Remove the original edge
        G.remove_edge(u, v, key)

        # Add new edges from the existing nodes to the new station node
        G.add_edge(u, station_node, **dictionary_vals)
        G.add_edge(station_node, v, **dictionary_vals)

    # After inserting the station into the nearest and second nearest edges,
    # connect the two new station nodes with an edge
    if len(new_station_nodes) == 2:
        # You might want to define attributes for this new connecting edge
        connecting_edge_attrs = {
            'type': 'station_connection',
            # Any other attributes...
        }
        G.add_edge(new_station_nodes[0], new_station_nodes[1], **connecting_edge_attrs)

    return new_station_nodes  # Optionally return the IDs of the new station nodes


initial_edge_count = G1.number_of_edges()
print(f"Initial number of edges in the graph: {initial_edge_count}")

for idx, station in stations_gdf.iterrows():
    station_point = Point(station.geometry.x, station.geometry.y)
    station_attributes = {
       'name': station['name'],
       'type': 'station',
       'color' :'red'
    }
    insert_station_into_nearest_edge(G1, station_point, station_attributes)

final_edge_count = G1.number_of_edges()
print(f"Final number of edges in the graph: {final_edge_count}")


for node, data in G1.nodes(data=True):
    if data.get('type') == 'station':
        print(data.get('name'))
    else:
        data['color'] = 'blue'

node_colors = [data['color'] for node, data in G1.nodes(data=True)]

# Now plot the graph using OSMnx, passing the node_colors list
#fig, ax = ox.plot_graph(G1, node_color=node_colors, node_size=30, edge_linewidth=1, edge_color='gray')

G1 = G1.to_undirected()

# Now plot the graph using OSMnx, passing the node_colors list
#fig, ax = ox.plot_graph(G1, node_color=node_colors, node_size=30, edge_linewidth=1, edge_color='gray')

def get_station_node_id(G, station_name):
    for node, data in G.nodes(data=True):
        if data.get('type') == 'station' and data.get('name') == station_name:
            print(data.get('name'))
            return node
    return None

station_a_name = "Broombridge"
station_b_name = "Harmonstown"


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
print(shortest_path_nodes)

if shortest_path_nodes:

    stations_only = [node for node in shortest_path_nodes if G1.nodes[node].get('type') == 'station']
    print(len(stations_only))


    shortest_path_station_names = [G1.nodes[node]['name'] for node in stations_only]
    print("Shortest path by station names:", shortest_path_station_names)


print(len(G1.nodes(data = True)))
# Correct way to filter and count station nodes
station_nodes_count = sum(1 for node, data in G1.nodes(data=True) if data.get('type') == 'station')
print(f"Number of station nodes: {station_nodes_count}")

# Assume 'node_id' is the ID of the node you're interested in
node_id = get_station_node_id(G1, "Ashtown")  

# Print edge attributes for all edges adjacent to 'node_id'
for u, v, attrs in G1.edges(node_id, data=True):
    print(f"Edge between {u} and {v} has attributes: {attrs}")


