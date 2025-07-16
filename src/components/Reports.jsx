import React, { useContext } from 'react';
import { CSVContext } from './context/CSVContext';
import './Reports.css';

const Reports = () => {
  const { csvData } = useContext(CSVContext);

  const downloadCSV = () => {
    if (csvData.length === 0) return;

    const headers = Object.keys(csvData[0]).join(',');
    const rows = csvData.map(row => Object.values(row).join(',')).join('\n');
    const csvContent = `${headers}\n${rows}`;

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', 'emission_report.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="reports-container">
      <h2>📄 Emission Reports</h2>

      {csvData.length === 0 ? (
        <p className="no-data">
          No emission data available. <br /> Please upload a CSV file in the <strong>Emission Form</strong> page.
        </p>
      ) : (
        <>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  {Object.keys(csvData[0]).map((header, idx) => (
                    <th key={idx}>{header}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {csvData.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {Object.values(row).map((cell, cellIndex) => (
                      <td key={cellIndex}>{cell}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button className="download-button" onClick={downloadCSV}>⬇️ Download as CSV</button>
        </>
      )}
    </div>
  );
};

export default Reports;
