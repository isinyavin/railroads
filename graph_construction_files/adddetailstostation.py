import sqlite3
import reverse_geocoder as rg

conn = sqlite3.connect('belgium_graph.db')
cursor = conn.cursor()

cursor.execute("SELECT node_id, x, y FROM nodes WHERE type='station'")
stations = cursor.fetchall()

cursor.execute("ALTER TABLE nodes ADD COLUMN admin1 TEXT")
cursor.execute("ALTER TABLE nodes ADD COLUMN admin2 TEXT")
cursor.execute("ALTER TABLE nodes ADD COLUMN country TEXT")

def get_location_info(coordinates):
    results = rg.search(coordinates, mode = 1)
    return {
        'admin1': results[0]['admin1'],
        'admin2': results[0]['admin2'],
        'cc': results[0]['cc']
    }

for station in stations:
    node_id, x, y = station
    location_info = get_location_info((y, x)) 
    cursor.execute("""
        UPDATE nodes
        SET admin1 = ?,
            admin2 = ?,
            country = ?
        WHERE node_id = ?
    """, (location_info['admin1'], location_info['admin2'], location_info['cc'], node_id))

conn.commit()
conn.close()
