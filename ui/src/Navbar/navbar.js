import React, { useEffect, useState } from 'react';
import './navbar.scss';
import { Navbar, Nav } from 'react-bootstrap';
import { useLocation } from 'react-router-dom';

function NavBar() {
  let location = useLocation();
  const [authenticated, setAuthenticated] = useState(
    localStorage.getItem('access_token') !== null
  );

  useEffect(() => {
    setAuthenticated(localStorage.getItem('access_token') !== null);
  }, [location]);

  return (
    <Navbar>
      <Navbar.Collapse>
        <Navbar.Brand href="/">FireApp</Navbar.Brand>
        <Nav className="ml-auto navbar-right">
          {authenticated ? (
            <Nav.Link href="/logout">Logout</Nav.Link>
          ) : (
            <Nav.Link href="/login">Login</Nav.Link>
          )}
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}
export default NavBar;
