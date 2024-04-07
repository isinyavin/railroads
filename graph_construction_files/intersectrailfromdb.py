import networkx as nx
from shapely.geometry import LineString, Point
from shapely.ops import unary_union, split
from shapely.strtree import STRtree
import sqlite3
import geopandas as gpd
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
from rtree import index
from shapely.strtree import STRtree

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
        start_node_id, end_node_id, geometry= row
        if geometry:
            line = geometry
            G.add_edge(start_node_id, end_node_id, geometry = line)

    conn.close()
    return G

def process_edges_for_intersections(G):
    intersections_to_add = []
    edges_to_remove = []
    edges_to_add = []
    i=1
    for (u1, v1, data1) in G.edges(data=True):
        if 'geometry' in data1:
            geom1 = loads(data1['geometry'])
            for (u2, v2, data2) in G.edges(data=True):
                if 'geometry' in data2 and (u1, v1) != (u2, v2):
                    geom2 = loads(data2['geometry'])
                    if geom1.intersects(geom2):
                        intersection = geom1.intersection(geom2)
                        if isinstance(intersection, Point):
                            intersection_id = f"intersection_{intersection.x}_{intersection.y}"
                            intersections_to_add.append((intersection_id, (intersection.x, intersection.y)))
                            edges_to_remove.append((u1, v1))
                            edges_to_remove.append((u2, v2))
                            print(i)
                            i+=1

    for node_id, pos in intersections_to_add:
        G.add_node(node_id, pos=pos, type='intersection')
    
    #for u, v in edges_to_remove:
        #G.remove_edge(u, v)
    
    #for u, v, attributes in edges_to_add:
        #G.add_edge(u, v, **attributes)


G = load_graph_from_db("ukgraph_updated copy.db")

process_edges_for_intersections(G)
