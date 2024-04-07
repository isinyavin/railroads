import React, { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './TrainRouteMap.css';
import markerIcon from '/Users/ivansinyavin/Desktop/UKRailroad/my-app/src/3448683-1.png';

const TrainRouteMap = ({ geo, depart, dest, startRouting, coordinates, stations, appearstations}) => {
  useEffect(() => {
    if (!startRouting) return;
    if(!coordinates && !stations) return;

    const map = L.map('map').setView([54.9679903, -2.4627642], 8); 

    const customIcon = L.icon({
        iconUrl: markerIcon,
        iconSize: [25, 25], 
        popupAnchor: [1, -34], 
        shadowSize: [41, 41] 
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
    }).addTo(map);

    const routeLatLngs = coordinates.map(coord => {
      const [lng, lat] = coord.split(', ').map(Number);
      return [lat, lng];
    });

    if (routeLatLngs.length > 1) {
      const polyline = L.polyline(routeLatLngs, { color: 'blue' }).addTo(map);
      map.fitBounds(polyline.getBounds());
    } else {
      console.error('Insufficient data for route coordinates: ', routeLatLngs);
    }
    if (Array.isArray(stations)) {
      stations.forEach((station, index) => {
        const [lng, lat] = station.coordinates;
        
        const isFirstOrLast = index === 0 || index === stations.length - 1;
    
        if (isFirstOrLast || appearstations) {
          let marker = L.marker([lat, lng], {icon: customIcon}).addTo(map);
          
          if (isFirstOrLast) {
            marker.bindTooltip(station.name, {permanent: true}).openTooltip();
          } else {
            marker.bindPopup(station.name);
          }
        }
      });
    }
    else {
      console.error('stationsData is not an array:', stations);
    }
    return () => map.remove();
    }, [geo, depart, dest, startRouting, coordinates, stations, appearstations]);

  return <div id="map" className="map-container"></div>;
};

export default TrainRouteMap;
