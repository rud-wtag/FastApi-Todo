import { filterActionTypes } from '../constants/ActionTypes';

const { ALL } = filterActionTypes;
const { SET_FILTER } = filterActionTypes;
const initialState = {
  filterState: ALL
};

export const filterReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_FILTER:
      return {
        ...state,
        filterState: action.payload
      };
    default:
      return state;
  }
};
