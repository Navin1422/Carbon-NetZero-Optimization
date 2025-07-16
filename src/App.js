// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Dashboard from './components/Dashboard';
import Form from './components/Form';
import Offset from './components/Offset';
import Reports from './components/Reports';
import NetZero from './components/NetZero';
import Tracker from './components/Tracker';
import Aiagent from './components/Aiagent';
import Login from './components/Login';
import ProtectedRoute from './components/ProtectedRoute';
import { CSVProvider } from './components/context/CSVContext';

function App() {
  const userRole = localStorage.getItem('userRole');

  // ⛔️ Check current path to hide navbar on login page
  const location = window.location.pathname;
  const showNavbar = location !== '/login';

  return (
    <CSVProvider>
      <Router>
        {/* ✅ Show Navbar only when logged in and not on login page */}
        {userRole && showNavbar && <Navbar />}

        <Routes>
          {/* Always accessible Login route */}
          <Route path="/login" element={<Login />} />

          {/* ✅ Protected Routes */}
          <Route path="/" element={<ProtectedRoute element={Home} allowedRoles={['admin', 'manager', 'auditor']} />} />
          <Route path="/dashboard" element={<ProtectedRoute element={Dashboard} allowedRoles={['admin', 'manager', 'auditor']} />} />
          <Route path="/form" element={<ProtectedRoute element={Form} allowedRoles={['admin', 'manager']} />} />
          <Route path="/offset" element={<ProtectedRoute element={Offset} allowedRoles={['admin', 'manager']} />} />
          <Route path="/reports" element={<ProtectedRoute element={Reports} allowedRoles={['admin', 'manager', 'auditor']} />} />
          <Route path="/netzero" element={<ProtectedRoute element={NetZero} allowedRoles={['admin', 'manager', 'auditor']} />} />
          <Route path="/tracker" element={<ProtectedRoute element={Tracker} allowedRoles={['admin', 'manager', 'auditor']} />} />
          <Route path="/ai-agent" element={<ProtectedRoute element={Aiagent} allowedRoles={['admin', 'manager', 'auditor']} />} />

          {/* ✅ Fallback to redirect */}
          <Route path="*" element={<Navigate to={userRole ? '/' : '/login'} replace />} />
        </Routes>
      </Router>
    </CSVProvider>
  );
}

export default App;
