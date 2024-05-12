import React, { useEffect } from 'react';
import axios from 'axios';
import propTypes from 'prop-types';
import { useSelector } from 'react-redux';
import { Navigate, useLocation } from 'react-router-dom';
import { setLoggedIn } from 'redux/actions/AppAction';
import { useDispatch } from 'react-redux';

const ProtectedRoute = ({ children }) => {
  const isLoggedIn = useSelector((state) => state.appStates);
  const dispatch = useDispatch();
  useEffect(() => {
    axios
      .get('/auth/profile', { withCredentials: true })
      .then((response) => {
        console.log('test>>>', response);
        if (response.status === 200) {
          dispatch(setLoggedIn(true));
          console.log(isLoggedIn);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
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
