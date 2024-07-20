import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './YouTubeURLForm.css';

function YouTubeURLForm() {
    const [url, setUrl] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        setIsLoading(true);
        try {
            const response = await axios.post('http://127.0.0.1:8000/videoanalyser/process_video/', JSON.stringify({ youtube_url: url }), {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': axios.defaults.headers.common['X-CSRFToken']
                }
            });
            console.log(response);
            setIsLoading(false);
            navigate('/chat');
        } catch (error) {
            console.error('Error processing video URL:', error);
            setIsLoading(false);
        }
    };

    return (
        <div className="form-container">
            <h1>YTVideoAnalyser</h1>
            <p>Welcome to YTVideoAnalyser! Follow the steps below to analyze YouTube videos.</p>
            <ol className="instructions">
                <li>Enter the URL of the YouTube video you wish to analyze.</li>
                <li>Click on 'Start Chat' to process the video.</li>
                <li>Interact with the chat interface to get insights about the video content.</li>
            </ol>
            <form onSubmit={handleSubmit} className="form">
                <input
                    type="text"
                    className="input"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter YouTube URL"
                    required
                />
                <button type="submit" className="button" disabled={isLoading}>Start Chat</button>
                {isLoading && <div className="loading-bar"></div>}
            </form>
        </div>
    );
}

export default YouTubeURLForm;
