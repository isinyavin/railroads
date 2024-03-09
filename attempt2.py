import osmnx as ox
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
import numpy as np
import geopy.distance
import matplotlib.pyplot as plt
from shapely.ops import split, nearest_points


stations_gdf = gpd.read_feather('dublinstation.feather')
rails_gdf = gpd.read_feather('dublinrails.feather')

dublin_bounds = [-6.487438, 53.198744, -6.07804, 53.511396]  

def is_within_bounds(point, bounds):
    x = point.x
    y = point.y
    return bounds[0] <= x <= bounds[2] and bounds[1] <= y <= bounds[3]

G = nx.Graph()

for idx, railway in rails_gdf.iterrows():
    if isinstance(railway.geometry, LineString):
        start_point, end_point = railway.geometry.coords[0], railway.geometry.coords[-1]

        start_node = Point(start_point)
        end_node = Point(end_point)

        start_node_id = f"{start_node.x}_{start_node.y}"
        end_node_id = f"{end_node.x}_{end_node.y}"
        
        if start_node_id not in G and is_within_bounds(start_node, dublin_bounds):
            G.add_node(start_node_id, pos=(start_node.x, start_node.y), type = "rail")
        if end_node_id not in G and is_within_bounds(end_node, dublin_bounds):
            G.add_node(end_node_id, pos=(start_node.x, start_node.y), type = "rail")
        
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

        if is_within_bounds(start_node, dublin_bounds) and is_within_bounds(end_node, dublin_bounds):
            G.add_edge(start_node_id, end_node_id, geometry=railway.geometry, **edge_attributes)


def add_station_to_graph(station, graph, railways_gdf):
    station_point = Point(station.geometry.x, station.geometry.y)
    print(station["name"])
    
    edge_distances = []

    for u, v, data in graph.edges(data=True):
        if 'geometry' in data:
            edge_geom = data['geometry']
            nearest_point = nearest_points(station_point, edge_geom)[1]
            distance = station_point.distance(nearest_point)
            edge_distances.append((distance, (u, v), nearest_point, edge_geom))

    edge_distances.sort(key=lambda x: x[0])
    nearest_edges = edge_distances[:2]

    for dist, (u, v), nearest_point, edge_geom in nearest_edges:
        station_node_id = len(graph) + 1
        connector_id = len(graph) +2
        station_attributes = {
            'name': station['name'],
        }
        graph.add_node(station_node_id, pos=(station_point.x, station_point.y), type = "station", **station_attributes)
        graph.add_node(connector_id, pos=(nearest_point.x, nearest_point.y))

        u_pos = graph.nodes[u]['pos']
        v_pos = graph.nodes[v]['pos']
        edge_to_u_geometry = LineString([station_point, nearest_point])

        print(edge_geom)
        print(nearest_point)

        line = edge_geom
        point =  nearest_point

        nearest_point_on_line, nearest_point = nearest_points(line, point)


        closest_coordinate = min(line.coords, key=lambda coord: Point(coord).distance(nearest_point_on_line))

        print("The closest coordinate on the LineString to the Point is:", closest_coordinate)

        split_geom = split(edge_geom.coords, Point(nearest_point.x, nearest_point.y))
        geom_to_u = split_geom.geoms[0]
        geom_to_v = split_geom.geoms[1]

        graph.add_edge(connector_id, station_node_id, weight=dist, geometry=edge_to_u_geometry)
        graph.add_edge(u, connector_id, geometry = geom_to_u)
        graph.add_edge(v, connector_id, geometry = geom_to_v)
        #graph.remove_edge(u,v)

i =0 
for idx, station in stations_gdf.iterrows():
    i += 1 
    print(f"Station: {station['name']} Count: {i/49*100}")
    add_station_to_graph(station, G, rails_gdf)

pos = nx.get_node_attributes(G, 'pos')
print(list(pos.items())[:5])


def plot_graph(G):
    plt.figure(figsize=(10, 10))
    
    station_nodes = [node for node, data in G.nodes(data=True) if data.get('type') == 'station']
    rail_nodes = [node for node, data in G.nodes(data=True) if data.get('type') != 'station']
    
    pos = nx.get_node_attributes(G, 'pos')
    
    if rail_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=rail_nodes, node_size=20, node_color='blue', alpha=0.5)
    
    if station_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=station_nodes, node_size=30, node_color='red', alpha=0.8)
    

    for u, v, data in G.edges(data=True):
        if 'geometry' in data:
            xs, ys = data['geometry'].xy
            plt.plot(xs, ys, color='black', alpha=0.5)
        else:
            print("alert")
    
    plt.axis('equal')
    plt.axis('off')
    plt.show()

#plot_graph(G)
    
def find_and_plot_path(G, station_name_start, station_name_end):
    station_nodes = {data['name']: node for node, data in G.nodes(data=True) if data.get('type') == 'station'}
    start_node = station_nodes.get(station_name_start)
    end_node = station_nodes.get(station_name_end)
    
    if not start_node or not end_node:
        print("One or both of the stations could not be found.")
        return
    

    shortest_path = nx.shortest_path(G, source=start_node, target=end_node)
    
    plt.figure(figsize=(10, 10))
    

    nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G if G.nodes[node].get('type') != 'station'], node_size=20, node_color='blue', alpha=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G if G.nodes[node].get('type') == 'station'], node_size=30, node_color='red', alpha=0.8)


    for u, v, data in G.edges(data=True):
        if 'geometry' in data:
            xs, ys = data['geometry'].xy
            plt.plot(xs, ys, color='black', alpha=0.5)
        else:
            print("alert")
    
    print(shortest_path)
    for i in range(len(shortest_path)-1):
        u = shortest_path[i]
        v = shortest_path[i+1]
    
        xs, ys = G[u][v]['geometry'].xy
        plt.plot(xs, ys, color='green', linewidth=5, alpha=0.8)
        

 



    plt.axis('equal')
    plt.axis('off')
    plt.show()

find_and_plot_path(G, 'Clondalkin & Fonthill', 'Hansfield')