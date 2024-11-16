// src/components/Header.js
import React, { useState } from "react";
import { Link } from "react-router-dom"; // Import Link for navigation
import './Header.css'; 

const Header = () => {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const toggleDropdown = () => setDropdownOpen(!dropdownOpen);

  return (
    <header className="header">
      <Link to="/" className="logo">HiveMind.ai</Link> <Link to="/" className="logo2">CS421: Programming Languages & Compilers</Link>{/* Link to the blank Home page */}
      <div className="profile-menu">
        <img 
          src="/path-to-pfp.jpg" 
          alt="profile" 
          className="profile-pic" 
          onClick={toggleDropdown} 
        />
        {dropdownOpen && (
          <div className="dropdown">
            <ul>
              <li>Profile</li>
              <li>Logout</li>
            </ul>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
