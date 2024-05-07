import { useDispatch } from 'react-redux';
import Button from 'components/ui/Button';
import { setFilter } from 'redux/actions/FilterAction';
import { LABEL_ALL, LABEL_COMPLETE, LABEL_INCOMPLETE } from 'utils/constants';

function FilterButtons() {
  const dispatch = useDispatch();

  const actionButtons = [
    { label: LABEL_ALL },
    { label: LABEL_COMPLETE },
    { label: LABEL_INCOMPLETE }
  ];

  function onFilter(event, label) {
    event.preventDefault();
    dispatch(setFilter(label));
  }

  return (
    <>
      {actionButtons.map((button) => {
        return (
          <Button
            onClick={(event) => onFilter(event, button.label)}
            key={button.label}
            className="bottom_nav__right__btn"
          >
            {button.label}
          </Button>
        );
      })}
    </>
  );
}

export default FilterButtons;
