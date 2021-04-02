import React from 'react';
import './Home.scss';
import { useHistory } from 'react-router';

function Home() {
  const history = useHistory();
  const access_token = localStorage.getItem('access_token');
  const role = localStorage.getItem('role');
  const id = localStorage.getItem('id');

  if (access_token !== null) {
    if (role === 'VOLUNTEER') {
      history.push('/volunteer/'+id);
    } else {
      history.push('/captain');
    }
  } else {
    history.push('/login');
  }

  return <div>Loading...</div>;
}

export default Home;
