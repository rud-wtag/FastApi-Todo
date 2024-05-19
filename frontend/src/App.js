import axios from 'axios';
import ProtectedRoute from 'components/AuthRequired';
import FullProfile from 'components/FullProfile';
import ChangePassword from 'pages/ChangePassword';
import Home from 'pages/Home';
import ResetPassword from 'pages/ResetPassword';
import SendResetLink from 'pages/SendResetLink';
import SignIn from 'pages/SignIn';
import SignUp from 'pages/SignUp';
import UpdateProfile from 'pages/UpdateProfile';
import { useEffect } from 'react';
import { Provider, useDispatch, useSelector } from 'react-redux';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { setLoggedIn, setProfile } from 'redux/actions/AppAction';
import store from 'redux/store';
import 'styles/style.scss';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1';
axios.defaults.withCredentials = true;

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <Home />
      </ProtectedRoute>
    )
  },
  {
    path: 'sign-up',
    element: <SignUp />
  },
  {
    path: 'sign-in',
    element: <SignIn />
  },
  {
    path: 'reset-password',
    element: <ResetPassword />
  },
  {
    path: 'change-password',
    element: <ChangePassword />
  },
  {
    path: 'profile',
    element: <FullProfile />
  },
  {
    path: 'update-profile',
    element: <UpdateProfile />
  },
  {
    path: 'send-reset-link',
    element: <SendResetLink />
  }
]);

function App() {
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

  return (
    <RouterProvider router={router} /> // RouterProvider should be wrapped inside the Provider
  );
}

const WrappedApp = () => (
  <Provider store={store}>
    <App />
  </Provider>
);

export default WrappedApp;
