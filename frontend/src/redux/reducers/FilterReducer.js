import { filterActionTypes } from '../constants/ActionTypes';

const { ALL, SET_FILTER, SET_PRIORITY, SET_DUE_DATE } = filterActionTypes;
const initialState = {
  filterState: ALL,
  priority: null,
  dueDate: null
};

export const filterReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_FILTER:
      return {
        ...state,
        filterState: action.payload
      };
    case SET_PRIORITY:
      return {
        ...state,
        priority: action.payload
      };
    case SET_DUE_DATE:
      return {
        ...state,
        dueDate: action.payload
      };
    default:
      return state;
  }
};
