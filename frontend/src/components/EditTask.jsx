import PropTypes from 'prop-types';
import { useDispatch } from 'react-redux';
import TaskForm from 'components/TaskForm';
import { editTodo, setEditMode } from 'redux/actions/TodoAction';

function EditTask({ task }) {
  const dispatch = useDispatch();

  function onSubmit(title, description, due_date, priority_level, category) {
    dispatch(editTodo(task.id, { title, description, due_date, priority_level, category }));
    dispatch(setEditMode({ taskId: task.id, isEditMode: false }));
  }

  return <TaskForm isEditMode={true} task={task} submitTask={onSubmit} />;
}

export default EditTask;

EditTask.propTypes = {
  task: PropTypes.shape({
    id: PropTypes.string.isRequired,
    title: PropTypes.string,
    isEditMode: PropTypes.bool,
    createdAt: PropTypes.instanceOf(Date),
    completedAt: PropTypes.instanceOf(Date)
  })
};

EditTask.defaultProps = {
  task: {
    id: null,
    title: '',
    isEditMode: false,
    createdAt: null,
    completedAt: null
  }
};
