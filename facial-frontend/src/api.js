import axios from 'axios';
import { API_BASE_URL } from './settings.js';


export async function getFaces(){
    const response = await axios.get(`${API_BASE_URL}/api/faces`);
    return response.data;
}

export async function recognizeFace(file){
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `${API_BASE_URL}/api/recognize`,
        formData,
        {
            headers:{'Content-Type': 'multipart/form-data'},
        }
    );
    return response.data;
}

export async function saveFace(file, name) {
    if (!file || !name) {
        throw new Error('File and name are required to save a face.');
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);
    const response = await axios.post(
        `${API_BASE_URL}/api/faces/save`,
        formData,
        {
            headers:{'Content-Type': 'multipart/form-data'},
        }
    );
    return response.data;
}

export async function getCameraIndices() {
  const res = await fetch(`${API_BASE_URL}/api/camera/`)
  if (!res.ok) throw new Error(`Status ${res.status}`)
  const data = await res.json()
  return data.cameras   // array of ints
}