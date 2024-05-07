import PropTypes from 'prop-types';
import { useEffect, useRef, useState } from 'react';
import { useDispatch } from 'react-redux';
import { ReactComponent as DeleteIcon } from 'assets/delete.svg';
import { ReactComponent as DoneIcon } from 'assets/ok.svg';
import Button from 'components/ui/Button';
import { setEditMode, setIsNewTaskRequested, setTodoComplete } from 'redux/actions/TodoAction';
import { KEY_ENTER, RESPONSE_ERROR } from 'utils/constants';
import { validate } from 'utils/helpers/index';

function TaskForm({ isEditMode = false, task, submitTask }) {
  const [error, setError] = useState(null);
  const [title, setTaskTitle] = useState(task?.title);
  const dispatch = useDispatch();
  const textAreaRef = useRef(null);

  function onSubmit(event) {
    event.preventDefault();
    const validateDetails = validate(title);

    if (validateDetails.status === RESPONSE_ERROR) {
      setError(validateDetails.message);
    } else {
      setError(null);
      submitTask(validateDetails.text);
      dispatch(setIsNewTaskRequested(false));
      setTaskTitle('');
    }
  }

  function onKeyDown(event) {
    if (event.key === KEY_ENTER) {
      onSubmit(event);
    }
  }

  function onCancel(event) {
    event.preventDefault();
    dispatch(setIsNewTaskRequested(false));
  }

  function onInputChange(event) {
    event.preventDefault();
    setTaskTitle(event.target.value);
  }

  function onComplete(event) {
    event.preventDefault();
    onSubmit(event);
    dispatch(setEditMode({ taskId: task.id, isEditMode: false }));
    dispatch(setTodoComplete(task.id));
  }

  useEffect(() => {
    textAreaRef.current.focus();
  }, []);

  return (
    <div className="task">
      <form onSubmit={onSubmit}>
        <textarea
          className="task__input"
          ref={textAreaRef}
          onChange={onInputChange}
          onKeyDown={onKeyDown}
          required
          value={title}
        />
        {error && <span>{error}</span>}
        <div className="task__footer">
          <div className="task__footer-left">
            {isEditMode ? (
              <>
                <Button>Save</Button>
                <Button variant="icon" onClick={onComplete}>
                  <DoneIcon />
                </Button>
              </>
            ) : (
              <Button variant="secondary">Add Task</Button>
            )}
            <Button variant="icon" onClick={onCancel}>
              <DeleteIcon />
            </Button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default TaskForm;

TaskForm.propTypes = {
  task: PropTypes.shape({
    title: PropTypes.string,
    createdAt: PropTypes.instanceOf(Date),
    completedAt: PropTypes.instanceOf(Date),
    id: PropTypes.string,
    isEditMode: PropTypes.bool
  }),
  isEditMode: PropTypes.bool,
  submitTask: PropTypes.func.isRequired
};

TaskForm.defaultProps = {
  task: {
    title: '',
    createdAt: null,
    completedAt: null,
    isEditMode: false
  }
};
