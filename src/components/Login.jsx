import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // ✅ import this
import './Login.css';

const Login = () => {
  const [role, setRole] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate(); // ✅ setup navigation

  const handleSubmit = (e) => {
    e.preventDefault();

    if (role && password) {
      localStorage.setItem('userRole', role); // ✅ store role (for access control if needed)
      navigate('/'); // ✅ redirect to Home page
    } else {
      alert('Please select a role and enter password');
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-card">
        <h2>🌿 Welcome to Carbon Tracker</h2>
        <form className="login-form" onSubmit={handleSubmit}>
          <label>Select Role:</label>
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="">Select</option>
            <option value="admin">Admin</option>
            <option value="manager">Manager</option>
            <option value="auditor">Auditor</option>
          </select>

          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="login-btn" type="submit">
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
