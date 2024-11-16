// src/components/Sidebar.js
import React, { useState } from "react";
import './Sidebar.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(true);

  const toggleSidebar = () => setIsOpen(!isOpen);

  return (
    <aside className={`sidebar ${isOpen ? "open" : "closed"}`}>
      <button className="toggle-btn" onClick={toggleSidebar}>
        {isOpen ? (
            <span>Collapse</span>
          ) : (
            <FontAwesomeIcon icon={faBars} />
        )}
      </button>
      <div className="sidebar-content">
        {isOpen && (
          <ul>
            <li>Chapter 1</li>
            <li>Chapter 2</li>
            <li>Chapter 3</li>
            {/* Add more chapters here */}
          </ul>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
