import React, { Component } from 'react';
import './navbar.scss';
import { Navbar, Nav } from 'react-bootstrap';

class NavBar extends Component {
  render() {
    return (
      <Navbar>
        <Navbar.Collapse>
          <Navbar.Brand href="/">FireApp</Navbar.Brand>
          <Nav className="ml-auto navbar-right">
            {localStorage.getItem('access_token') !== null ? (
              <Nav.Link href="/logout">Logout</Nav.Link>
            ) : (
              <Nav.Link href="/login">Login</Nav.Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}
export default NavBar;
