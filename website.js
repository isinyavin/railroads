// In src/App.js

import React from 'react';
import StationSelector from './components/StationSelector';
import Map from './components/Map';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        Train Route Finder
      </header>
      <div className="Selectors">
        <StationSelector label="Start Station" />
        <StationSelector label="Destination Station" />
      </div>
      <Map />
    </div>
  );
}

export default App;

// In src/components/StationSelector.js

import React from 'react';

function StationSelector({ label }) {
  return (
    <div>
      <label>{label}</label>
      <select>
        {/* Options will be populated here */}
      </select>
    </div>
  );
}

export default StationSelector;

// In src/components/Map.js

import React from 'react';
import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';

function Map() {
  return (
    <MapContainer center={[53.350140, -6.266155]} zoom={13} scrollWheelZoom={false}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {/* Markers and Polylines will be added here */}
    </MapContainer>
  );
}

export default Map;
