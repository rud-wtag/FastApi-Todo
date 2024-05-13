import React, { useEffect } from 'react';
import propTypes from 'prop-types';
import { useSelector } from 'react-redux';
import { Navigate, useLocation } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const isLoggedIn = useSelector((state) => state.appStates.isLoggedIn);
  useEffect(() => {
    console.log('route_mounted====', isLoggedIn);
  }, [isLoggedIn]);
  let location = useLocation();

  if (!isLoggedIn) {
    return <Navigate to="/sign-in" state={{ from: location }} replace />;
  }
  return children;
};

export default ProtectedRoute;

ProtectedRoute.propTypes = {
  children: propTypes.node
};
