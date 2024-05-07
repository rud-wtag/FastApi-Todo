import propTypes from 'prop-types';
import { useEffect, useState } from 'react';
import { TOAST_TYPE_SUCCESS } from 'utils/constants';
import { ReactComponent as DoneIcon } from 'assets/ok.svg';

function Toast({ message = '', type = TOAST_TYPE_SUCCESS }) {
  const [show, setShow] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setShow(false);
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
