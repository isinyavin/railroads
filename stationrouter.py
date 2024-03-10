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

def find_route(station_name_start, station_name_end):
    fig, ax = plt.subplots(figsize=(10, 10))
    with open('dublingraph.pkl', 'rb') as file:
        G = pickle.load(file)
    station_nodes = {data['name']: node for node, data in G.nodes(data=True) if data.get('type') == 'station'}
    start_node = station_nodes.get(station_name_start)
    end_node = station_nodes.get(station_name_end)
    
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

    gdf_path.plot(ax=ax, color='green', linewidth=3, zorder=2)
    
    if stations_within_distance:
        gdf_stations = gpd.GeoDataFrame(geometry=stations_within_distance, crs='epsg:4326')
        gdf_stations.plot(ax=ax, color='red', markersize=50, zorder=3, alpha=0.8)

    ctx.add_basemap(ax, crs=gdf_path.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

    return plt