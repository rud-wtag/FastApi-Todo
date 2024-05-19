import * as React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useEffect, useState } from 'react';
import AddTask from 'components/AddTask';
import NoTaskPlaceholder from 'components/NoTaskPlaceholder';
import Task from 'components/Task';
import axios from 'axios';
import { loadTasksFromDB, toast } from 'redux/actions/TodoAction';
import Pagination from '@mui/material/Pagination';
import { TOAST_TYPE_ERROR } from 'utils/constants';
import { filterTasks } from 'utils/helpers/ReducerHelper';
import { Box } from '@mui/material';

export default function TaskContainer() {
  const tasks = useSelector((state) => state.todoStates.todos);
  const pager = useSelector((state) => state.todoStates);
  const filter = useSelector((state) => state.filterStates.filterState);
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
        `/tasks?search_query=${search.query}&page=${page}&size=${pager.size}${
          filterTasks(filter) != null ? `&status=${filterTasks(filter)}` : ``
        }`
      )
      .then((response) => {
        if (response.status == 200) {
          console.log(response.data.items);
          dispatch(loadTasksFromDB(response.data.items));
        }
      })
      .catch((error) => {
        console.log(error);
        dispatch(toast({ type: TOAST_TYPE_ERROR, message: 'Failed to update task' }));
      });
  }, [search, page, filter]);

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
                createdAt: task.createdAt ? new Date(task.createdAt) : task.createdAt,
                completedAt: task.completedAt ? new Date(task.completedAt) : task.completedAt
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
