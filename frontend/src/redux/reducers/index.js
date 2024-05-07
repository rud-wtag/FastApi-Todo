import { combineReducers } from 'redux';
import { filterReducer } from 'redux/reducers/FilterReducer';
import { searchReducer } from 'redux/reducers/SearchReducer';
import { todoReducer } from 'redux/reducers/TodoReducer';

const reducer = combineReducers({
  todoStates: todoReducer,
  filterStates: filterReducer,
  searchStates: searchReducer
});

export default reducer;
