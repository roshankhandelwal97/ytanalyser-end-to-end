import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import "./chat.css"

function Chat() {
    const [question, setQuestion] = useState('');
    const [messages, setMessages] = useState([]);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleQuestionSubmit = async (event) => {
        event.preventDefault();
        if (!question) return;
        try {
            const response = await axios.post('http://localhost:8000/videoanalyser/query_video/', { question });
            const newMessage = { type: 'answer', text: response.data.answer };
            setMessages([...messages, { type: 'question', text: question }, newMessage]);
            setQuestion('');
        } catch (error) {
            console.error('Error sending question:', error);
        }
    };

    return (
        <div className="chat-container">
            <h1>Ask video related questions</h1>
            <div className="chat-box">
                <div className="chat-messages">
                    {messages.map((msg, index) => (
                        <div key={index} className={`message ${msg.type}`}>
                            {msg.text}
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>
                <form onSubmit={handleQuestionSubmit} className="chat-input">
                    <input
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="Ask a question..."
                        required
                    />
                    <button type="submit">Send</button>
                </form>
            </div>
        </div>
    );
}

export default Chat;