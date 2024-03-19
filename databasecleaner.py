import sqlite3

conn = sqlite3.connect('frenchrail.db')  
cursor = conn.cursor()

try:
    cursor.execute("SELECT node_id FROM nodes WHERE type='station'")
    station_nodes = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT DISTINCT start_node_id FROM edges")
    edge_start_nodes = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT DISTINCT end_node_id FROM edges")
    edge_end_nodes = {row[0] for row in cursor.fetchall()}

    edge_node_ids = edge_start_nodes.union(edge_end_nodes)

    unconnected_stations = station_nodes.difference(edge_node_ids)

    for node_id in unconnected_stations:
        cursor.execute("DELETE FROM nodes WHERE node_id=?", (node_id,))
        print(node_id)

    conn.commit()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    conn.close()