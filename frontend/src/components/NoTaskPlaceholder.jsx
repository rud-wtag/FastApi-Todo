import { useDispatch } from 'react-redux';
import { ReactComponent as AddTaskSVG } from 'assets/create.svg';
import { setIsNewTaskRequested } from 'redux/actions/TodoAction';

function NoTaskPlaceholder() {
  const dispatch = useDispatch();

  function onNewTaskRequest() {
    dispatch(setIsNewTaskRequested(true));
  }

  return (
    <div className="no_task">
      <div onClick={onNewTaskRequest} className="no_task__svg">
        <AddTaskSVG />
      </div>
      <p className="no_task__text">You didn’t add any task. Please, add one.</p>
    </div>
  );
}

export default NoTaskPlaceholder;
