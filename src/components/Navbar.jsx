// src/components/Navbar.jsx
import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const role = localStorage.getItem('userRole');
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('userRole');
    navigate('/login');
  };

  const isActive = (path) => (location.pathname === path ? 'active-link' : '');

  // Define role-based links
  const commonLinks = [
    { path: '/', label: 'Home' },
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/ai-agent', label: 'AI Agent' },
  ];

  const roleLinks = {
    admin: [
      { path: '/form', label: 'Emission' },
      { path: '/offset', label: 'Offset' },
      { path: '/reports', label: 'Reports' },
      { path: '/tracker', label: 'Tracker' },
      { path: '/netzero', label: 'Net Zero' },
    ],
    manager: [
      { path: '/form', label: 'Emission' },
      { path: '/offset', label: 'Offset' },
      { path: '/reports', label: 'Reports' },
      { path: '/tracker', label: 'Tracker' },
      { path: '/netzero', label: 'Net Zero' },
    ],
    auditor: [
      { path: '/reports', label: 'Reports' },
      { path: '/tracker', label: 'Tracker' },
      { path: '/netzero', label: 'Net Zero' },
    ],
  };

  return (
    <nav className="navbar">
      <h2 className="logo">🌿 Carbon Net Zero</h2>

      <ul className="nav-links">
        {commonLinks.map((link) => (
          <li key={link.path}>
            <Link className={isActive(link.path)} to={link.path}>{link.label}</Link>
          </li>
        ))}

        {role &&
          roleLinks[role]?.map((link) => (
            <li key={link.path}>
              <Link className={isActive(link.path)} to={link.path}>{link.label}</Link>
            </li>
          ))}

        {/* Role badge + logout */}
        {role && (
          <>
            <li><span className="role-badge">{role.toUpperCase()}</span></li>
            <li><button className="logout-btn" onClick={handleLogout}>Logout</button></li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;