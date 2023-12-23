import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000'); // Adjust the URL to your Flask server

function App() {
  const [measurements, setMeasurements] = useState([]);

  useEffect(() => {
    socket.on('position', (data) => {
      setMeasurements(currentMeasurements => [...currentMeasurements, JSON.parse(data.data)]);
    });

    // Clean up the effect
    return () => socket.off('position');
  }, []);

  return (
    <div>
      <h1>Measurements</h1>
      {measurements.map((measurement, index) => (
        <div key={index}>
          Lat: {measurement.lat}, Lon: {measurement.lon}
        </div>
      ))}
    </div>
  );
}

export default App;
