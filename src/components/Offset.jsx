// src/components/Offset.jsx
import React, { useState, useContext } from 'react';
import './Offset.css';
import { CSVContext } from './context/CSVContext';

const Offset = () => {
  const [treeCount, setTreeCount] = useState('');
  const [recCredits, setRecCredits] = useState('');
  const [netEmission, setNetEmission] = useState(null);

  const { csvData } = useContext(CSVContext);

  // Calculate total gross emissions from uploaded data
  const grossEmission = csvData.reduce((sum, row) => {
    const value = parseFloat(row.Emission) || 0;
    return sum + value;
  }, 0);

  const handleSubmit = () => {
    const treeOffset = Number(treeCount) * 0.021; // tons per tree per year
    const recOffset = Number(recCredits) * 1;      // 1 REC = 1 ton CO₂e
    const net = grossEmission - (treeOffset + recOffset);
    setNetEmission(net.toFixed(2));
  };

  return (
    <div className="offset-container">
      <h2>🌿 Carbon Offset Calculator</h2>

      <label>🌲 Number of Trees Planted:</label>
      <input
        type="number"
        value={treeCount}
        onChange={(e) => setTreeCount(e.target.value)}
        placeholder="e.g., 100"
      />

      <label>⚡ Number of RECs Purchased:</label>
      <input
        type="number"
        value={recCredits}
        onChange={(e) => setRecCredits(e.target.value)}
        placeholder="e.g., 2"
      />

      <button onClick={handleSubmit}>Calculate Net Emissions</button>

      {netEmission !== null && (
        <div className="result">
          <h4>📉 Net Emissions after Offset: {netEmission} tons CO₂e</h4>
          <p>🌐 Gross Emission: {grossEmission.toFixed(2)} tons</p>
          <p>🌲 Tree Offset: {(treeCount * 0.021).toFixed(2)} tons</p>
          <p>⚡ REC Offset: {recCredits} tons</p>
        </div>
      )}
    </div>
  );
};

export default Offset;
