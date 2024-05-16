import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import BottomNav from 'components/BottomNav';
import ToastContainer from 'components/ToastContainer';
import TaskContainer from 'components/TaskContainer';
import Heading from 'components/Heading';
import Loader from 'components/ui/Loader';
import { loadTasksFromDB, toast } from 'redux/actions/TodoAction';
import axios from 'axios';
import { TOAST_TYPE_ERROR } from 'utils/constants';

function Home() {
  const isSearching = useSelector((state) => state.searchStates.searching);
  const dispatch = useDispatch();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchTasks() {
      axios
        .get('/tasks')
        .then((response) => {
          if (response.status == 200) {
            dispatch(loadTasksFromDB(response.data.items));
            setIsLoading(false);
          }
        })
        .catch((error) => {
          dispatch(toast({ type: 'danger', message: 'something wrong. Try again later' }));
          console.log(error);
        });
    }

    fetchTasks();
  }, []);

  return (
    <div className="home">
      {isLoading ? (
        <div>loading....</div>
      ) : (
        <>
          {isSearching && <Loader />}
          <ToastContainer />
          <Heading />
          <BottomNav />
          <TaskContainer />
        </>
      )}
    </div>
  );
}

export default Home;
