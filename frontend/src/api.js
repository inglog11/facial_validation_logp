import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8006/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const employeeAPI = {
  list: () => api.get('/employees/'),
  get: (id) => api.get(`/employees/${id}/`),
  create: (data) => {
    const formData = new FormData();
    formData.append('employee_code', data.employee_code);
    formData.append('full_name', data.full_name);
    formData.append('status', data.status);
    formData.append('photo_ref', data.photo_ref);
    
    return api.post('/employees/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  update: (id, data) => {
    const formData = new FormData();
    if (data.full_name) formData.append('full_name', data.full_name);
    if (data.status) formData.append('status', data.status);
    if (data.photo_ref) formData.append('photo_ref', data.photo_ref);
    
    return api.patch(`/employees/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  delete: (id) => api.delete(`/employees/${id}/`),
};

export const checkInAPI = {
  checkIn: (employeeCode, captureImage) => 
    api.post('/check-in/', {
      employee_code: employeeCode,
      capture_image: captureImage,
    }),
};

export default api;
