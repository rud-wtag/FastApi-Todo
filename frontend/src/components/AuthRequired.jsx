import React, { useEffect } from 'react';
import propTypes from 'prop-types';
import { useSelector } from 'react-redux';
import { Navigate, useLocation } from 'react-router-dom';
import { useCookies } from 'react-cookie';

const ProtectedRoute = ({ children }) => {
  const [cookies] = useCookies(['profile']);
  const isLoggedIn = useSelector((state) => state.appStates.isLoggedIn);
  useEffect(() => {}, [isLoggedIn]);
  let location = useLocation();

  if (!cookies.profile) {
    return <Navigate to="/sign-in" state={{ from: location }} replace />;
  }
  return children;
};

export default ProtectedRoute;

ProtectedRoute.propTypes = {
  children: propTypes.node
};
