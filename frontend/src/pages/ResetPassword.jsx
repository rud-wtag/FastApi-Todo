import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import ToastContainer from 'components/ToastContainer';
import Heading from 'components/Heading';
import { ReactComponent as Logo } from 'assets/logo.svg';
import { toast } from 'redux/actions/TodoAction';
import { TOAST_TYPE_SUCCESS } from 'utils/constants';
import { useDispatch } from 'react-redux';

export default function ResetPassword() {
  const dispatch = useDispatch();
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const search = useLocation().search;
  const token = new URLSearchParams(search).get('token');

  const submitHandler = (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append('new_password', password);

    axios
      .post(`/auth/reset-password?token=${token}`, formData)
      .then((response) => {
        if (response.status == 200) {
          navigate('/sign-in');
          dispatch(toast({ type: TOAST_TYPE_SUCCESS, message: 'Password reset successful' }));
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
          <div className="label">Todo</div>
        </div>
        <div className="sign-in__container">
          <TextField
            onChange={(e) => {
              setPassword(e.target.value);
            }}
            variant="outlined"
            size="small"
            fullWidth="true"
            label="New Password"
            type="password"
          />
          <Button
            onClick={(e) => {
              submitHandler(e);
            }}
            variant="outlined"
          >
            Submit
          </Button>
        </div>
      </div>
    </>
  );
}
