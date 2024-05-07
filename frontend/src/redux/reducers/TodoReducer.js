import { actionTypes } from 'redux/constants/ActionTypes';
import { completeTask, deleteTask, editTask, setEditMode } from 'utils/helpers/ReducerHelper';
const {
  ADD_TODO,
  SET_ADD_TASK,
  DELETE_TODO,
  COMPLETE_TASK,
  SET_EDIT,
  EDIT_TODO,
  TOAST_MESSAGE,
  LOAD_TASKS_FROM_DB
} = actionTypes;

const initialState = {
  isNewTaskRequested: false,
  todos: [],
  currentPage: 1,
  toast: {
    type: 'success',
    message: null
  }
};

export const todoReducer = (state = initialState, action) => {
  let newList;

  switch (action.type) {
    case ADD_TODO:
      return {
        ...state,
        todos: [{ ...action.payload }, ...state.todos]
      };

    case EDIT_TODO:
      newList = editTask(state.todos, action.payload);
      return { ...state, todos: newList };

    case SET_ADD_TASK:
      return {
        ...state,
        isNewTaskRequested: action.payload
      };

    case DELETE_TODO:
      newList = deleteTask(state.todos, action.payload);
      return {
        ...state,
        todos: newList
      };

    case COMPLETE_TASK:
      newList = completeTask(state.todos, action.payload);
      return { ...state, todos: newList };

    case SET_EDIT:
      newList = setEditMode(state.todos, action.payload);
      return { ...state, todos: newList };

    case TOAST_MESSAGE:
      return { ...state, toast: action.payload };

    case LOAD_TASKS_FROM_DB:
      return { ...state, todos: [...action.payload] };

    default:
      return state;
  }
};
