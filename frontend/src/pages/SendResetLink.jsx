import { useState } from 'react';
import { useDispatch } from 'react-redux';
import axios from 'axios';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { ReactComponent as Logo } from 'assets/logo.svg';
import ToastContainer from 'components/ToastContainer';
import Heading from 'components/Heading';
import { toast } from 'redux/actions/TodoAction';
import { TOAST_TYPE_SUCCESS } from 'utils/constants';

export default function SendResetLink() {
  const [email, setEmail] = useState('');
  const dispatch = useDispatch();

  const submitHandler = (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append('email', email);

    axios
      .post('/auth/send-password-reset-link', formData)
      .then((response) => {
        if (response.status == 200) {
          dispatch(toast({ type: TOAST_TYPE_SUCCESS, message: 'Reset email sent successfully' }));
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
          <div className="label">Forget password</div>
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
          <Button
            onClick={(e) => {
              submitHandler(e);
            }}
            variant="outlined"
          >
            Send reset link
          </Button>
        </div>
      </div>
    </>
  );
}
