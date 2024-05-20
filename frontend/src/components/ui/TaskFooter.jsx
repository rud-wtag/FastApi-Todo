import propTypes from 'prop-types';
import { useDispatch } from 'react-redux';
import { ReactComponent as DeleteIcon } from 'assets/delete.svg';
import { ReactComponent as EditIcon } from 'assets/edit.svg';
import { ReactComponent as DoneIcon } from 'assets/ok.svg';
import Button from 'components/ui/Button';
import { deleteTodo, setEditMode, setTodoComplete } from 'redux/actions/TodoAction';
import { daysBetweenDate } from 'utils/helpers';
import ActionMenu from 'components/ActionMenu';

export default function TaskFooter({ completed_at = null, created_at, taskId }) {
  const dispatch = useDispatch();

  function onDelete(event) {
    event.preventDefault();
    alert('Task will removed!');
    dispatch(deleteTodo(taskId));
  }

  function onComplete(event) {
    event.preventDefault();
    dispatch(setTodoComplete(taskId));
  }

  function onEdit(event) {
    event.preventDefault();
    dispatch(setEditMode({ taskId: taskId, isEditMode: true }));
  }

  return (
    <div className="task__footer">
      <div className="task__footer-left">
        {!completed_at && (
          <>
            <Button variant="icon" onClick={onComplete}>
              <DoneIcon />
            </Button>
            <Button variant="icon" onClick={onEdit}>
              <EditIcon />
            </Button>
          </>
        )}
        <Button variant="icon" onClick={onDelete}>
          <DeleteIcon />
        </Button>
        <ActionMenu />
      </div>
      {completed_at && (
        <div className="task__footer-right">
          completed in: {daysBetweenDate(completed_at, created_at)}
        </div>
      )}
    </div>
  );
}

TaskFooter.propTypes = {
  completed_at: propTypes.instanceOf(Date),
  taskId: propTypes.number.isRequired,
  created_at: propTypes.instanceOf(Date).isRequired
};
