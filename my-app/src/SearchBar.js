import React, { useEffect, useState } from 'react';
import "./searchBar.css"

function SearchBar({geography, placeholder, onSelect, selectedStation}){
    const [stations, setStations] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [filteredData, setFilteredData] = useState([]);
    const [wordEntered, setWordEntered] = useState("");
    const [selectedStationDetails, setSelectedStationDetails] = useState(null);


    useEffect(() => {
      setSelectedStationDetails(null);
      setWordEntered(selectedStation || "");
      if (selectedStation) {
        const stationDetails = stations.find(s => s.name === selectedStation);
        setSelectedStationDetails(stationDetails || null);
      }
    }, [selectedStation, stations]);

    const handleSelectStation = (name) => {
        const cleanedName = name.trim(); 
        setWordEntered(cleanedName);
        setFilteredData([])
        onSelect(name); 
    }

    const handleFilter = (event) => {
      setSelectedStationDetails(null);
      const searchWord = event.target.value.toLowerCase();
      setWordEntered(searchWord);
      const newFilter = stations.filter((station) => {
          return (
              station.name.toLowerCase().includes(searchWord) ||
              (station.admin1 && station.admin1.toLowerCase().includes(searchWord)) ||
              (station.admin2 && station.admin2.toLowerCase().includes(searchWord)) ||
              (station.country && station.country.toLowerCase().includes(searchWord))
          );
      });
  
      setFilteredData(searchWord === "" ? [] : newFilter);
  };
  

    useEffect(() => {
      const fetchStations = async () => {
        setIsLoading(true);
        try {
          const response = await fetch(`https://railroads-production.up.railway.app/api/${geography}/stations`);
          if (!response.ok) {
            throw new Error('Something went wrong!');
          }
          const data = await response.json();
          setStations(data);
        } catch (error) {
          setError(error.message);
        }
        setIsLoading(false);
      };

      if (geography) {
        fetchStations();
      }
    }, [geography]);

    return (
      <div className="search">
          <div className="searchInputs">
              <input
                  type="text"
                  placeholder={placeholder}
                  value={wordEntered}
                  onChange={handleFilter}
              />
          </div>
          {selectedStationDetails && ( 
            <div className="station-selected-details">
                <p>{selectedStationDetails.admin1}, {selectedStationDetails.admin2}, {selectedStationDetails.country}</p>
            </div>
        )}
          {filteredData.length !== 0 && (
              <div className="dataResult">
                  {isLoading && <div>Loading...</div>}
                  {error && <div>Error: {error}</div>}
                  {filteredData.map((station, index) => (
                  <div key={index} className="dataItem" onClick={() => handleSelectStation(station.name)}>
                      <p className="station-name">{station.name.trim()}</p>
                      <p className="station-details">
                      {station.admin2}, {station.admin1}, {station.country}
                      </p>
                  </div>
                  ))}
              </div>
          )}
      </div>
  );
                  }
export default SearchBar