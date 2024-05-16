import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Button } from '@mui/material';
import Heading from './Heading';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';

export default function FullProfile() {
  const profile = useSelector((state) => state.appStates.profile);
  return (
    <>
      <Heading />
      <div className="profile-page">
        <Card
          sx={{
            display: 'flex',
            flexDirection: 'column',
            textAlign: 'center',
            alignItems: 'center',
            gap: '4rem',
            padding: '2rem',
            marginTop: '-5rem'
          }}
        >
          <Box sx={{ display: 'flex', flexDirection: 'column' }}>
            <CardMedia
              component="img"
              sx={{
                width: '15rem',
                height: '15rem',
                borderRadius: '50%',
                marginInline: 'auto'
              }}
              image="https://picsum.photos/200/300"
              alt="Live from space album cover"
            />
            <CardContent sx={{ flex: '1 0 auto' }}>
              <Typography component="div" variant="h5">
                {profile?.username}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" component="div">
                {profile?.full_name}
              </Typography>
            </CardContent>
            <Box sx={{ display: 'flex', gap: '1rem' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', pl: 1, pb: 1 }}>
                <Link to="/change-password">
                  <Button variant="outlined">Change password</Button>
                </Link>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', pl: 1, pb: 1 }}>
                <Link to="/update-profile">
                  <Button variant="outlined">Update Profile</Button>
                </Link>
              </Box>
            </Box>
          </Box>
        </Card>
      </div>
    </>
  );
}
