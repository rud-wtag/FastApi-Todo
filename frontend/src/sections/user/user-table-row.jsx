import PropTypes from 'prop-types';
import { useState } from 'react';

import Avatar from '@mui/material/Avatar';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import MenuItem from '@mui/material/MenuItem';
import Popover from '@mui/material/Popover';
import Stack from '@mui/material/Stack';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';

import Iconify from 'components/iconify';
import Label from 'components/label';
import axios from 'axios'
import { toast } from 'react-toastify';
// ----------------------------------------------------------------------

export default function UserTableRow({
  userId,
  selected,
  full_name,
  avatarUrl,
  email,
  role,
  isVerified,
  status,
  handleClick,
  setAction
}) {
  const [open, setOpen] = useState(null);

  const handleOpenMenu = (event) => {
    setOpen(event.currentTarget);
  };

  const handleCloseMenu = () => {
    setOpen(null);
  };

  const onActivate = () => {
    axios.put(`/users/${userId}/activate`)
    .then(res => {
      if (res.status == 200){
        toast.success('🦄 User activated');
        setAction(`user ${userId} activated`)
        handleCloseMenu()
      }
    })
    .catch(err=>{
      toast.error('🦄 User can not activated');
    })
  }
  const onDeactivate = () => {
    axios.put(`/users/${userId}/deactivate`)
    .then(res => {
      console.log(res)
      if (res.status == 200){
        toast.success('User deactivated');
        setAction(`user ${userId} deactivated`)
        handleCloseMenu()
      }
    })
    .catch(err=>{
      toast.error('User can not be deactivated');
    })
  }
  const onDelete = () => {
    axios.delete(`/users/${userId}`)
    .then(res => {
      console.log(res)
      if (res.status == 200){
        toast.success('User deleted');
        setAction(`user ${userId} deleted`)
        handleCloseMenu()
      }
    })
    .catch(err=>{
      toast.error('User can not be deleted');
    })
  }

  return (
    <>
      <TableRow hover tabIndex={-1} role="checkbox" selected={selected}>
        <TableCell padding="checkbox">
          <Checkbox disableRipple checked={selected} onChange={handleClick} />
        </TableCell>

        <TableCell component="th" scope="row" padding="none">
          <Stack direction="row" alignItems="center" spacing={2}>
            <Avatar alt={full_name} src={avatarUrl} />
            <Typography variant="subtitle2" noWrap>
              {full_name}
            </Typography>
          </Stack>
        </TableCell>

        <TableCell>{email}</TableCell>

        <TableCell>{role == 1? 'Admin': 'User'}</TableCell>

        <TableCell align="center">{isVerified ? 'Yes' : 'No'}</TableCell>

        <TableCell>
          <Label color={(status === false && 'error') || 'success'}>
            {status == true ? 'active' : 'inactive'}
          </Label>
        </TableCell>

        <TableCell align="right">
          <IconButton onClick={handleOpenMenu}>
            <Iconify icon="eva:more-vertical-fill" />
          </IconButton>
        </TableCell>
      </TableRow>

      <Popover
        open={!!open}
        anchorEl={open}
        onClose={handleCloseMenu}
        anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: { width: 140 }
        }}
      >
        {
          !status && 
          (<MenuItem onClick={onActivate}>
            <Iconify icon="eva:edit-fill" sx={{ mr: 2 }} />
            Activate
          </MenuItem>)
        }
        {
          status &&
          <MenuItem onClick={onDeactivate}>
            <Iconify icon="eva:edit-fill" sx={{ mr: 2 }} />
            Deactivate
          </MenuItem>
        }

        <MenuItem onClick={onDelete} sx={{ color: 'error.main' }}>
          <Iconify icon="eva:trash-2-outline" sx={{ mr: 2 }} />
          Delete
        </MenuItem>
      </Popover>
    </>
  );
}

UserTableRow.propTypes = {
  avatarUrl: PropTypes.any,
  email: PropTypes.any,
  handleClick: PropTypes.func,
  isVerified: PropTypes.any,
  full_name: PropTypes.any,
  role: PropTypes.any,
  selected: PropTypes.any,
  status: PropTypes.string
};
