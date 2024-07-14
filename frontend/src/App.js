// App.js
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import YouTubeURLForm from './YouTubeURLForm.js';
import Chat from './Chat.js';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<YouTubeURLForm />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </BrowserRouter>
  );
}


export default App;
