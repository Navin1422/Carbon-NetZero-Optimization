// src/components/Tracker.jsx
import React from 'react';
import './Tracker.css';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Tracker = () => {
  const targetData = {
    labels: ['2028', '2032', '2040'],
    datasets: [
      {
        label: 'Target Reduction (%)',
        data: [25, 60, 100], // 🎯 change if your milestones vary
        backgroundColor: '#4caf50',
      },
      {
        label: 'Achieved (%)',
        data: [18, 30, 45], // 🔧 replace with real-time data later
        backgroundColor: '#2196f3',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Net Zero Milestone Progress' },
    },
  };

  return (
    <div className="tracker-container">
      <h2>📈 Net Zero Tracker</h2>
      <p>Track your emission reduction progress over key milestone years.</p>
      <div className="tracker-chart">
        <Bar data={targetData} options={options} />
      </div>
    </div>
  );
};

export default Tracker;
