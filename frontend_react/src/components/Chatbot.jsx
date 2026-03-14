import React, { useState } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';
import api from '../api';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hello! I'm your AgriAI assistant. How can I help you today?", sender: 'bot' }
  ]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { text: input, sender: 'user' };
    setMessages([...messages, userMsg]);
    setInput('');

    try {
      const res = await api.post('/chatbot', { message: input });
      setMessages(prev => [...prev, { text: res.data.response, sender: 'bot' }]);
    } catch (err) {
      setMessages(prev => [...prev, { text: "Sorry, I'm having trouble connecting right now.", sender: 'bot' }]);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="bg-white w-80 h-96 rounded-2xl shadow-2xl flex flex-col border border-gray-200">
          <div className="bg-calm-green-600 p-4 rounded-t-2xl flex justify-between items-center text-white">
            <span className="font-bold">AgriAI Chatbot</span>
            <button onClick={() => setIsOpen(false)}><X className="h-5 w-5" /></button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${m.sender === 'user' ? 'bg-calm-green-600 text-white' : 'bg-white shadow-sm text-gray-800'}`}>
                  {m.text}
                </div>
              </div>
            ))}
          </div>
          <div className="p-4 border-t border-gray-200 flex gap-2">
            <input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              className="flex-1 border border-gray-300 rounded-full px-4 text-sm focus:outline-none focus:border-calm-green-500" 
              placeholder="Ask anything..." 
            />
            <button onClick={handleSend} className="bg-calm-green-600 text-white p-2 rounded-full"><Send className="h-4 w-4" /></button>
          </div>
        </div>
      ) : (
        <button 
          onClick={() => setIsOpen(true)}
          className="bg-calm-green-600 text-white p-4 rounded-full shadow-lg hover:scale-110 transition scale-100"
        >
          <MessageCircle className="h-6 w-6" />
        </button>
      )}
    </div>
  );
};

export default Chatbot;
