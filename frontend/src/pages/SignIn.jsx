import { Box } from '@mui/material';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { ReactComponent as Logo } from 'assets/logo.svg';
import axios from 'axios';
import Heading from 'components/Heading';
import ToastContainer from 'components/ToastContainer';
import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';
import { setLoggedIn } from 'redux/actions/AppAction';
import { toast } from 'redux/actions/TodoAction';
import { TOAST_TYPE_ERROR } from 'utils/constants';
import { useCookies } from 'react-cookie';

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [cookies, setCookie, removeCookie] = useCookies(['profile']);

  const submitHandler = (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    axios
      .post('/auth/login', formData)
      .then((response) => {
        if (response.status == 200) {
          console.log(response);
          setCookie('profile', response.data.user);
          dispatch(setLoggedIn(true));
          if(response.data.user.role == 'admin')
            navigate('/dashboard');
          else
            navigate('/');
        }
      })
      .catch((error) => {
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: 'Invalid credentials' }));
        console.log(error);
      });
  };
  return (
    <>
      <Heading />
      <ToastContainer />
      <div className="sign-in">
        <div className="logo">
          <Logo />
          <div className="label">Sign In</div>
        </div>
        <div className="sign-in__container">
          <TextField
            onChange={(e) => {
              setEmail(e.target.value);
            }}
            variant="outlined"
            size="small"
            fullWidth="true"
            label="Username"
          />
          <TextField
            onChange={(e) => {
              setPassword(e.target.value);
            }}
            variant="outlined"
            size="small"
            fullWidth="true"
            label="Password"
            type="password"
          />
          <Button
            onClick={(e) => {
              submitHandler(e);
            }}
            variant="outlined"
          >
            Sign In
          </Button>
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              gap: '2rem',
              alignItems: 'center'
            }}
          >
            <Box sx={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
              <p>Forget Password?</p> <Link to="/send-reset-link">Click here</Link>
            </Box>
            <Box sx={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
              <p>Don't have account?</p> <Link to="/sign-up">Sign Up</Link>
            </Box>
          </Box>
        </div>
      </div>
    </>
  );
}
