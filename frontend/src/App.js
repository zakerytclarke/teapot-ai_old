import React, { useEffect } from 'react';
import { Widget, addResponseMessage } from 'react-chat-widget';
import './App.css';

import 'react-chat-widget/lib/styles.css';

import logo from './assets/logo.gif';



function App() {
  useEffect(() => {
    addResponseMessage("Hello, I'm Teapot AI. How can I help you?");
  }, []);

  const handleNewUserMessage = async (newMessage) => {
    var chat_env={
      service_id:"wikiqa",
      message:newMessage
    }
    var reply = await fetch("http://localhost:5000/getReply",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify(chat_env)
    }).then(x=>x.json());

    addResponseMessage(reply.message);
  };

  

    return (
      
      <div className="App">
        <img id="logo" src={logo} alt="Logo" />
        <Widget
          handleNewUserMessage={handleNewUserMessage}
          profileAvatar={logo}
          title="Chat with Teapot AI"
          subtitle="Chatting with Teapot Customer Service"
        />
      </div>
    );
}

export default App;