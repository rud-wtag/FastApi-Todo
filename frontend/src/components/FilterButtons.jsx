import Button from 'components/ui/Button';
import { useDispatch } from 'react-redux';
import { setDueDate, setFilter, setPriority } from 'redux/actions/FilterAction';
import { LABEL_ALL, LABEL_COMPLETE, LABEL_INCOMPLETE } from 'utils/constants';

import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import dayjs from 'dayjs';
import SecondaryButton from '@mui/material/Button';


function FilterButtons() {
  const dispatch = useDispatch();

  const priorityChange = (event) => {
    dispatch(setPriority(event.target.value))
  };

  const dueDateChange = (dueDate) => {
    dispatch(setDueDate(dueDate))
  };

  const actionButtons = [
    { label: LABEL_ALL },
    { label: LABEL_COMPLETE },
    { label: LABEL_INCOMPLETE }
  ];

  function onFilter(event, label) {
    event.preventDefault();
    dispatch(setFilter(label));
  }

  function resetFilter(even)
  {
    event.preventDefault();
    dispatch(setPriority(null));
    dispatch(setDueDate(null));
    dispatch(setFilter(null));
  }

  return (
    <Box sx={{display: "flex", gap: "1rem"}}>
      <SecondaryButton variant="contained" color="secondary" onClick={(e) => resetFilter(e)}>Reset</SecondaryButton>
      <Box sx={{ minWidth: 120, height: "56px" }}>
        <FormControl fullWidth>
          <InputLabel id="demo-simple-select-label">Priority</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={''}
            label="Priority"
            onChange={priorityChange}
          >
            <MenuItem value={'HIGH'}>High</MenuItem>
            <MenuItem value={'MEDIUM'}>Medium</MenuItem>
            <MenuItem value={'LOW'}>Low</MenuItem>
          </Select>
        </FormControl>
      </Box>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DesktopDatePicker
          onChange={(newValue) => dueDateChange(dayjs(newValue).format('YYYY-MM-DD'))}
          defaultValue={dayjs()}
        />
      </LocalizationProvider>
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
    </Box>
  );
}

export default FilterButtons;
