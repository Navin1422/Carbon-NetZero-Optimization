// src/components/Dashboard.jsx
import React, { useContext, useEffect, useRef } from 'react';
import { CSVContext } from './context/CSVContext';
import Chart from 'chart.js/auto';
import './Dashboard.css';

const Dashboard = () => {
  const { csvData } = useContext(CSVContext);
  const pieRef = useRef(null);
  const barRef = useRef(null);
  const pieChartRef = useRef(null);
  const barChartRef = useRef(null);

  // Total Scope 1, 2, 3 emissions
  const scope1 = csvData.reduce((sum, row) => sum + Number(row.Scope1 || 0), 0);
  const scope2 = csvData.reduce((sum, row) => sum + Number(row.Scope2 || 0), 0);
  const scope3 = csvData.reduce((sum, row) => sum + Number(row.Scope3 || 0), 0);

  // Department-wise total emissions
  const departmentData = {};
  csvData.forEach(row => {
    const dept = row.Department || 'Unknown';
    const total = Number(row.Scope1 || 0) + Number(row.Scope2 || 0) + Number(row.Scope3 || 0);
    departmentData[dept] = (departmentData[dept] || 0) + total;
  });

  const departmentLabels = Object.keys(departmentData);
  const departmentEmissions = Object.values(departmentData);

  // Pie chart for Scope-wise emissions
  useEffect(() => {
    if (pieChartRef.current) pieChartRef.current.destroy();
    const ctx = pieRef.current.getContext('2d');

    pieChartRef.current = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['Scope 1', 'Scope 2', 'Scope 3'],
        datasets: [{
          data: [scope1, scope2, scope3],
          backgroundColor: ['#ff6b6b', '#4dabf7', '#82c91e'],
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' },
          title: { display: true, text: 'Scope-wise Emission Breakdown' }
        }
      }
    });
  }, [scope1, scope2, scope3]);

  // Bar chart for Department-wise emissions
  useEffect(() => {
    if (barChartRef.current) barChartRef.current.destroy();
    const ctx = barRef.current.getContext('2d');

    barChartRef.current = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: departmentLabels,
        datasets: [{
          label: 'Total Emissions (kg CO₂e)',
          data: departmentEmissions,
          backgroundColor: '#74c0fc',
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: { display: true, text: 'Emissions by Department' },
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: value => `${value} kg`
            }
          }
        }
      }
    });
  }, [departmentLabels, departmentEmissions]); // ✅ fixed warning here

  return (
    <div className="dashboard-container">
      <h2>📊 Emission Dashboard</h2>

      <div className="summary-cards">
        <div className="card scope1">🔥 Scope 1: {scope1} kg CO₂e</div>
        <div className="card scope2">⚡ Scope 2: {scope2} kg CO₂e</div>
        <div className="card scope3">🚚 Scope 3: {scope3} kg CO₂e</div>
      </div>

      <div className="chart-wrapper">
        <canvas ref={pieRef} />
      </div>

      <div className="chart-wrapper">
        <canvas ref={barRef} />
      </div>
    </div>
  );
};

export default Dashboard;
