import { filterActionTypes } from 'redux/constants/ActionTypes';
import { TASKS_PER_PAGE } from 'utils/constants';

const { ALL, COMPLETE, INCOMPLETE } = filterActionTypes;

export const deleteTask = (todos, payload) => {
  return todos.filter((todo) => todo.id !== payload);
};

export const completeTask = (todos, payload) => {
  const newList = todos.map((todo) => {
    if (todo.id === payload.id) {
      return {
        ...todo,
        ...payload
      };
    }
    return todo;
  });
  return newList;
};

export const editTask = (todos, task) => {
  const newList = todos.map((todo) => {
    if (todo.id === task.id) {
      return {
        ...todo,
        ...task
      };
    }
    return todo;
  });
  return newList;
};

export const setEditMode = (todos, task) => {
  const newList = todos.map((todo) => {
    if (todo.id === task.taskId) {
      return {
        ...todo,
        isEditMode: task.isEditMode
      };
    }
    return todo;
  });
  return newList;
};

export const nextPage = (todos, currentPage) => {
  const indexOfLastTask = currentPage * TASKS_PER_PAGE;

  if (todos.length > indexOfLastTask) return currentPage + 1;
  return 1;
};

export const filterTasks = (filterState = ALL) => {
  switch (filterState) {
    case ALL:
      return null;
    case COMPLETE:
      return true;
    case INCOMPLETE:
      return false;
    default:
      return null;
  }
};
