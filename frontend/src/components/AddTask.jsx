import { useDispatch } from 'react-redux';
import TaskForm from 'components/TaskForm';
import { addTodo, toast } from 'redux/actions/TodoAction';
import { INITIAL_TASK, TOAST_TYPE_SUCCESS } from 'utils/constants';

function AddTask() {
  const dispatch = useDispatch();

  const onSubmit = (title) => {
    dispatch(addTodo(title));
    dispatch(toast({ type: TOAST_TYPE_SUCCESS, message: 'Task added successfully' }));
  };

  return <TaskForm task={INITIAL_TASK} submitTask={onSubmit} />;
}

export default AddTask;
