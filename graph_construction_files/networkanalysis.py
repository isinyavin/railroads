import networkx as nx
import sqlite3
from shapely.wkt import loads


def load_graph_from_db(db_path):
    G = nx.Graph()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('SELECT node_id, x, y, type, name FROM nodes')
    for row in c.fetchall():
        node_id, x, y, type_, name = row
        G.add_node(node_id, pos=(x, y), type=type_, name=name)

    #you can add weight back in later
    c.execute('SELECT start_node_id, end_node_id, geometry FROM edges')
    for row in c.fetchall():
        start_node_id, end_node_id, geometry = row
        if geometry:
            line = loads(geometry)
            G.add_edge(start_node_id, end_node_id, geometry = line)

    conn.close()
    return G

G = load_graph_from_db("regional_network_databases/ukraine_graph.db")
components = list(nx.connected_components(G))

station_counts_per_component = []

for component in components:

    station_count = 0
    
    for node_id in component:
        node_data = G.nodes[node_id]
        if node_data.get('type') == 'station':
            station_count += 1
    
    station_counts_per_component.append(station_count)

for i, count in enumerate(station_counts_per_component):
    if count > 1:
        print(f"Connected component {i} has {count} 'station' nodes.")