import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import BottomNav from 'components/BottomNav';
import Heading from 'components/Heading';
import TaskContainer from 'components/TaskContainer';
import Loader from 'components/ui/Loader';
import Toast from 'components/ui/Toast';
import { loadTasksFromDB, toast } from 'redux/actions/TodoAction';
import supabase from 'supabase';
import ToastContainer from 'components/ToastContainer';

function Home() {
  const isSearching = useSelector((state) => state.searchStates.searching);
  const dispatch = useDispatch();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchTasks() {
      let { data, error } = await supabase
        .from('todos')
        .select()
        .order('createdAt', { ascending: false });

      if (!error) {
        dispatch(loadTasksFromDB(data));
        setIsLoading(false);
      } else {
        dispatch(toast({ type: 'danger', message: 'something wrong. Try again later' }));
      }
    }

    fetchTasks();
  }, []);

  return (
    <div className="home">
      {isLoading ? (
        <div>loading....</div>
      ) : (
        <>
          <ToastContainer />
          <Heading />
          {isSearching && <Loader />}
          <Toast />
          <BottomNav />
          <TaskContainer />
        </>
      )}
    </div>
  );
}

export default Home;
