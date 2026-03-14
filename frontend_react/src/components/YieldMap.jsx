import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in React-Leaflet
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const YieldMap = () => {
  const position = [10.78, 79.13]; // Center on Tamil Nadu (Thanjavur)

  return (
    <div className="h-full w-full rounded-2xl overflow-hidden border border-gray-200">
      <MapContainer center={position} zoom={8} scrollWheelZoom={false} style={{ height: '400px', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position}>
          <Popup>
            Thanjavur Region: <br /> Healthy Crop Growth detected via Sentinel-2.
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
};

export default YieldMap;
