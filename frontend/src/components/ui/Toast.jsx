import propTypes from 'prop-types';
import { useEffect, useState } from 'react';
import { TOAST_TYPE_SUCCESS } from 'utils/constants';
import { ReactComponent as DoneIcon } from 'assets/ok.svg';
import { useDispatch } from 'react-redux';
import { toast } from 'redux/actions/TodoAction';

function Toast({ message = '', type = TOAST_TYPE_SUCCESS }) {
  const [show, setShow] = useState(true);
  const dispatch = useDispatch();

  useEffect(() => {
    setTimeout(() => {
      setShow(false);
      dispatch(toast({ type: null, message: null }));
    }, 3000);
  }, []);

  return (
    <>
      {show && (
        <div className={`toast toast--${type}`}>
          {type === TOAST_TYPE_SUCCESS && <DoneIcon />} <span>{message}</span>
        </div>
      )}
    </>
  );
}

Toast.propTypes = {
  message: propTypes.string,
  type: propTypes.string
};

export default Toast;
