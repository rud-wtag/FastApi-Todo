import { useDispatch } from 'react-redux';
import TaskForm from 'components/TaskForm';
import { addTodo, toast } from 'redux/actions/TodoAction';
import { INITIAL_TASK, TOAST_TYPE_SUCCESS } from 'utils/constants';

function AddTask() {
  const dispatch = useDispatch();

  const onSubmit = (title, description, due_date, priority_level, category) => {
    dispatch(addTodo(title, description, due_date, priority_level, category));
  };

  return <TaskForm task={INITIAL_TASK} submitTask={onSubmit} />;
}

export default AddTask;
