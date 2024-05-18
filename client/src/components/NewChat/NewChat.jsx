import React from 'react'
import { IoMdChatboxes } from "react-icons/io";

import './NewChat.css';

const NewChat = () => {
  return (
    <div className='newChat'>
        <IoMdChatboxes />
        <p>
            NewChat
        </p>
    </div>
  )
}

export default NewChat