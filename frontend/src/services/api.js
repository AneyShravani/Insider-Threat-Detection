import axios from 'axios';

const BASE_URL = 'http://localhost:5000'; // your app.py runs here

export const fetchDashboardData = () => axios.get(`${BASE_URL}/api/dashboard`);
export const fetchThreatData = () => axios.get(`${BASE_URL}/api/threats`);
export const fetchUserRiskData = () => axios.get(`${BASE_URL}/api/user-risk`);
export const fetchMLData = () => axios.get(`${BASE_URL}/api/ml-analysis`);