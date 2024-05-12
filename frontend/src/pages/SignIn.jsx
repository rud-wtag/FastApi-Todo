import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { ReactComponent as Logo } from 'assets/logo.svg';
import { setLoggedIn } from 'redux/actions/AppAction';
import ToastContainer from 'components/ToastContainer';
import Heading from 'components/Heading';

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
        console.log(response, response.status);
        if (response.status == 200) {
          dispatch(setLoggedIn(true));
          navigate('/');
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };
  return (
    <>
      <Heading />
      <div className="sign-in">
        <ToastContainer />
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
        </div>
      </div>
    </>
  );
}
