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
  const [failedtoRoute, setfailedtoRoute] = useState(false)
  const [displayMap, setDisplayMap] = useState(false);
  const [initiatedsearch, setInitiatedSearch] = useState(false);

  const toggleDisplay = () => {
    setDisplayMap(!displayMap); 
  };

  const handleFindRoute = async () => {
    try {
      setDisplayMap(true);
      setIsLoading(true);
      setfailedtoRoute(false);
      setInitiatedSearch(true);
      const detailsResponse = await fetch(`https://railroads-production.up.railway.app/api/route/details/${geography}/${startStation}/${destinationStation}`);
      if (detailsResponse.ok) {
        const detailsData = await detailsResponse.json(); 
        setRouteDetails(detailsData); 
        const routeResponse = await fetch(`https://railroads-production.up.railway.app/api/route/${geography}/${startStation}/${destinationStation}`);
        if (routeResponse.ok) {
          const blob = await routeResponse.blob();
          const imageUrl = URL.createObjectURL(blob);
          setRouteImage(imageUrl);
          setIsLoading(false);
        }
      } else {
        setIsLoading(false);
        setfailedtoRoute(true);
        setRouteImage(null);
        setRouteDetails([]);
      }
    } catch (error) {
      setIsLoading(false);
      setfailedtoRoute(true);
      setRouteImage(null);
      setRouteDetails([]);
    }
  };

  const generateRandomStations = async () => {
    if (!geography) 
    {
      alert('Please select a geography first.');
      return;
    }
    try {
      const response = await fetch(`https://railroads-production.up.railway.app/api/${geography}/stations`);
      if (!response.ok) {
        throw new Error('Failed to fetch stations');
      }
      const stationsData = await response.json();

      let startStationIndex = Math.floor(Math.random() * stationsData.length);
      let destinationStationIndex = Math.floor(Math.random() * stationsData.length);
      while (destinationStationIndex === startStationIndex) {
        destinationStationIndex = Math.floor(Math.random() * stationsData.length);
      }

    setStartStation(stationsData[startStationIndex].name);
    setDestinationStation(stationsData[destinationStationIndex].name);

  } catch (error) {
    console.error('Error fetching stations:', error);
    setIsLoading(false);
  }
  }
  

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
              <SearchBar geography={geography} placeholder={"Enter Departure Station"} onSelect={setStartStation} selectedStation={startStation}/>
              <SearchBar geography={geography} placeholder="Enter Destination Station" onSelect={setDestinationStation} selectedStation={destinationStation} />
              <button className="random-station-generator" onClick={generateRandomStations}>Generate Random Stations</button>

            </div>
            <button className="find-route-button" onClick={handleFindRoute}>Find Route</button>
            {failedtoRoute && (
          <div className="error-box">
            <p>No route exists between the two selected stations. Please try again.</p>
            </div>
        )}
            {isLoading && (
                <div className="loading-container">
                  <p>Loading map. This may take a while...</p>
                  <Spinner />
                </div>
              )}
          </div>
          <div className="Output-Components">

            {!isLoading && initiatedsearch && !failedtoRoute && ( 
              <div className = "toggle-bar">
              <div className={`slider ${displayMap === true ? 'left' : 'right'}`}></div>
              <button className={`toggle-option ${displayMap === true ? 'active': ''}`}
                onClick={()=>toggleDisplay()}>
                  Map
              </button>
              <button className={`toggle-option ${displayMap === false ? 'active': ''}`}
                onClick={()=>toggleDisplay()}>
                  Details
              </button>
              </div>
              )}
          {displayMap && (
            <div className="MapContainer">
              {!isLoading && <Map routeImage={routeImage} />}
            </div>
          ) }
          
            {!displayMap && initiatedsearch && !isLoading && (
              <div className="RouteDetails">
              <h2>Route Details</h2>
            {routeDetails.length > 0 ? (
            <ul>
              {routeDetails.map((station, index) => {
                return (
                  <li key={index}>{station}</li> 
                );
              })}
            </ul>
          ) : (
            <p>No route details available.</p>
          )}
            </div>
            )
          }


    
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

