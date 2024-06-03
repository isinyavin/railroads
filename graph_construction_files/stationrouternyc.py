from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
import geopandas as gpd
from flask_cors import CORS
import matplotlib.pyplot as plt
import networkx as nx
from io import BytesIO
import pickle
from shapely.geometry import Point, LineString
import contextily as ctx
import sqlite3
from shapely.wkt import loads
import numpy as np

def find_bounds_stations(stations):
    if not stations:
        return None  

    all_x = [station.x for station in stations]
    all_y = [station.y for station in stations]

    all_x_array = np.array(all_x)
    all_y_array = np.array(all_y)

    minx = np.min(all_x_array)
    miny = np.min(all_y_array)
    maxx = np.max(all_x_array)
    maxy = np.max(all_y_array)

    return minx, miny, maxx, maxy

def load_graph_from_db(db_path):
    G = nx.Graph()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('SELECT node_id, x, y, type, name FROM nodes')
    for row in c.fetchall():
        node_id, x, y, type_, name = row
        G.add_node(node_id, pos=(x, y), type=type_, name=name)

    c.execute('SELECT start_node_id, end_node_id, geometry FROM edges')
    for row in c.fetchall():
        start_node_id, end_node_id, geometry = row
        if geometry:
            line = loads(geometry)
            G.add_edge(start_node_id, end_node_id, geometry = line)

    conn.close()
    return G

def find_route(station_name_start, station_name_end):
    fig, ax = plt.subplots(figsize=(10, 10))
    G = load_graph_from_db("nyclines_efficient.db")
    station_nodes = {data['name']: node for node, data in G.nodes(data=True) if data.get('type') == 'station'}
    start_node = station_nodes.get(station_name_start)
    end_node = station_nodes.get(station_name_end)
    plot_graph(G)
    
    if not start_node or not end_node:
        print("One or both of the stations could not be found.")
        return

    shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')

    line_geom = [LineString([G.nodes[u]['pos'], G.nodes[v]['pos']]) for u, v in zip(shortest_path[:-1], shortest_path[1:])]
    gdf_path = gpd.GeoDataFrame(geometry=line_geom, crs='epsg:4326')

    path_union = gdf_path.unary_union

    stations_within_distance = []
    for node, data in G.nodes(data=True):
        if data.get('type') == 'station':
            station_point = Point(data['pos'])
            if path_union.distance(station_point) <= 0.005:
                stations_within_distance.append(station_point)

    bounds = find_bounds_stations(stations_within_distance)
    if bounds:
        minx, miny, maxx, maxy = bounds
        margin = 1 
        plt.xlim(minx - margin, maxx + margin)
        plt.ylim(miny - margin, maxy + margin)

    gdf_path.plot(ax=ax, color='green', linewidth=3, zorder=2)
    
    if stations_within_distance:
        gdf_stations = gpd.GeoDataFrame(geometry=stations_within_distance, crs='epsg:4326')
        gdf_stations.plot(ax=ax, color='red', markersize=20, zorder=3, alpha=0.8)
        start_node_geom = Point(G.nodes[start_node]['pos'])  
        gdf_start_node = gpd.GeoDataFrame(geometry=[start_node_geom], crs='epsg:4326')

        gdf_start_node.plot(ax=ax, color='blue', markersize=100, zorder=3, alpha=0.8)
        end_node_geom = Point(G.nodes[end_node]['pos'])  
        gdf_end_node = gpd.GeoDataFrame(geometry=[end_node_geom], crs='epsg:4326')

        gdf_end_node.plot(ax=ax, color='blue', markersize=100, zorder=3, alpha=0.8)
        y_offset = 0.1  
        background_padding = dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="none", alpha=0.6)  

        ax.text(start_node_geom.x, start_node_geom.y + y_offset, station_name_start, 
                horizontalalignment='center', verticalalignment='center', 
                color='black', fontsize=12, weight='bold', bbox=background_padding)

        ax.text(end_node_geom.x, end_node_geom.y + y_offset, station_name_end, 
                horizontalalignment='center', verticalalignment='center', 
                color='black', fontsize=12, weight='bold', bbox=background_padding)

    ctx.add_basemap(ax, crs=gdf_path.crs.to_string(), source=ctx.providers.Esri.WorldStreetMap)
    plt.axis('off')

    plt.show()

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


G = load_graph_from_db("regional_network_databases/ukraine_graph.db")
plot_graph(G)