import React from 'react';
import StationSelector from './StationSelector';
import Map from './Map';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        RailRouter
      </header>
      <div className="Selectors">
        <StationSelector label="Departing Station" />
        <StationSelector label="Arriving Station" />
      </div>
      <Map />
    </div>
  );
}

export default App;
