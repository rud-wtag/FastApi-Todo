import { actionTypes } from 'redux/constants/ActionTypes';
import { INITIAL_TASK, TOAST_TYPE_ERROR } from 'utils/constants';
import axios from 'axios';
import dayjs from 'dayjs';
export const addTodo = (title, description, due_date, priority_level, category) => {
  return async (dispatch) => {
    const task = {
      title,
      description,
      due_date,
      priority_level,
      category,
      createdAt: new Date().toISOString()
    };
    console.log(task)
    axios
      .post('/tasks', task)
      .then((res) => {
        if (res.status == 200)
          dispatch({
            type: actionTypes.ADD_TODO,
            payload: {
              ...INITIAL_TASK,
              ...res.data
            }
          });
        dispatch(toast({ type: 'success', message: 'Task added successfully' }));
      })
      .catch((error) => {
        console.log(error);
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: 'Failed to add task' }));
      });
  };
};

export const editTodo = (task_id, updated_task) => {
  return async (dispatch) => {
    axios
      .put(`/tasks/${task_id}`, updated_task)
      .then((res) => {
        if (res.status == 200)
          dispatch({
            type: actionTypes.EDIT_TODO,
            payload: res.data
          });
        dispatch(toast({ type: 'success', message: 'Task updated successfully' }));
      })
      .catch((error) => {
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: error.response.data.detail?.[0]?.msg }));
      });
  };
};

export const deleteTodo = (todoId) => {
  return async (dispatch) => {
    axios
      .delete(`/tasks/${todoId}`)
      .then((res) => {
        if (res.status == 200)
          dispatch({
            type: actionTypes.DELETE_TODO,
            payload: todoId
          });
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: 'Task deleted' }));
      })
      .catch((error) => {
        console.log(error);
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: 'Failed to delete task' }));
      });
  };
};

export const setIsNewTaskRequested = (isNewTaskRequested) => {
  return {
    type: actionTypes.SET_ADD_TASK,
    payload: isNewTaskRequested
  };
};

export const setTodoComplete = (taskId) => {
  return async (dispatch) => {
    axios
      .put(`/tasks/${taskId}/complete`)
      .then((res) => {
        if (res.status == 200)
          dispatch({
            type: actionTypes.COMPLETE_TASK,
            payload: res.data
          });
        dispatch(toast({ type: 'success', message: 'task completed' }));
      })
      .catch((error) => {
        console.log(error);
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: 'Failed to update task' }));
      });
  };
};

export const setEditMode = (taskId) => {
  return {
    type: actionTypes.SET_EDIT,
    payload: taskId
  };
};

export const nextPage = (todos) => {
  return {
    type: actionTypes.NEXT_PAGE,
    payload: todos
  };
};

export const toast = (toastState) => {
  return {
    type: actionTypes.TOAST_MESSAGE,
    payload: toastState
  };
};

export const loadTasksFromDB = (tasks) => {
  return {
    type: actionTypes.LOAD_TASKS_FROM_DB,
    payload: tasks
  };
};

export const setPager = (pager) => {
  return {
    type: actionTypes.SET_PAGER,
    payload: pager
  };
};
