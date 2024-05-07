import { searchActionTypes } from 'redux/constants/ActionTypes';

export const setSearch = (query) => {
  return {
    type: searchActionTypes.SET_SEARCH,
    payload: query
  };
};

export const setSearching = (isSearching) => {
  return {
    type: searchActionTypes.SET_SEARCHING,
    payload: isSearching
  };
};
