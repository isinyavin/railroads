// In App.js
import React, { useState } from 'react';
import StationSelector from './StationSelector';
import Map from './Map';
import './App.css';

function App() {
  const [startStation, setStartStation] = useState('');
  const [destinationStation, setDestinationStation] = useState('');

  const handleFindRoute = () => {
    alert(`Finding route from ${startStation} to ${destinationStation}`);
  };

  return (
    <div className="App">
      <header className="App-header">
        RailRouter
      </header>
      <div className="Content">
        <div className="Selectors">
          <StationSelector label="Start Station" onSelect={setStartStation} selectedStation={startStation} />
          <StationSelector label="Destination Station" onSelect={setDestinationStation} selectedStation={destinationStation} />
        </div>
        <button className="find-route-button" onClick={handleFindRoute}>Find Route</button>
        <div className="MapContainer">
          <Map />
        </div>
      </div>
    </div>
  );
}

export default App;

