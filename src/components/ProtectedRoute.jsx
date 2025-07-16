// src/components/ProtectedRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ element: Element, allowedRoles }) => {
  const userRole = localStorage.getItem('userRole');

  // If not logged in, redirect to login
  if (!userRole) {
    return <Navigate to="/login" replace />;
  }

  // If role is not allowed, redirect to home (or access-denied page if you make one)
  if (!allowedRoles.includes(userRole)) {
    alert('❌ Access Denied: You are not authorized to view this page.');
    return <Navigate to="/" replace />;
  }

  return <Element />;
};

export default ProtectedRoute;
