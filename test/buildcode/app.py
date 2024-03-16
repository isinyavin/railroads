from flask import Flask, request, jsonify
import networkx as nx
import pickle
from shapely.geometry import Point, LineString
import geopandas as gpd

app = Flask(__name__)

with open('dublingraph.pkl', 'rb') as file:
    G = pickle.load(file)

@app.route('/find-path', methods=['POST'])
def find_path_route():  
    data = request.json
    start_station = data.get('start_station')
    end_station = data.get('end_station')

    path_info = find_shortest_path(G, start_station, end_station)  
    
    if path_info is None:
        return jsonify({"error": "Path not found or invalid stations"}), 404

    return jsonify(path_info)


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


if __name__ == '__main__':
    app.run(debug=True, port = 5002)


