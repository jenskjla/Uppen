// src/components/MainPage.js
import React from "react";
import Header from "./Header";
import Sidebar from "./Sidebar";
import Content from "./Content";
import Chatbot from "./Chatbot";
import '../App.css'; // Corrected import path

const MainPage = () => {
  return (
    <div className="app">
      <Header />
      <div className="main">
        <Sidebar />
        <div className="content-wrapper">
          <Content />
          <Chatbot />
        </div>
      </div>
    </div>
  );
}

export default MainPage;
