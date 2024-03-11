import React, { useEffect, useState } from 'react';

function StationSelector({ label, onSelect, selectedStation }) {
  const [stations, setStations] = useState([]);

  useEffect(() => {
    const fetchStations = async () => {
      const response = await fetch('https://railroads.onrender.com/api/stations');
      const data = await response.json();
      setStations(data);
    };

    fetchStations();
  }, []);

  const handleSelectChange = (event) => {
    onSelect(event.target.value); 
  };

  return (
    <div className="station-selector">
      <label>{label}</label>
      <select value={selectedStation} onChange={handleSelectChange}>
        {stations.map((station) => (
          <option key={station.id} value={station.name}>
            {station.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default StationSelector;
