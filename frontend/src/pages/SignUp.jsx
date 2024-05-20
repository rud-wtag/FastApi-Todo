import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { ReactComponent as Logo } from 'assets/logo.svg';
import Heading from 'components/Heading';
import ToastContainer from 'components/ToastContainer';

import axios from 'axios';
import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { toast } from 'redux/actions/TodoAction';
import { TOAST_TYPE_ERROR, TOAST_TYPE_SUCCESS } from 'utils/constants';

export default function SignUp() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [full_name, setFullName] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const submitHandler = (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append('full_name', password);
    formData.append('email', email);
    formData.append('password', password);

    axios
      .post('/auth/register', { full_name, email, password })
      .then((response) => {
        if (response.status == 200) {
          navigate('/sign-in');
          dispatch(toast({ type: TOAST_TYPE_SUCCESS, message: 'Registration successful' }));
        }
      })
      .catch((error) => {
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: 'Failed to signup' }));
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
          <div className="label">Todo</div>
        </div>
        <div className="sign-in__container">
          <TextField
            variant="outlined"
            size="small"
            fullWidth="true"
            label="Full Name"
            onChange={(e) => {
              setFullName(e.target.value);
            }}
          />
          <TextField
            variant="outlined"
            size="small"
            fullWidth="true"
            label="Email"
            onChange={(e) => {
              setEmail(e.target.value);
            }}
          />
          <TextField
            variant="outlined"
            size="small"
            fullWidth="true"
            label="Password"
            type="password"
            onChange={(e) => {
              setPassword(e.target.value);
            }}
          />
          <Button
            variant="outlined"
            onClick={(e) => {
              submitHandler(e);
            }}
          >
            Sign Up
          </Button>
        </div>
      </div>
    </>
  );
}
