import PropTypes from 'prop-types';
import { useEffect, useRef, useState } from 'react';
import { useDispatch } from 'react-redux';
import { ReactComponent as DeleteIcon } from 'assets/delete.svg';
import { ReactComponent as DoneIcon } from 'assets/ok.svg';
import Button from 'components/ui/Button';
import { setEditMode, setIsNewTaskRequested, setTodoComplete } from 'redux/actions/TodoAction';
import { KEY_ENTER, RESPONSE_ERROR } from 'utils/constants';
import { validate } from 'utils/helpers/index';
import { TextField } from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import dayjs from 'dayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

function TaskForm({ isEditMode = false, task, submitTask }) {
  const [error, setError] = useState(null);
  const [title, setTaskTitle] = useState(task?.title);
  const [description, setDescription] = useState(task?.description);
  const [priorityLevel, setPriorityLevel] = useState(task?.priority_level);
  const [dueDate, setDueDate] = useState(task?.due_date);
  const [category, setCategory] = useState(task?.category);
  const dispatch = useDispatch();
  const textAreaRef = useRef(null);

  function onSubmit(event) {
    event.preventDefault();
    const validateTitle = validate(title);
    const validateDetails = validate(description);

    if (validateTitle.status === RESPONSE_ERROR) {
      setError(validateTitle.message);
      return;
    }

    if (validateDetails.status === RESPONSE_ERROR) {
      setError(validateDetails.message);
      return;
    }
    setError(null);
    submitTask(validateTitle.text, validateDetails.text, dueDate, priorityLevel, category);
    dispatch(setIsNewTaskRequested(false));
    setTaskTitle('');
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
        <TextField
          sx={{ margin: '1rem 0' }}
          onChange={(e) => setTaskTitle(e.target.value)}
          variant="outlined"
          size="small"
          fullWidth="true"
          label="Title"
          value={title}
        />
        <textarea
          className="task__input"
          ref={textAreaRef}
          onChange={(e) => setDescription(e.target.value)}
          onKeyDown={onKeyDown}
          required
          value={description}
        />
        {error && <span>{error}</span>}
        <FormControl sx={{ margin: '1rem 0' }} fullWidth>
          <InputLabel id="demo-simple-select-label">Priority Level</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={priorityLevel}
            label="Priority Level"
            onChange={(e) => setPriorityLevel(e.target.value)}
          >
            <MenuItem value={'LOW'}>LOW</MenuItem>
            <MenuItem value={'MEDIUM'}>MEDIUM</MenuItem>
            <MenuItem value={'HIGH'}>HIGH</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{ margin: '1rem 0' }} fullWidth>
          <InputLabel id="demo-simple-select-label">Category</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={category}
            label="Category"
            onChange={(e) => setCategory(e.target.value)}
          >
            <MenuItem value={'personal'}>personal</MenuItem>
            <MenuItem value={'project'}>project</MenuItem>
          </Select>
        </FormControl>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DesktopDatePicker
            onChange={(newValue) => setDueDate(dayjs(newValue).toISOString())}
            defaultValue={dayjs()}
          />
        </LocalizationProvider>
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
    description: PropTypes.string,
    priority_level: PropTypes.string,
    category: PropTypes.string,
    createdAt: PropTypes.instanceOf(Date),
    due_date: PropTypes.instanceOf(Date),
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
