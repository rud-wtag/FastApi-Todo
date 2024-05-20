import classNames from 'classnames';
import EditTask from 'components/EditTask';
import TaskFooter from 'components/ui/TaskFooter';
import PropTypes from 'prop-types';
import { getFormattedDate } from 'utils/helpers';

function Task({ task }) {
  const {
    id,
    title,
    description,
    created_at,
    due_date,
    priority_level,
    category,
    completed_at,
    task_state,
    isEditMode
  } = task;

  return (
    <>
      {isEditMode ? (
        <EditTask task={task} />
      ) : (
        <div
          className={classNames('task', {
            'task--outdated': task_state === 'outdated'
          })}
        >
          <div
            className={classNames('task__title', {
              'task__title--completed': completed_at
            })}
          >
            {title}
          </div>
          <div
            className={classNames({
              'task__title--completed': completed_at
            })}
          >
            {description}
          </div>
          <p className="task__created">Priority: {priority_level}</p>
          <p className="task__created">Category: {category}</p>
          <p className="task__created">Created At: {getFormattedDate(created_at)}</p>
          <p className="task__created">Due date: {getFormattedDate(due_date)}</p>
          <TaskFooter
            completed_at={completed_at}
            isEditMode={isEditMode}
            created_at={created_at}
            taskId={id}
          />
        </div>
      )}
    </>
  );
}

export default Task;

Task.propTypes = {
  task: PropTypes.shape({
    id: PropTypes.number.isRequired,
    title: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    priority_level: PropTypes.string.isRequired,
    category: PropTypes.string.isRequired,
    isEditMode: PropTypes.bool,
    created_at: PropTypes.instanceOf(Date).isRequired,
    due_date: PropTypes.instanceOf(Date).isRequired,
    completed_at: PropTypes.instanceOf(Date)
  })
};

Task.defaultProps = {
  task: {
    completed_at: null,
    isEditMode: false
  }
};
