import { appActionTypes } from 'redux/constants/ActionTypes';

export const setLoggedIn = (auth_state) => {
  return {
    type: appActionTypes.SET_LOGGED_IN,
    payload: auth_state
  };
};

export const setProfile = (profile) => {
  return {
    type: appActionTypes.SET_PROFILE,
    payload: profile
  };
};
