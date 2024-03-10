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
      <div className="Content">
        <div className="Selectors">
          {/* Your selectors here */}
          <StationSelector label="Start Station" />
          <StationSelector label="Destination Station" />
        </div>
        <div className="MapContainer">
          <Map />
        </div>
      </div>
    </div>
  );
}


export default App;
