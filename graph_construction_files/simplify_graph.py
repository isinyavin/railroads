import networkx as nx
import sqlite3
from shapely.wkt import loads, dumps

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
            G.add_edge(start_node_id, end_node_id, geometry=line)

    conn.close()
    return G

def create_filtered_graph(G, min_size):
    filtered_graph = nx.Graph()
    components = list(nx.connected_components(G))
    
    for component in components:
        if len(component) >= min_size:
            subgraph = G.subgraph(component).copy()
            filtered_graph = nx.compose(filtered_graph, subgraph)
    
    return filtered_graph

def get_station_counts_per_component(G):
    components = list(nx.connected_components(G))
    station_counts_per_component = []

    for component in components:
        station_count = 0
        for node_id in component:
            node_data = G.nodes[node_id]
            if node_data.get('type') == 'station':
                station_count += 1
        station_counts_per_component.append(station_count)

    return station_counts_per_component

def update_db_with_filtered_graph(db_path, filtered_G):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    
    c.execute('SELECT node_id FROM nodes')
    for row in c.fetchall():
        node_id = row[0]
        if node_id not in filtered_G.nodes:
            c.execute('DELETE FROM nodes WHERE node_id = ?', (node_id,))

    
    c.execute('SELECT start_node_id, end_node_id FROM edges')
    for row in c.fetchall():
        start_node_id, end_node_id = row
        if not filtered_G.has_edge(start_node_id, end_node_id):
            c.execute('DELETE FROM edges WHERE start_node_id = ? AND end_node_id = ?', (start_node_id, end_node_id))

    conn.commit()
    conn.close()


G = load_graph_from_db("regional_network_databases/ukgraph2copy.db")


min_size = 200
filtered_G = create_filtered_graph(G, min_size)


station_counts_per_component = get_station_counts_per_component(filtered_G)


for i, count in enumerate(station_counts_per_component):
    if count > 1:
        print(f"Connected component {i} has {count} 'station' nodes.")


update_db_with_filtered_graph("regional_network_databases/ukgraph2copy.db", filtered_G)
