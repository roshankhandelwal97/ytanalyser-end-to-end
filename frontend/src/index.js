import React from 'react';
import { createRoot } from 'react-dom/client'; // Import createRoot
import App from './App';
import axios from 'axios';

// Ensure cookies are sent with requests
axios.defaults.withCredentials = true;

// Configure Axios to handle CSRF
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';


// Function to get CSRF token from cookies
function getCsrfToken() {
    const cookieString = document.cookie;
    console.log("Cookies: ", cookieString);  // Helpful for debugging
    const token = cookieString
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    console.log("CSRF Token: ", token);  // Verify the token is correct
    return token;
}

// Set up Axios to include CSRF token in the headers
axios.interceptors.request.use(config => {
    const token = getCsrfToken();
    if (token) {
        config.headers['X-CSRFToken'] = token;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// Using the new root API for React 18
const container = document.getElementById('root');
const root = createRoot(container); // Create a root.
root.render(
  
    <React.StrictMode>
        <App />
    </React.StrictMode>
);