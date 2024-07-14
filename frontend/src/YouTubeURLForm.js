import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './YouTubeURLForm.css';

function YouTubeURLForm() {
    const [url, setUrl] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/videoanalyser/get_csrf_token/')
            .then(response => {
                const token = response.data.csrfToken;
                axios.defaults.headers.common['X-CSRFToken'] = token;
                axios.defaults.headers.post['Content-Type'] = 'application/json';
            })
            .catch(error => console.error('Error fetching CSRF token:', error));
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/videoanalyser/process_video/', JSON.stringify({ youtube_url: url }), {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': axios.defaults.headers.common['X-CSRFToken']
                }
            });
            console.log(response);
            navigate('/chat');
        } catch (error) {
            console.error('Error processing video URL:', error);
        }
    };

    return (
        <div className="form-container">
            <form onSubmit={handleSubmit} className="form">
                <input
                    type="text"
                    className="input"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter YouTube URL"
                    required
                />
                <button type="submit" className="button">Start Chat</button>
            </form>
        </div>
    );
}

export default YouTubeURLForm;
