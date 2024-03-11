// In App.js
import React, { useState} from 'react';
import StationSelector from './StationSelector';
import Map from './Map';
import './App.css';
import SearchBar from "./SearchBar"

function App() {
  const [startStation, setStartStation] = useState('');
  const [destinationStation, setDestinationStation] = useState('');
  const [routeImage, setRouteImage] = useState(null); 


  const handleFindRoute = async () => {
    try {
      const response = await fetch(`https://railroads.onrender.com/api/route/${startStation}/${destinationStation}`);
      if (response.ok) {
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        setRouteImage(imageUrl);
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
        {/* Wrap the selectors and the button in an additional div */}
        <div className="Selectors-wrapper">
          <div className="Selectors">
            <SearchBar placeholder="Enter Departure Station" onSelect={setStartStation} selectedStation={startStation}/>
            <SearchBar placeholder="Enter Destination Station" onSelect={setDestinationStation} selectedStation={destinationStation} />
          </div>
          <button className="find-route-button" onClick={handleFindRoute}>Find Route</button>
        </div>
        <div className="MapContainer">
          <Map routeImage={routeImage} />
        </div>
      </div>
    </div>
  );
}

export default App;

