import { useSelector } from 'react-redux';
import React, { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import Toast from 'components/ui/Toast';

function ToastContainer() {
  const toast = useSelector((state) => state.todoStates.toast);
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    if (toast.message) {
      const newToast = { id: uuidv4(), type: toast.type, message: toast.message };
      setToasts((prevToasts) => [newToast, ...prevToasts]);
    }
  }, [toast]);

  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <Toast key={toast.id} type={toast.type} message={toast.message} />
      ))}
    </div>
  );
}

export default ToastContainer;
