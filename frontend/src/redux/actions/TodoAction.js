import { v4 as uuidv4 } from 'uuid';
import { actionTypes } from 'redux/constants/ActionTypes';
import supabase from 'supabase';
import { INITIAL_TASK } from 'utils/constants';

export const addTodo = (title) => {
  return async (dispatch) => {
    const task = {
      id: uuidv4(),
      title,
      createdAt: new Date().toISOString()
    };

    const { error } = await supabase.from('todos').insert([task]).select();

    if (!error) {
      dispatch({
        type: actionTypes.ADD_TODO,
        payload: {
          ...INITIAL_TASK,
          ...task
        }
      });
      dispatch(toast({ type: 'success', message: 'Task added successfully' }));
    } else {
      dispatch(toast({ type: 'danger', message: 'Failed to add task' }));
    }
  };
};

export const editTodo = (task) => {
  return async (dispatch) => {
    const { error } = await supabase
      .from('todos')
      .update({ title: task.title })
      .eq('id', task.taskId)
      .select();
    if (!error) {
      dispatch({
        type: actionTypes.EDIT_TODO,
        payload: task
      });
      dispatch(toast({ type: 'success', message: 'Task updated successfully' }));
    } else {
      dispatch(toast({ type: 'danger', message: 'Failed to add task' }));
    }
  };
};

export const deleteTodo = (todoId) => {
  return async (dispatch) => {
    const { error } = await supabase.from('todos').delete().eq('id', todoId);
    if (!error) {
      dispatch({
        type: actionTypes.DELETE_TODO,
        payload: todoId
      });
      dispatch(toast({ type: 'danger', message: 'Task deleted' }));
    }
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
    const { error } = await supabase
      .from('todos')
      .update({ completedAt: new Date() })
      .eq('id', taskId)
      .select();
    if (!error) {
      dispatch({
        type: actionTypes.COMPLETE_TASK,
        payload: { taskId: taskId, completedAt: new Date() }
      });
      dispatch(toast({ type: 'success', message: 'task completed' }));
    } else {
      dispatch(toast({ type: 'danger', message: error.message }));
    }
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
