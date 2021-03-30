import React from 'react';
import './Home.scss';
import { useHistory } from 'react-router';

function Home() {
  const history = useHistory();
  const access_token = localStorage.getItem('access_token');
  const role = localStorage.getItem('role');

  if (access_token !== null) {
    if (role === 'VOLUNTEER') {
      history.push('/volunteer');
    } else {
      history.push('/captain');
    }
  } else {
    history.push('/login');
  }

  return <div>Loading...</div>;
}

export default Home;
