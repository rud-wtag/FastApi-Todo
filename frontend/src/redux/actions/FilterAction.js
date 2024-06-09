import { filterActionTypes } from 'redux/constants/ActionTypes';

export const setFilter = (filterState) => {
  return {
    type: filterActionTypes.SET_FILTER,
    payload: filterState
  };
};

export const setPriority = (priority) => {
  return {
    type: filterActionTypes.SET_PRIORITY,
    payload: priority
  };
};

export const setDueDate = (dueDate) => {
  return {
    type: filterActionTypes.SET_DUE_DATE,
    payload: dueDate
  };
};
