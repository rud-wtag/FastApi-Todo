import Button from '@mui/material/Button';
import Popover from '@mui/material/Popover';
import { ReactComponent as UserIcon } from 'assets/user.svg';
import axios from 'axios';
import PopupState, { bindPopover, bindTrigger } from 'material-ui-popup-state';
import { useEffect } from 'react';
import { useCookies } from 'react-cookie';
import { useDispatch, useSelector } from 'react-redux';
import { useLocation, useNavigate } from 'react-router-dom';
import { setLoggedIn, setProfile } from 'redux/actions/AppAction';

export default function Profile() {
  const [cookies, setCookie, removeCookie] = useCookies(['cookie-name']);
  const profile = useSelector((state) => state.appStates.profile);
  const isLoggedIn = useSelector((state) => state.appStates.isLoggedIn);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const logout = (e) => {
    e.preventDefault();
    axios
      .get('/auth/logout')
      .then((res) => {
        if (res.status == 204) {
          removeCookie('profile');
          dispatch(setLoggedIn(false));
          navigate('/sign-in');
        }
      })
      .catch((err) => {
        console.log(err);
      });
  };

  useEffect(() => {
    axios
      .get('/auth/profile')
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

  return (
    <PopupState variant="popover" popupId="demo-popup-popover">
      {(popupState) => (
        <div className="profile">
          <Button variant="contained" {...bindTrigger(popupState)}>
            <UserIcon />
          </Button>
          <Popover
            {...bindPopover(popupState)}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'left'
            }}
            transformOrigin={{
              vertical: 'top',
              horizontal: 'left'
            }}
          >
            {isLoggedIn ? (
              <div className="profile__container">
                {profile.username}
                <div className="profile__container-btns">
                  <Button onClick={(e) => logout(e)} color="error">
                    Logout
                  </Button>
                  <Button
                    onClick={() =>
                      navigate('/profile', { replace: true, state: { from: location } })
                    }
                  >
                    Profile
                  </Button>
                </div>
              </div>
            ) : (
              <div>
                <Button
                  onClick={() => navigate('/sign-in', { replace: true, state: { from: location } })}
                >
                  SignIn
                </Button>
              </div>
            )}
          </Popover>
        </div>
      )}
    </PopupState>
  );
}
