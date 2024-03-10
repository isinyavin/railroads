from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_stations_database.db'
db = SQLAlchemy(app)

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

@app.route('/api/stations', methods=['GET'])
def get_stations():
    stations = Station.query.all()
    return jsonify([station.to_dict() for station in stations])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5011)
