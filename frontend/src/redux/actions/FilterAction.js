import { filterActionTypes } from 'redux/constants/ActionTypes';

export const setFilter = (filterState) => {
  return {
    type: filterActionTypes.SET_FILTER,
    payload: filterState
  };
};
