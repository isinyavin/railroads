"use client"
import React, { useState} from 'react';
import GeographySelector from "./GeographySelector"
import Map from './Map';
import './App.css';
import SearchBar from "./SearchBar"
import Spinner from './Spinner';

function App() {
  const [startStation, setStartStation] = useState('');
  const [geography, setGeography] = useState('');
  const [destinationStation, setDestinationStation] = useState('');
  const [routeImage, setRouteImage] = useState(null); 
  const [routeDetails, setRouteDetails] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleFindRoute = async () => {
    try {
      setIsLoading(true);
      const detailsResponse = await fetch(`https://railroads-production.up.railway.app/api/route/details/${geography}/${startStation}/${destinationStation}`);
      if (detailsResponse.ok) {
        const detailsData = await detailsResponse.json(); 
        setRouteDetails(detailsData); 
      } else {
        alert('Failed to fetch route details. Please try again.');
        setIsLoading(false);
      }
  
      const routeResponse = await fetch(`https://railroads-production.up.railway.app/api/route/${geography}/${startStation}/${destinationStation}`);
      if (routeResponse.ok) {
        const blob = await routeResponse.blob();
        const imageUrl = URL.createObjectURL(blob);
        setRouteImage(imageUrl);
        setIsLoading(false);
      } else {
        alert('Failed to fetch the route image. Please try again.');
        setIsLoading(false);
      }
    } catch (error) {
      console.error('Error fetching route:', error);
      alert('Error fetching the route. Please check your connection and try again.');
      setIsLoading(false);
    }
  };
  

  return (
    <div className="App">
      <header className="App-header">
        RailRouter
      </header>
      <div className="ContentwMap">
        <div className="Content">
          <div className="Selectors-wrapper">
            <div className="Selectors">
              <GeographySelector
                label="Choose a geography"
                setSelectedGeography={setGeography}
                selectedGeography={geography}
              />
              <SearchBar geography={geography} placeholder="Enter Departure Station" onSelect={setStartStation} selectedStation={startStation}/>
              <SearchBar geography={geography} placeholder="Enter Destination Station" onSelect={setDestinationStation} selectedStation={destinationStation} />
            </div>
            <button className="find-route-button" onClick={handleFindRoute}>Find Route</button>
          </div>
          <div className="RouteDetails">
          <h2>Route Details</h2>
          {routeDetails.length > 0 ? (
            <ul>
              {routeDetails.map((station, index) => {
                let stationClass = "";
                if (station === startStation || station === destinationStation) {
                  stationClass = "bold"; 
                }
                return (
                  <li key={index} className={stationClass}>{station}</li> 
                );
              })}
            </ul>
          ) : (
            <p>No route details available.</p>
          )}
        </div>
        </div>
        {isLoading && (
        <div className="loading-container">
          <p>Loading map. This may take a while...</p>
          <Spinner />
        </div>
        )}
      {!isLoading && (
        <div className="MapContainer">
          <Map routeImage={routeImage} />
      </div>
      )}
      </div>
    </div>
  );
}

export default App;

