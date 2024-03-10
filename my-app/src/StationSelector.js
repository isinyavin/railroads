import React, { useEffect, useState } from 'react';

function StationSelector({ label }) {
  const [stations, setStations] = useState([]);

  useEffect(() => {
    const fetchStations = async () => {
      const response = await fetch('/api/stations');
      const data = await response.json();
      setStations(data);
    };

    fetchStations();
  }, []);

  return (
    <div className="station-selector">
      <label>{label}</label>
      <select>
        {stations.map((station, index) => (
          <option key={index} value={station.name}>
            {station.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default StationSelector;

