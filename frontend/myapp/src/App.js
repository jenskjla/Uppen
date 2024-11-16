// src/App.js
import React from "react";
import { Routes, Route } from "react-router-dom"; // Import Routes and Route
import MainPage from "./components/MainPage"; // Import MainPage component
import Home from "./components/Home"; // Import the new blank Home component
import './App.css';

function App() {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<Home />} />  {/* New blank Home page */}
        <Route path="/main" element={<MainPage />} /> {/* Existing layout as MainPage */}
      </Routes>
    </div>
  );
}

export default App;
