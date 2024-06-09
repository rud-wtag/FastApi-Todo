import { appActionTypes } from '../constants/ActionTypes';

const { SET_LOGGED_IN, SET_PROFILE } = appActionTypes;
const initialState = {
  isLoggedIn: false,
  profile: {}
};

export const appReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_LOGGED_IN:
      return {
        ...state,
        isLoggedIn: action.payload
      };
    case SET_PROFILE:
      return {
        ...state,
        profile: action.payload
      };
    default:
      return state;
  }
};
