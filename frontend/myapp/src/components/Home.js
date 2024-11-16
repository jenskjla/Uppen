import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router for navigation
import './Home.css'; // Assuming you have a separate CSS file for styles

const Home = () => {
    const [dropdownOpen, setDropdownOpen] = useState(false);

    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen);
    };

    return (
        <>
            <header className="header">
                <h1 to="/" className="logo">HiveMind.ai</h1>
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

            {/* Main Content */}
            <main className="main-container">
                <h1>Welcome Neel Shettigar</h1>
                <p>Get ready to learn!</p>

                {/* Glassmorphic rectangles */}
                <div className="rectangle-container">
                    <Link to="/main" className="glassmorphic-rectangle">
                        {/* Use an online logo for CS 421 */}
                        <img 
                            src="https://upload.wikimedia.org/wikipedia/commons/3/38/OCaml_logo.svg" 
                            alt="OCaml Logo" 
                            className="rectangle-logo" 
                        />
                        <h2 className="class-name">CS 421</h2>
                        <p className="short-name">Programming Languages & Compilers</p>
                    </Link>

                    <Link to="/page2" className="glassmorphic-rectangle">
                        {/* Use an online logo for CS 424 */}
                        <img 
                            src="https://upload.wikimedia.org/wikipedia/commons/e/e2/Real-Time_Clock.svg" 
                            alt="Real Time Systems Logo" 
                            className="rectangle-logo" 
                        />
                        <h2 className="class-name">CS 424</h2>
                        <p className="short-name">Real Time Systems</p>
                    </Link>

                    <Link to="/page3" className="glassmorphic-rectangle">
                        {/* Use an online logo for CS 427 */}
                        <img 
                            src="https://upload.wikimedia.org/wikipedia/commons/6/65/Software-engineering-icon.png" 
                            alt="Software Engineering Logo" 
                            className="rectangle-logo" 
                        />
                        <h2 className="class-name">CS 427</h2>
                        <p className="short-name">Software Engineering I</p>
                    </Link>
                </div>
            </main>
        </>
    );
};

export default Home;
