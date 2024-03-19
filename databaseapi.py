from flask import Flask, jsonify, request, send_file
from sqlalchemy import create_engine, text
from flask_sqlalchemy import SQLAlchemy
import geopandas as gpd
from flask_cors import CORS
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import networkx as nx
from io import BytesIO
import pickle
from shapely.geometry import Point, LineString
import contextily as ctx
from stationrouter import find_route, get_stations_route

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dublingraph.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
CORS(app, origins=["http://localhost:3000"])

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

def generate_graph_image(station_name_start, station_name_end, db_path, margin):
    plt = find_route(station_name_start, station_name_end, db_path, margin)
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0) 
    plt.close('all') 
    return img


with app.app_context():
    db.create_all()

def get_stations_from_db(db_path):
    engine = create_engine(db_path)
    print(db_path)
    with engine.connect() as connection:
        query = text("SELECT name FROM nodes WHERE type = 'station' AND name IS NOT NULL")
        result = connection.execute(query)
        stations = [row._asdict() for row in result]
    return stations


@app.route('/api/route/<string:geography>/<string:depart>/<string:arrive>', methods=["GET"])
def get_route(depart, arrive, geography):
    if geography == "dublin":
        db_path = "dublingraph.db"
        margin = 0.05
    if geography == "uk":
        db_path = "ukgraph2copy.db"
        margin = 1
    if geography == "nyc":
        db_path = "nycsub.db"
        margin = 0.1
    if geography == "france":
        db_path = "frenchrail.db"
        margin = 1
    img = generate_graph_image(depart, arrive, db_path, margin)
    return send_file(img, mimetype='image/png')

@app.route('/api/route/details/<string:geography>/<string:depart>/<string:arrive>', methods=["GET"])
def get_route_details(depart, arrive, geography):
    if geography == "dublin":
        db_path = "dublingraph.db"
    if geography == "uk":
        db_path = "ukgraph2copy.db"
    stations = get_stations_route(depart, arrive, db_path)
    return jsonify(stations)


@app.route('/api/stations/<string:name>', methods=['GET'])
def get_station_by_name(name):
    station = Station.query.filter_by(name=name).first()
    if station:
        return jsonify(station.to_dict())
    else:
        return jsonify({"error": "Station not found"}), 404

@app.route('/api/<string:geography>/stations', methods=['GET'])
def get_stations(geography):
    GEOGRAPHY_DATABASE_MAP = {
        'dublin': 'sqlite:///dublingraph.db',
        'uk': 'sqlite:///ukgraph2copy.db'
    }

    db_path = GEOGRAPHY_DATABASE_MAP.get(geography.lower())
    if db_path is None:
        return jsonify({"error": f"No database found for geography: {geography}"}), 404

    stations = get_stations_from_db(db_path)
    return jsonify(stations)

if __name__ == '__main__':
    app.run(debug=True)
