import { useState } from 'react'

import './App.css';
import Header from '../../components/Header/Header';
import NewChat from '../../components/NewChat/NewChat';
import ChatTitle from '../../components/ChatTitle/ChatTitle';
import Human from '../../components/Conversation/Human';
import AI from '../../components/Conversation/AI';
import Input from '../../components/Input/Input';

function App() {

  const chatTitles = [
    'Svelte code',
    'Rounding for Floating-point',
    'Highlight CanvasObject'
  ]

  const conversations = [
    {
      author: 'human',
      data: 'Hi! What are you?'
    },
    {
      author: 'ai',
      data: 'Hello! I am an AI model'
    },
    {
      author: 'human',
      data: 'What can you do?'
    },
    {
      author: 'ai',
      data: 'I present Move Code to you'
    }
  ]

  return (
      <div className="app">
        <div className="all-chats">
          <NewChat />

          <div className="previous-chats">

            {chatTitles.map((title) => 
              <ChatTitle title={title} />
            )}
            
          </div>
        </div>
        <div className="chat-screen">
          <div className="current-conversation">
            <Header />
            
            <div className='conversation'>
              {conversations.map((conversation) => {
                if (conversation.author == 'human')
                  return <Human data={conversation.data} />
                else
                  return <AI data={conversation.data} />
              })}
            </div>
          </div>

          <div className="prompt-wrapper">
              <Input />
          </div>
        </div>
      </div>
  )
}

export default App
