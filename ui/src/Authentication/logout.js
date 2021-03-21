import React from 'react';
import { useHistory } from 'react-router';

function Logout() {
  const history = useHistory();
  localStorage.removeItem('access_token');
  localStorage.removeItem('role');
  history.push('/login');

  return <div>Loading...</div>;
}

export default Logout;
