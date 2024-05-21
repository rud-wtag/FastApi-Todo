import propTypes from 'prop-types';
import { useDispatch } from 'react-redux';
import { ReactComponent as DeleteIcon } from 'assets/delete.svg';
import { ReactComponent as EditIcon } from 'assets/edit.svg';
import { ReactComponent as DoneIcon } from 'assets/ok.svg';
import Button from 'components/ui/Button';
import { deleteTodo, setEditMode, setTodoComplete } from 'redux/actions/TodoAction';
import { daysBetweenDate } from 'utils/helpers';
import ActionMenu from 'components/ActionMenu';
import { useEffect, useState } from 'react';
import AlertDialog from './AlertDialog';

export default function TaskFooter({ completed_at = null, created_at, taskId }) {
  const dispatch = useDispatch();
  const [open, setOpen] = useState(false);
  const [proceed, setProceed] = useState(false);

  function onDelete(event) {
    event.preventDefault();
    setOpen(true);
  }

  function onProceed(event) {
    event.preventDefault();
    setProceed(true);
    setOpen(false);
  }

  function onClose(event) {
    event.preventDefault();

    setProceed(false);
    setOpen(false);
  }

  function onComplete(event) {
    event.preventDefault();
    dispatch(setTodoComplete(taskId));
  }

  function onEdit(event) {
    event.preventDefault();
    dispatch(setEditMode({ taskId: taskId, isEditMode: true }));
  }

  useEffect(() => {
    if (proceed == true) {
      dispatch(deleteTodo(taskId));
      setProceed(false);
    }
  }, [proceed]);

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
        <AlertDialog
          title={'Delete task !!'}
          description={'Task will no longer accessible and backed up'}
          open={open}
          handleConfirm={(e) => onProceed(e)}
          handleClose={(e) => onClose(e)}
        />
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
