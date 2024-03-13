import sqlite3
import geopandas as gpd
from sqlalchemy import create_engine

stations_gdf = gpd.read_feather('feather_files/dublinstation.feather')

conn = sqlite3.connect('my_stations_database.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    latitude REAL,
    longitude REAL
);
''')

for index, row in stations_gdf.iterrows():
    point = row['geometry']
    lat, long = point.y, point.x  

    cursor.execute('''
    INSERT INTO stations (name, latitude, longitude) 
    VALUES (?, ?, ?)
    ''', (row['name'], lat, long))

    conn.commit()

conn.commit()

conn.close()