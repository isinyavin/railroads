import React, { useEffect, useState } from 'react';
import "./searchBar.css"

function SearchBar({placeholder, onSelect, selectedStation}){
    const [stations, setStations] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [filteredData, setFilteredData] = useState([]);
    const [wordEntered, setWordEntered] = useState("");
    
    const handleSelectStation = (name) => {
        setWordEntered(name)
        setFilteredData([])
        onSelect(name); 
    }

    const handleFilter = (event) =>{
        const searchWord = event.target.value
        setWordEntered(searchWord)
        const newFilter = stations.filter((station) => {
            return station.name.toLowerCase().includes(searchWord.toLowerCase());
        });

        if (searchWord === ""){
            setFilteredData([])
        }
        else 
        {
            setFilteredData(newFilter)
        }
        
    }

    useEffect(() => {
        const fetchStations = async () => {
          setIsLoading(true);
          try {
            const response = await fetch('http://127.0.0.1:5003/api/stations');
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
    
        fetchStations();
      }, []);

    return (
        <div className="search">
          <div className="searchInputs">
            <input type="text" placeholder={placeholder} value={wordEntered} onChange={handleFilter} />
          </div>
            {filteredData.length !== 0 && (
            <div className='dataResult'>
                {isLoading && <div>Loading...</div>}
                {error && <div>Error: {error}</div>}
                {filteredData.slice(0,15).map((station, index) => (
                    <div key={index} className="dataItem" onClick={() => handleSelectStation(station.name)}>
                        <p>{station.name}</p>
                    </div>
                ))}
            </div>
            )}
        </div>
      );
    }
export default SearchBar