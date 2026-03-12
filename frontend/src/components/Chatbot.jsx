// SmartCurriculum - AI Chatbot Component
// Floating chatbot with pre-built FAQ responses about the app

import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Bot, User, Sparkles } from 'lucide-react';
import './Chatbot.css';

// Pre-built responses for common questions
const FAQ_RESPONSES = {
    'what is this app': {
        answer: "SmartCurriculum is an AI-powered personalized educational curriculum design system. It helps you create customized learning paths based on your academic goals, tracks your progress, and provides resources for each topic.",
        suggestions: ['How do I create a curriculum?', 'What features are available?']
    },
    'how do i create a curriculum': {
        answer: "To create a curriculum:\n1. Go to the Curriculum page\n2. Click 'New Curriculum' or 'Generate My Roadmap'\n3. Select your program category (Engineering, Science, Commerce, etc.)\n4. Choose your learning intensity\n5. Click Generate!\n\nYour personalized roadmap will be created with modules, topics, and estimated hours.",
        suggestions: ['How do I track progress?', 'Can I download my curriculum?']
    },
    'what features are available': {
        answer: "SmartCurriculum offers:\n• 📚 Personalized curriculum generation\n• 📊 Progress tracking with skill checkboxes\n• 📄 PDF download of your roadmap\n• 👤 Profile customization\n• 📝 Resume analysis (coming soon)\n• 🎯 Career-focused learning paths",
        suggestions: ['How do I track progress?', 'Tell me about the dashboard']
    },
    'how do i track progress': {
        answer: "You can track your progress by:\n• Checking off completed skills in each module\n• Viewing the progress percentage on the Curriculum page\n• Checking the Dashboard for overall statistics\n\nCompleted modules are marked with a green checkmark!",
        suggestions: ['What is the dashboard?', 'Can I download my curriculum?']
    },
    'can i download my curriculum': {
        answer: "Yes! You can download your curriculum as a PDF:\n1. Go to the Curriculum page\n2. Click 'Download PDF' button\n3. Save the file to your device\n\nThis creates a professional roadmap you can print or share.",
        suggestions: ['What features are available?', 'How do I edit my profile?']
    },
    'tell me about the dashboard': {
        answer: "The Dashboard is your central hub showing:\n• Your current curriculum progress\n• Quick stats (modules completed, hours studied)\n• Recent activity\n• Quick actions to navigate the app\n\nIt gives you an overview of your learning journey!",
        suggestions: ['How do I create a curriculum?', 'How do I track progress?']
    },
    'how do i edit my profile': {
        answer: "To edit your profile:\n1. Click on your avatar in the top-right corner\n2. Select 'Profile' from the menu\n3. Update your information (name, university, career goals, skills)\n4. Click 'Save Changes'\n\nYour profile helps personalize your curriculum recommendations!",
        suggestions: ['What features are available?', 'How do I create a curriculum?']
    },
    'hello': {
        answer: "Hello! 👋 I'm your SmartCurriculum assistant. I can help you navigate the app, create curricula, track progress, and more. What would you like to know?",
        suggestions: ['What is this app?', 'How do I create a curriculum?']
    },
    'help': {
        answer: "I'm here to help! Here are some things I can assist with:\n• Creating and managing curricula\n• Tracking your learning progress\n• Understanding app features\n• Downloading your roadmap\n• Profile settings\n\nJust ask me anything!",
        suggestions: ['What is this app?', 'What features are available?']
    }
};

// Default response for unknown queries
const DEFAULT_RESPONSE = {
    answer: "I'm not sure about that, but I can help you with:\n• Creating curricula\n• Tracking progress\n• App features\n• Downloading PDFs\n\nTry asking about these topics!",
    suggestions: ['What is this app?', 'How do I create a curriculum?', 'What features are available?']
};

function Chatbot() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        {
            type: 'bot',
            text: "Hi! 👋 I'm your SmartCurriculum assistant. How can I help you today?",
            suggestions: ['What is this app?', 'How do I create a curriculum?', 'What features are available?']
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    // Auto-scroll to latest message
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Focus input when opened
    useEffect(() => {
        if (isOpen) {
            inputRef.current?.focus();
        }
    }, [isOpen]);

    const findResponse = (query) => {
        const lowerQuery = query.toLowerCase().trim();

        // Check for exact or partial matches
        for (const [key, value] of Object.entries(FAQ_RESPONSES)) {
            if (lowerQuery.includes(key) || key.includes(lowerQuery)) {
                return value;
            }
        }

        // Check for keyword matches
        if (lowerQuery.includes('curriculum') || lowerQuery.includes('roadmap')) {
            return FAQ_RESPONSES['how do i create a curriculum'];
        }
        if (lowerQuery.includes('progress') || lowerQuery.includes('track')) {
            return FAQ_RESPONSES['how do i track progress'];
        }
        if (lowerQuery.includes('download') || lowerQuery.includes('pdf')) {
            return FAQ_RESPONSES['can i download my curriculum'];
        }
        if (lowerQuery.includes('profile') || lowerQuery.includes('settings')) {
            return FAQ_RESPONSES['how do i edit my profile'];
        }
        if (lowerQuery.includes('feature') || lowerQuery.includes('what can')) {
            return FAQ_RESPONSES['what features are available'];
        }
        if (lowerQuery.includes('dashboard') || lowerQuery.includes('home')) {
            return FAQ_RESPONSES['tell me about the dashboard'];
        }

        return DEFAULT_RESPONSE;
    };

    const handleSend = (text = inputValue) => {
        if (!text.trim()) return;

        // Add user message
        const userMessage = { type: 'user', text: text.trim() };
        setMessages(prev => [...prev, userMessage]);
        setInputValue('');

        // Simulate typing delay
        setTimeout(() => {
            const response = findResponse(text);
            const botMessage = {
                type: 'bot',
                text: response.answer,
                suggestions: response.suggestions
            };
            setMessages(prev => [...prev, botMessage]);
        }, 500);
    };

    const handleSuggestionClick = (suggestion) => {
        handleSend(suggestion);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="chatbot-container">
            {/* Chat Window */}
            {isOpen && (
                <div className="chatbot-window">
                    <div className="chatbot-header">
                        <div className="chatbot-header-info">
                            <div className="chatbot-avatar">
                                <Bot size={20} />
                            </div>
                            <div>
                                <h3>SmartCurriculum Assistant</h3>
                                <span className="online-status">Online</span>
                            </div>
                        </div>
                        <button className="chatbot-close" onClick={() => setIsOpen(false)}>
                            <X size={20} />
                        </button>
                    </div>

                    <div className="chatbot-messages">
                        {messages.map((message, index) => (
                            <div key={index} className={`message ${message.type}`}>
                                {message.type === 'bot' && (
                                    <div className="message-avatar">
                                        <Bot size={16} />
                                    </div>
                                )}
                                <div className="message-content">
                                    <p className="message-text">{message.text}</p>
                                    {message.suggestions && (
                                        <div className="message-suggestions">
                                            {message.suggestions.map((suggestion, i) => (
                                                <button
                                                    key={i}
                                                    className="suggestion-btn"
                                                    onClick={() => handleSuggestionClick(suggestion)}
                                                >
                                                    {suggestion}
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </div>
                                {message.type === 'user' && (
                                    <div className="message-avatar user">
                                        <User size={16} />
                                    </div>
                                )}
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="chatbot-input">
                        <input
                            ref={inputRef}
                            type="text"
                            placeholder="Ask me anything..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={handleKeyPress}
                        />
                        <button
                            className="send-btn"
                            onClick={() => handleSend()}
                            disabled={!inputValue.trim()}
                        >
                            <Send size={18} />
                        </button>
                    </div>
                </div>
            )}

            {/* Toggle Button */}
            <button
                className={`chatbot-toggle ${isOpen ? 'open' : ''}`}
                onClick={() => setIsOpen(!isOpen)}
            >
                {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
                {!isOpen && <span className="toggle-label">Help</span>}
            </button>
        </div>
    );
}

export default Chatbot;
