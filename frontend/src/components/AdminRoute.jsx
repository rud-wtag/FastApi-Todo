import React, { useEffect } from 'react';
import propTypes from 'prop-types';
import { useSelector } from 'react-redux';
import { Navigate, useLocation } from 'react-router-dom';
import { useCookies } from 'react-cookie';

const AdminRoute = ({ children }) => {
  const [cookies] = useCookies(['profile']);
  const isLoggedIn = useSelector((state) => state.appStates.isLoggedIn);
  useEffect(() => {}, [isLoggedIn]);
  let location = useLocation();

  if (!cookies.profile) {
    return <Navigate to="/sign-in" state={{ from: location }} replace />;
  }

  if (cookies.profile.role !== 'admin') {
    return <Navigate to="/" state={{ from: location }} replace />;
  }
  return children;
};

export default AdminRoute;

AdminRoute.propTypes = {
  children: propTypes.node
};
