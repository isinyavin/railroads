import sqlite3
import geopy.distance

conn = sqlite3.connect('ukraine_graph.db')
cursor = conn.cursor()

cursor.execute("SELECT edge_id, geometry FROM edges")
edges = cursor.fetchall()

def calculate_distance(wkt_linestring):
    coords = wkt_linestring.replace('LINESTRING (', '').replace(')', '').split(', ')
    coords = [tuple(map(float, coord.split()))[::-1] for coord in coords]
    point1, point2 = coords[0], coords[-1]
    return geopy.distance.geodesic(point1, point2).meters


cursor.execute("ALTER TABLE edges ADD COLUMN weight REAL")

for edge in edges:
    edge_id, geometry = edge
    distance = calculate_distance(geometry)
    cursor.execute("UPDATE edges SET weight = ? WHERE edge_id = ?", (distance, edge_id))

conn.commit()
conn.close()
