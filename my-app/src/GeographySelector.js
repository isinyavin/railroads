import React from 'react';

function GeographySelector({ label, setSelectedGeography, selectedGeography }) {
  const handleGeographyChange = (event) => {
    setSelectedGeography(event.target.value);
  };

  return (
    <div>
      <label htmlFor="geography-select">{label}</label>
      <select id="geography-select" value={selectedGeography} onChange={handleGeographyChange}>
        <option value="">Please Select a Geography</option>
        <option value="dublin">Dublin, Ireland</option>
        <option value="uk">United Kingdom</option>
        <option value="nyc">New York City</option>
      </select>
    </div>
  );
}

export default GeographySelector;
