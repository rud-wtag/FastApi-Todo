import { Box } from '@mui/material';
import Pagination from '@mui/material/Pagination';
import axios from 'axios';
import AddTask from 'components/AddTask';
import NoTaskPlaceholder from 'components/NoTaskPlaceholder';
import Task from 'components/Task';
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { loadTasksFromDB, toast, setPager } from 'redux/actions/TodoAction';
import { TOAST_TYPE_ERROR } from 'utils/constants';
import { filterTasks } from 'utils/helpers/ReducerHelper';

export default function TaskContainer() {
  const tasks = useSelector((state) => state.todoStates.todos);
  const pager = useSelector((state) => state.todoStates);
  const filter = useSelector((state) => state.filterStates.filterState);
  const priority = useSelector((state) => state.filterStates.priority);
  const dueDate = useSelector((state) => state.filterStates.dueDate);
  const search = useSelector((state) => state.searchStates);
  const isNewTaskRequested = useSelector((state) => state.todoStates.isNewTaskRequested);
  const [page, setPage] = useState(1);
  const isTasksAvailable = tasks.length || isNewTaskRequested;
  const isPaginationAvailable = true;
  const dispatch = useDispatch();

  const handleChange = (e, value) => {
    e.preventDefault();
    setPage(value);
  };

  useEffect(() => {
    axios
      .get(
        `/tasks?search_query=${search.query}&page=${page}&size=${pager.size}${filterTasks(filter) != null ? `&status=${filterTasks(filter)}` : ``}${priority != null ? `&priority_level=${priority}` : ``}${dueDate != null ? `&due_date=${dueDate}` : ``}`
      )
      .then((response) => {
        if (response.status == 200) {
          dispatch(loadTasksFromDB(response.data.items));
          dispatch(setPager({ page: response.data.page, pages: response.data.pages }));
        }
      })
      .catch((error) => {
        console.log(error);
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: 'Failed to update task' }));
      });
  }, [search, page, filter, priority, dueDate]);

  return (
    <>
      {!isTasksAvailable && <NoTaskPlaceholder />}
      <div className="container">
        <div className="task_container grid grid-gap grid-cols-1 grid-cols-md-2 grid-cols-lg-3">
          {isNewTaskRequested && <AddTask />}
          {tasks.map((task) => (
            <Task
              task={{
                ...task,
                created_at: task.created_at ? new Date(task.created_at) : task.created_at,
                completed_at: task.completed_at ? new Date(task.completed_at) : task.completed_at
              }}
              key={task.id}
            />
          ))}
        </div>
        {isPaginationAvailable && (
          <Box sx={{ margin: '2rem 0', display: 'flex', justifyContent: 'center' }}>
            <Pagination
              count={pager.pages}
              page={page}
              onChange={(e, value) => handleChange(e, value)}
              color="secondary"
            />
          </Box>
        )}
      </div>
    </>
  );
}
