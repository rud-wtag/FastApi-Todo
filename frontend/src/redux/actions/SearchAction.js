import { searchActionTypes } from 'redux/constants/ActionTypes';
import axios from 'axios'
import { toast } from './TodoAction';
import {TOAST_TYPE_ERROR} from '../../utils/constants/index'

export const setSearch = (query) => {
  return async (dispatch) => {
    axios
      .get(`/tasks?search_query=${query}`)
      .then((res) => {
        if (res.status == 200)
          dispatch({
            type: searchActionTypes.SET_SEARCH,
            payload: res.data.items
          });
        dispatch(toast({ type: 'success', message: 'task completed' }));
      })
      .catch((error) => {
        console.log(error);
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: 'Failed to update task' }));
      });
  };
};

export const setSearching = (isSearching) => {
  return {
    type: searchActionTypes.SET_SEARCHING,
    payload: isSearching
  };
};
