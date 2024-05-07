import { filterActionTypes } from 'redux/constants/ActionTypes';
import { TASKS_PER_PAGE } from 'utils/constants';

const { ALL, COMPLETE, INCOMPLETE } = filterActionTypes;

export const deleteTask = (todos, payload) => {
  return todos.filter((todo) => todo.id !== payload);
};

export const completeTask = (todos, payload) => {
  const newList = todos.map((todo) => {
    if (todo.id === payload.taskId) {
      return {
        ...todo,
        completedAt: payload.completedAt
      };
    }
    return todo;
  });
  return newList;
};

export const editTask = (todos, task) => {
  const newList = todos.map((todo) => {
    if (todo.id === task.taskId) {
      return {
        ...todo,
        title: task.title
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

const filterTasks = (tasks, filterState = ALL) => {
  switch (filterState) {
    case ALL:
      return tasks;
    case COMPLETE:
      return tasks.filter((task) => {
        if (task.completedAt !== null) return task;
      });
    case INCOMPLETE:
      return tasks.filter((task) => {
        if (task.completedAt === null) return task;
      });
    default:
      return tasks;
  }
};

const searchTasks = (tasks, query) => {
  return tasks.filter((task) => task.title.includes(query));
};

export const paginate = (tasks, currentPage) => {
  const indexOfLastTask = currentPage * TASKS_PER_PAGE;

  return tasks.slice(0, indexOfLastTask);
};

export const searchAndFilter = (tasks, filter, search) => {
  let todos;

  if (search.query) {
    todos = searchTasks(tasks, search.query);
  } else {
    todos = tasks;
  }

  todos = filterTasks(todos, filter.filterState);
  return todos;
};
