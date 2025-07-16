// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // Your Django backend base URL
  timeout: 5000, // optional timeout
  // ✅ Don't set Content-Type here — let it be set individually per request (e.g. form-data)
});

export default api;
