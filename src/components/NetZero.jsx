// src/components/NetZero.jsx
import React from 'react';
import './NetZero.css';

const NetZero = () => {
  // Dummy emission data
  const milestones = [
    { year: 2028, target: 2000, actual: 2400 },
    { year: 2032, target: 1200, actual: 1800 },
    { year: 2040, target: 0, actual: 900 },
  ];

  return (
    <div className="netzero-container">
      <h2>🌍 Net Zero Tracker</h2>

      {milestones.map((milestone, index) => {
        const progress = Math.min(
          ((milestone.target - milestone.actual) / milestone.target) * 100,
          100
        ).toFixed(0);

        return (
          <div key={index} className="milestone">
            <h4>🎯 Target Year: {milestone.year}</h4>
            <p>Target Emission: {milestone.target} kg CO₂e</p>
            <p>Current Emission: {milestone.actual} kg CO₂e</p>

            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${100 - progress}%`,
                  backgroundColor: progress >= 100 ? '#37b24d' : '#f03e3e',
                }}
              >
                {100 - progress}%
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default NetZero;
