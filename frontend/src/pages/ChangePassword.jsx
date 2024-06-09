import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { ReactComponent as Logo } from 'assets/logo.svg';
import axios from 'axios';
import Heading from 'components/Heading';
import ToastContainer from 'components/ToastContainer';
import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useLocation, useNavigate } from 'react-router-dom';
import { toast } from 'redux/actions/TodoAction';
import { TOAST_TYPE_ERROR, TOAST_TYPE_SUCCESS } from 'utils/constants';

export default function ChangePassword() {
  const dispatch = useDispatch();
  const [oldPassword, setOldPassword] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();
  const search = useLocation().search;
  const token = new URLSearchParams(search).get('token');
  console.log(token);

  const submitHandler = (e) => {
    e.preventDefault();
    if (password != confirmPassword) {
      dispatch(toast({ type: TOAST_TYPE_ERROR, message: "password didn't matched!" }));
      return;
    }
    let formData = new FormData();
    formData.append('old_password', oldPassword);
    formData.append('new_password', password);

    axios
      .post(`/auth/change-password`, formData)
      .then((response) => {
        console.log(response, response.status);
        if (response.status == 200) {
          navigate('/sign-in');
          dispatch(toast({ type: TOAST_TYPE_SUCCESS, message: 'Password reset successful!' }));
        }
      })
      .catch((error) => {
        console.log(error.response.data?.detail);
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: error.response.data.detail }));
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
              setOldPassword(e.target.value);
            }}
            variant="outlined"
            size="small"
            fullWidth="true"
            label="Old Password"
            type="password"
          />
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
          <TextField
            onChange={(e) => {
              setConfirmPassword(e.target.value);
            }}
            variant="outlined"
            size="small"
            fullWidth="true"
            label="Confirm New Password"
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
