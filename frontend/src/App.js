import axios from 'axios';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setLoggedIn, setProfile } from 'redux/actions/AppAction';
import Router from 'routes/sections';
import 'styles/style.scss';

import 'global.css';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1';
axios.defaults.withCredentials = true;

export default function App() {
  const dispatch = useDispatch();
  const isLoggedIn = useSelector((state) => state.appStates.isLoggedIn);

  useEffect(() => {
    axios
      .get('/auth/profile', { withCredentials: true })
      .then((response) => {
        if (response.status === 200) {
          dispatch(setProfile(response.data));
          dispatch(setLoggedIn(true));
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  useEffect(() => {}, [isLoggedIn]);

  return <Router />;
}
