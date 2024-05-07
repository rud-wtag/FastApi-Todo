import { searchActionTypes } from '../constants/ActionTypes';
const { SET_SEARCH, SET_SEARCHING } = searchActionTypes;

const initialState = {
  query: null,
  searching: false
};

export const searchReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_SEARCH:
      return {
        ...state,
        query: action.payload
      };
    case SET_SEARCHING:
      return {
        ...state,
        searching: action.payload
      };
    default:
      return state;
  }
};
