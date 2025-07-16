import React, { useState } from 'react';
import './Form.css';
import api from '../services/api';
import { ClipLoader } from 'react-spinners'; // Spinner

function Form() {
  const [fileName, setFileName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setSelectedFile(file);
    setFileName(file.name);
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert('⚠️ Please select a CSV file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile); // 'file' must match backend field name

    try {
      setIsSubmitting(true);

      // ✅ FINAL: Correct URL & no headers override
      const response = await api.post('/upload-emissions/', formData);

      console.log('✅ API response:', response.data);
      alert('✅ File submitted successfully!');
    } catch (error) {
      console.error('❌ Submission error:', error.response?.data || error.message);
      alert('❌ Failed to submit file.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="form-container">
      <div className="form-card">
        <h2>📄 Upload Emissions Data</h2>

        <label htmlFor="csvFile">Choose CSV File:</label>
        <input
          type="file"
          id="csvFile"
          accept=".csv"
          onChange={handleFileChange}
          className="file-input"
        />

        {fileName && (
          <p className="filename">📁 <strong>{fileName}</strong></p>
        )}

        <button className="upload-btn" onClick={handleSubmit} disabled={isSubmitting}>
          {isSubmitting ? (
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ClipLoader size={18} color="#fff" /> Uploading...
            </span>
          ) : (
            '⬆️ Upload'
          )}
        </button>
      </div>
    </div>
  );
}

export default Form;
