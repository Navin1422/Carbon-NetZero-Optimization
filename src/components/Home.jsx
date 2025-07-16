// src/components/Home.jsx
import React from 'react';
import './Home.css';

const Home = () => {
  return (
    <div className="home-wrapper">
      {/* Title Section */}
      <div className="home-title-section">
        <h1>🌍 Carbon Net Zero Tracking and Optimization System</h1>
        <p>
          Empowering industries to monitor, reduce, and optimize Scope 1, 2, and 3 carbon emissions using AI-driven insights and real-time data.
        </p>
      </div>

      {/* Project Overview */}
      <div className="home-overview-box">
        <h2>📘 Overview</h2>
        <ul>
          <li>✔ Real-time emissions tracking across departments</li>
          <li>✔ AI analysis for emission hotspot detection</li>
          <li>✔ Net Zero progress milestones (2028, 2032, 2040)</li>
          <li>✔ ESG reporting and carbon offset integration</li>
        </ul>
      </div>
      
  


      {/* Usage Section (same style) */}
      <div className="home-overview-box">
        <h2>🛠️ How to Use the System</h2>
        <ul>
          <li>📥 Upload emission data via the Emission Form (CSV format)</li>
          <li>📊 View real-time analytics on the Dashboard</li>
          <li>🧠 Explore AI-based suggestions to reduce emissions</li>
          <li>🧾 Download reports and track Net Zero milestones</li>
        </ul>
      </div>
    </div>
  );
};

export default Home;
