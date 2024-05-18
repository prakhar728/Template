import React from 'react';
import { FaRobot } from "react-icons/fa";

import "./style.css";

const AI = ({data}) => {
  return (
    <div className='ai'>
        <FaRobot />
        <p>
        {data}
        </p>
    </div>
  )
}

export default AI