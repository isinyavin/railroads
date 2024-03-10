from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import geopandas as gpd
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
CORS(app, origins=["http://localhost:3001"])

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

def setup_database():
    db.create_all()

    stations_gdf = gpd.read_feather('feather_files/dublinstation.feather')
    
    for index, row in stations_gdf.iterrows():
        point = row['geometry']
        lat, lon = point.y, point.x
        station = Station(name=row['name'], latitude=lat, longitude=lon)
        db.session.add(station)
    
    db.session.commit()

@app.route('/api/stations/<string:name>', methods=['GET'])
def get_station_by_name(name):
    station = Station.query.filter_by(name=name).first()
    if station:
        return jsonify(station.to_dict())
    else:
        return jsonify({"error": "Station not found"}), 404

@app.route('/api/stations', methods=['GET'])
def get_stations():
    stations = Station.query.all()
    return jsonify([station.to_dict() for station in stations])

if __name__ == '__main__':
    with app.app_context():
        setup_database()
    app.run(debug=True, port = 5002)
