// In App.js
import React, { useState } from 'react';
import StationSelector from './StationSelector';
import Map from './Map';
import './App.css';

function App() {
  const [startStation, setStartStation] = useState('');
  const [destinationStation, setDestinationStation] = useState('');
  const [routeImage, setRouteImage] = useState(null); 

  const handleFindRoute = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5002/api/route/${startStation}/${destinationStation}`);
      if (response.ok) {
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        setRouteImage(imageUrl); // Update state with the route image URL
      } else {
        alert('Failed to find the route. Please try again.');
      }
    } catch (error) {
      console.error('Error fetching route:', error);
      alert('Error fetching the route. Please check your connection and try again.');
    }
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
          {/* Now routeImage is defined and passed correctly */}
          <Map routeImage={routeImage} /> 
        </div>
      </div>
    </div>
  );
}

export default App;

