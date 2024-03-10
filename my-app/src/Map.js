// In Map.js
import React from 'react';

const Map = ({ routeImage }) => {
  return (
    <div>
      {routeImage ? <img src={routeImage} alt="Route Map" style={{ width: '100%', height: 'auto' }} /> : 'Route map will be displayed here.'}
    </div>
  );
};

export default Map;

