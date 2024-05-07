import classNames from 'classnames';
import PropTypes from 'prop-types';
import EditTask from 'components/EditTask';
import TaskFooter from 'components/ui/TaskFooter';
import { getFormattedDate } from 'utils/helpers';

function Task({ task }) {
  const { id, title, createdAt, completedAt, isEditMode } = task;

  return (
    <>
      {isEditMode ? (
        <EditTask task={task} />
      ) : (
        <div className="task">
          <div
            className={classNames('task__title', {
              'task__title--completed': completedAt
            })}
          >
            {title}
          </div>
          <p className="task__created">Created At: {getFormattedDate(createdAt)}</p>
          <TaskFooter
            completedAt={completedAt}
            isEditMode={isEditMode}
            createdAt={createdAt}
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
    id: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    isEditMode: PropTypes.bool,
    createdAt: PropTypes.instanceOf(Date).isRequired,
    completedAt: PropTypes.instanceOf(Date)
  })
};

Task.defaultProps = {
  task: {
    completedAt: null,
    isEditMode: false
  }
};
