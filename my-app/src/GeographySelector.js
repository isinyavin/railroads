import React, {useState } from 'react';

function GeographySelector({ label, setSelectedGeography, selectedGeography }) {
    const [geography, setGeography] = useState([]);
    
    const handleGeographyChange = (event) => {
      setSelectedGeography(event.target.value);
      setGeography(event.target.value)
    };
  
    return (
      <div>
        <label htmlFor="geography-select">{label}</label>
        <select id="geography-select" value={geography} onChange={handleGeographyChange}>
          <option value="Dublin, Ireland">Dublin, Ireland</option>
          <option value="United Kingdom">United Kingdom</option>
        </select>
      </div>
    );
}
  
export default GeographySelector;
