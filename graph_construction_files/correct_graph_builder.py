import osmnx as ox
import geopandas as gpd
import contextily as ctx
import networkx as nx
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points, split, snap
import numpy as np
import geopy.distance
import matplotlib.pyplot as plt
from shapely.ops import split, nearest_points
import pickle
import sqlite3
from shapely.ops import unary_union, split
from shapely.strtree import STRtree
from rtree import index

conn = sqlite3.connect('ukraine_graph.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS nodes
             (node_id TEXT PRIMARY KEY, x REAL, y REAL, type TEXT, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS edges
             (edge_id INTEGER PRIMARY KEY AUTOINCREMENT, start_node_id TEXT, end_node_id TEXT,
              geometry TEXT)''')  
conn.commit()

rails_gdf = gpd.read_file('geojson files/ukraine_lines.geojson')
stations_gdf = gpd.read_file('geojson files/ukraine_stations.geojson')

#dublin_bounds = [-6.587438, 53.098744, -6.00804, 54.511396]  

#def is_within_bounds(point, bounds):
    #x = point.x
    #y = point.y
    #return bounds[0] <= x <= bounds[2] and bounds[1] <= y <= bounds[3]

G = nx.Graph()


def add_and_split_railways3(graph, railway, edge_attributes):
    # Create an R-tree index for existing edges
    idx = index.Index()
    for i, (u, v, data) in enumerate(graph.edges(data=True)):
        if 'geometry' in data:
            geom = data['geometry']
            idx.insert(i, geom.bounds)

    new_railway_geom = railway.geometry

    # Query the R-tree index for candidates that might intersect with the new railway
    candidate_ids = list(idx.intersection(new_railway_geom.bounds))
    candidate_geoms = [data['geometry'] for i, (_, _, data) in enumerate(graph.edges(data=True)) if i in candidate_ids]

    if len(candidate_geoms) > 0:
        combined_candidates_geom = unary_union(candidate_geoms)
        if combined_candidates_geom.intersects(new_railway_geom):
            split_geoms = split(new_railway_geom, combined_candidates_geom)
        else:
            split_geoms = [new_railway_geom]
    else:
        split_geoms = [new_railway_geom]

    for split_geom in split_geoms:
        start_point, end_point = split_geom.coords[0], split_geom.coords[-1]
        start_node_id = f"{start_point[0]}_{start_point[1]}"
        end_node_id = f"{end_point[0]}_{end_point[1]}"

        if start_node_id not in graph:
            graph.add_node(start_node_id, pos=start_point, type="rail")
        if end_node_id not in graph:
            graph.add_node(end_node_id, pos=end_point, type="rail")

        if not graph.has_edge(start_node_id, end_node_id):
            graph.add_edge(start_node_id, end_node_id, geometry=split_geom, **edge_attributes)



def add_and_split_railways2(graph, railway, edge_attributes):
    edge_geometries = [data['geometry'] for _, _, data in graph.edges(data=True) if 'geometry' in data]
    spatial_index = STRtree(edge_geometries)

    new_railway_geom = railway.geometry

    candidate_geoms = spatial_index.query(new_railway_geom)
    candidate_geoms = [geom for geom in candidate_geoms if isinstance(geom, (LineString, Point))]

    if len(candidate_geoms) > 0:
        combined_candidates_geom = unary_union(candidate_geoms)
        if combined_candidates_geom.intersects(new_railway_geom):
            split_geoms = split(new_railway_geom, combined_candidates_geom)
        else:
            split_geoms = [new_railway_geom]
    else:
        split_geoms = [new_railway_geom]

    for split_geom in split_geoms:
        start_point, end_point = split_geom.coords[0], split_geom.coords[-1]
        start_node_id = f"{start_point[0]}_{start_point[1]}"
        end_node_id = f"{end_point[0]}_{end_point[1]}"

        if start_node_id not in graph:
            graph.add_node(start_node_id, pos=start_point, type="rail")
        if end_node_id not in graph:
            graph.add_node(end_node_id, pos=end_point, type="rail")

        if not graph.has_edge(start_node_id, end_node_id):
            graph.add_edge(start_node_id, end_node_id, geometry=split_geom, **edge_attributes)



def add_and_split_railways(graph, railway, edge_attributes):
    new_railway_geom = railway.geometry
    all_edges_geom = [data['geometry'] for u, v, data in graph.edges(data=True) if 'geometry' in data]
    combined_edges_geom = unary_union(all_edges_geom + [new_railway_geom])

    if not combined_edges_geom.is_simple:
        split_geoms = split(new_railway_geom, combined_edges_geom)
    else:
        split_geoms = [new_railway_geom]

    for split_geom in split_geoms:
        start_point, end_point = split_geom.coords[0], split_geom.coords[-1]
        start_node_id = f"{start_point[0]}_{start_point[1]}"
        end_node_id = f"{end_point[0]}_{end_point[1]}"

        if start_node_id not in graph:
            graph.add_node(start_node_id, pos=start_point, type="rail")
        if end_node_id not in graph:
            graph.add_node(end_node_id, pos=end_point, type="rail")

        if not graph.has_edge(start_node_id, end_node_id):
            graph.add_edge(start_node_id, end_node_id, geometry=split_geom, **edge_attributes)
"""
i = 1
for idx, railway in rails_gdf.iterrows():
    print(f"Processed {i} edges")
    if isinstance(railway.geometry, LineString):
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
        add_and_split_railways3(G, railway, edge_attributes)
        i += 1
"""




for idx, railway in rails_gdf.iterrows():
    if isinstance(railway.geometry, LineString):
        start_point, end_point = railway.geometry.coords[0], railway.geometry.coords[-1]

        start_node = Point(start_point)
        end_node = Point(end_point)

        start_node_id = f"{start_node.x}_{start_node.y}"
        end_node_id = f"{end_node.x}_{end_node.y}"
        
        if start_node_id not in G:
            G.add_node(start_node_id, pos=(start_node.x, start_node.y), type = "rail")
        if end_node_id not in G:
            G.add_node(end_node_id, pos=(end_node.x, end_node.y), type = "rail")
        
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

        if G.has_edge(start_node, end_node) == False:
            G.add_edge(start_node_id, end_node_id, geometry=railway.geometry, **edge_attributes)
distances = []


def add_station_to_graph(station, graph, railways_gdf):
    
    station_point = Point(station.geometry.x, station.geometry.y)

    edge_distances = []

    for u, v, data in graph.edges(data=True):
        if 'geometry' in data:
            edge_geom = data['geometry']
            nearest_point = nearest_points(station_point, edge_geom)[1]
            distance = station_point.distance(nearest_point)
            edge_distances.append((distance, (u, v), nearest_point, edge_geom))

    edge_distances.sort(key=lambda x: x[0])
    nearest_edges = edge_distances[:2]
    station_node_id = f"{station_point.x}_{station_point.y}"
    station_attributes = {
        'name': station['name'],
    }
    if 'station' in station and station['station'] == 'subway':
        station_attributes['subway'] = True

    graph.add_node(station_node_id, pos=(station_point.x, station_point.y), type = "station", **station_attributes)

    for dist, (u, v), nearest_point, edge_geom in nearest_edges:
        connector_id = f"{nearest_point.x}_{nearest_point.y}"
        if connector_id == station_node_id:
            continue

        if dist > 0.01:
            continue
        graph.add_node(connector_id, pos=(nearest_point.x, nearest_point.y))

        u_pos = graph.nodes[u]['pos']
        v_pos = graph.nodes[v]['pos']
        edge_to_u_geometry = LineString([station_point, nearest_point])

        line = edge_geom
        point =  nearest_point

        nearest_point_on_line, nearest_point2 = nearest_points(line, point)

        closest_coordinate = min(line.coords, key=lambda coord: Point(coord).distance(nearest_point_on_line))
        closest_point_geometry = Point(closest_coordinate)

        split_geom = split(line, closest_point_geometry)

        i = 0 
        if len(split_geom.geoms) == 2:
            geom_to_u = split_geom.geoms[0]
            geom_to_v = split_geom.geoms[1]
            #print("Split successful")
            x,y = nearest_point.x, nearest_point.y
            geom_to_u = LineString(list(geom_to_u.coords) + [(x,y)])
            geom_to_v = LineString([(x,y)]+ list(geom_to_v.coords)[1:])
            #print(geom_to_u)
            #print(geom_to_v)
        else:
            i+=1
            u_pos = graph.nodes[u]['pos']
            v_pos = graph.nodes[v]['pos']
            geom_to_u = LineString([u_pos, nearest_point])
            geom_to_v = LineString([nearest_point, v_pos])
        
        graph.add_edge(connector_id, station_node_id, geometry=edge_to_u_geometry)
        graph.add_edge(u, connector_id, geometry = geom_to_u)
        graph.add_edge(connector_id, v, geometry = geom_to_v)

        #graph.remove_edge(u,v)
        #if graph.has_edge(u,v):
            #return exit(1)
        

def add_station_to_graph2(station, graph, railways_gdf, railways_gdf_sindex):
    station_point = Point(station.geometry.x, station.geometry.y)
    buffer_distance = 0.01 
    buffered_point = station_point.buffer(buffer_distance)

    possible_matches_index = list(railways_gdf_sindex.intersection(buffered_point.bounds))
    possible_matches = railways_gdf.iloc[possible_matches_index]

    nearest_edges = []
    for _, edge in possible_matches.iterrows():
        edge_geom = edge.geometry
        _, nearest_point_on_edge = nearest_points(station_point, edge_geom)
        distance = station_point.distance(nearest_point_on_edge)
        nearest_edges.append({
            'edge': edge,
            'distance': distance,
            'nearest_point_on_edge': nearest_point_on_edge,
            'start_coord': edge_geom.coords[0],
            'end_coord': edge_geom.coords[-1]
    })
    
    station_point = Point(station.geometry.x, station.geometry.y)

    nearest_edges.sort(key=lambda x: x['distance'])
    nearest_edges = nearest_edges[:2]

    station_node_id = f"{station_point.x}_{station_point.y}"
    station_attributes = {
        'name': station['name'],
    }
    if 'station' in station and station['station'] == 'subway':
        station_attributes['subway'] = True

    graph.add_node(station_node_id, pos=(station_point.x, station_point.y), type = "station", **station_attributes)

    for edge in nearest_edges:
        connector_id = f"{edge['nearest_point_on_edge'].x}_{edge['nearest_point_on_edge'].y}"
        if connector_id == station_node_id:
            continue

        if distance > 0.01:
            continue
        graph.add_node(connector_id, pos=(edge['nearest_point_on_edge'].x, edge['nearest_point_on_edge'].y))

        u_pos = edge['start_coord']
        v_pos = edge['end_coord']
        edge_to_u_geometry = LineString([station_point, edge['nearest_point_on_edge']])

        line = edge_geom
        point =  edge['nearest_point_on_edge']

        nearest_point_on_line, nearest_point2 = nearest_points(line, point)

        closest_coordinate = min(line.coords, key=lambda coord: Point(coord).distance(nearest_point_on_line))
        closest_point_geometry = Point(closest_coordinate)

        split_geom = split(line, closest_point_geometry)

        i = 0 
        if len(split_geom.geoms) == 2:
            geom_to_u = split_geom.geoms[0]
            geom_to_v = split_geom.geoms[1]
            #print("Split successful")
            x,y = edge['nearest_point_on_edge'].x, edge['nearest_point_on_edge'].y
            geom_to_u = LineString(list(geom_to_u.coords) + [(x,y)])
            geom_to_v = LineString([(x,y)]+ list(geom_to_v.coords)[1:])
            #print(geom_to_u)
            #print(geom_to_v)
        else:
            i+=1
            u_pos = edge['start_coord']
            v_pos = edge['end_coord']
            geom_to_u = LineString([u_pos, edge['nearest_point_on_edge']])
            geom_to_v = LineString([edge['nearest_point_on_edge'], v_pos])
        
        u = f"{edge['start_coord'][0]}_{edge['start_coord'][1]}"
        v = f"{edge['end_coord'][0]}_{edge['end_coord'][1]}"
        graph.add_edge(connector_id, station_node_id, geometry=edge_to_u_geometry)
        graph.add_edge(u, connector_id, geometry = geom_to_u)
        graph.add_edge(connector_id, v, geometry = geom_to_v)

        #graph.remove_edge(u,v)
        #if graph.has_edge(u,v):
            #return exit(1)

railways_gdf_sindex = rails_gdf.sindex
i =0 
for idx, station in stations_gdf.iterrows():
    i += 1 
    print(f"Station: {station['name']} Count: {i/3621*100}")
    add_station_to_graph2(station, G, rails_gdf, railways_gdf_sindex)

pos = nx.get_node_attributes(G, 'pos')





def plot_graph(G):
    plt.figure(figsize=(10, 10))
    
    station_nodes = [node for node, data in G.nodes(data=True) if data.get('type') == 'station']
    print(station_nodes)
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


    

def calculate_distance(coords):
    """Calculate the distance of a LineString using its coordinates."""
    if len(coords) > 1:
        return sum(geopy.distance.geodesic(coords[i], coords[i+1]).meters for i in range(len(coords) - 1))
    else:
        return 0

    for u, v, data in G.edges(data=True):
        if 'geometry' in data:
            edge_length = calculate_distance(list(data['geometry'].coords))
            G[u][v]['weight'] = edge_length


for node_id, data in G.nodes(data=True):
    c.execute('''INSERT INTO nodes (node_id, x, y, type, name) VALUES (?, ?, ?, ?, ?)''',
               (node_id, data['pos'][0], data['pos'][1], data.get('type', None), data.get('name', None)))
conn.commit()


for u, v, data in G.edges(data=True):
    geometry_wkt = data['geometry'].wkt if 'geometry' in data else None
    c.execute('''INSERT INTO edges (start_node_id, end_node_id, geometry)
                 VALUES (?, ?, ?)''', (u, v, geometry_wkt))
conn.commit()

conn.close()





def find_and_plot_path(G, station_name_start, station_name_end, ax):
    station_nodes = {data['name']: node for node, data in G.nodes(data=True) if data.get('type') == 'station'}
    start_node = station_nodes.get(station_name_start)
    end_node = station_nodes.get(station_name_end)
    
    if not start_node or not end_node:
        print("One or both of the stations could not be found.")
        return
    

    shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
    edge_list = list(zip(shortest_path[:-1], shortest_path[1:]))

    line_geom = [LineString([G.nodes[u]['pos'], G.nodes[v]['pos']]) for u, v in zip(shortest_path[:-1], shortest_path[1:])]
    gdf_path = gpd.GeoDataFrame(geometry=line_geom, crs='epsg:4326')

    path_union = gdf_path.unary_union
    
    stations_within_distance = []
    for node, data in G.nodes(data=True):
        if data.get('type') == 'station':
            station_point = Point(data['pos'])
            if path_union.distance(station_point) <= 0.005:
                stations_within_distance.append(station_point)


    gdf_path.plot(ax=ax, color='green', linewidth=3, zorder=2)
    
    if stations_within_distance:
        gdf_stations = gpd.GeoDataFrame(geometry=stations_within_distance, crs='epsg:4326')
        gdf_stations.plot(ax=ax, color='red', markersize=50, zorder=3, alpha=0.8)


    ctx.add_basemap(ax, crs=gdf_path.crs.to_string(), source=ctx.providers.CartoDB.Positron)


    ax.axis('off')
    
    plt.show()


    """
    plt.figure(figsize=(10, 10))
    

    #nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G if G.nodes[node].get('type') != 'station'], node_size=20, node_color='blue', alpha=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G if G.nodes[node].get('type') == 'station'], node_size=30, node_color='red', alpha=0.8)


    for u, v, data in G.edges(data=True):
        if 'geometry' in data:
            xs, ys = data['geometry'].xy
            plt.plot(xs, ys, color='black', alpha=0.5)
        else:
            print("alert")
    
    coords = []
    #nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='green', width=5)

    
    for i in range(len(shortest_path)-1):
        u = shortest_path[i]
        v = shortest_path[i+1]

        #if 'geometry' in G[u][v]:  # Ensure geometry exists for this edge
        xs, ys = G[u][v]['geometry'].xy
        print(xs)
        print(ys)
        coords.extend(list(zip(xs, ys)))  # Store coordinates for any further use
        plt.plot(xs, ys, color='green', linewidth=5, alpha=0.8)

    output_file_path = 'coords.txt'
    # Open the file for writing
    with open(output_file_path, 'w') as file:
        for coord in coords:
        # Write each coordinate to the file, formatted as x, y
            file.write(f"{coord[0]}, {coord[1]}\n")


    plt.axis('equal')
    plt.axis('off')
    plt.show()
    """






def find_shortest_path(G, station_name_start, station_name_end):
    station_nodes = {data['name']: node for node, data in G.nodes(data=True) if data.get('type') == 'station'}
    start_node = station_nodes.get(station_name_start)
    end_node = station_nodes.get(station_name_end)

    if not start_node or not end_node:
        return {"message": "One or both of the stations could not be found."}

    shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
    line_geom = [LineString([G.nodes[u]['pos'], G.nodes[v]['pos']]) for u, v in zip(shortest_path[:-1], shortest_path[1:])]
    gdf_path = gpd.GeoDataFrame(geometry=line_geom, crs='epsg:4326')
    return {"path": gdf_path}

#print(find_shortest_path(G, 'Adamstown', 'Howth'))