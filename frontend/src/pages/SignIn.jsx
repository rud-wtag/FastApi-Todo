import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { ReactComponent as Logo } from 'assets/logo.svg';
import { setLoggedIn } from 'redux/actions/AppAction';
import ToastContainer from 'components/ToastContainer';
import Heading from 'components/Heading';
import { Box } from '@mui/material';
import { toast } from 'redux/actions/TodoAction';
import { TOAST_TYPE_ERROR } from 'utils/constants';

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const submitHandler = (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    axios
      .post('/auth/login', formData)
      .then((response) => {
        if (response.status == 200) {
          dispatch(setLoggedIn(true));
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
          <Box sx={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
            <p>Forget Password?</p> <Link to="/send-reset-link">Click here</Link>
          </Box>
        </div>
      </div>
    </>
  );
}
