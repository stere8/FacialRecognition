// src/components/CameraViewer.jsx

import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../settings';
import { getCameraIndices } from '../api';

export default function CameraViewer(){
    const [cameras,setCameras] = useState([]);
    const [selectedIndex, setSelectedIndex] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() =>{
        getCameraIndices()
      .then((list) => setCameras(list))
      .catch(() => setError("Could not load camera list."))
    },[])

      // Declare handleChange correctly:
    const handleChange = (e) => {
    const idx = parseInt(e.target.value, 10)
    setSelectedIndex(isNaN(idx) ? null : idx)
    setError('')
  }

    return(
      <div className='max-w-md mx-auto p-4'>
        <h2 className='text-x0 font-semibold mb-2'>Select a camera</h2>
        {error && <p className='text-red-500'>{error}</p>}
        <select
          className="w-full border rounded p-2 mb-4"
          value={selectedIndex || ''}
          onChange={handleChange}   >
              <option value="">-- pick camera index --</option>
        {cameras.map((idx) => (
          <option key={idx} value={idx}>
            Camera {idx}
          </option>
        ))}
          </select>
        {selectedIndex !== null && (
          <div>
            <h3 className="text-lg font-medium mb-2">
              Selected Camera: {selectedIndex} Live Feed
            </h3>
            <img
              src={`${API_BASE_URL}/api/camera/${selectedIndex}/stream`}
              alt={`Camera ${selectedIndex} live feed`}
              onError={() => setError("Could not load camera feed.")}
            />
          </div>)}

      </div>
    )
}