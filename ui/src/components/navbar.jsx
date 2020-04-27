import React, { Component } from "react";
import { Navbar, Nav } from "react-bootstrap";

class NavBar extends Component {
  // state = {  }
  render() {
    return (
      <Navbar bg="dark" variant="dark">
        <Navbar.Brand href="/">Fire App</Navbar.Brand>
        <Nav className="mr-auto">
          <Nav.Link href="/nar">New Asset Request</Nav.Link>
          <Nav.Link href="/volunteers">Volunteers</Nav.Link>
        </Nav>
      </Navbar>
    );
  }
}

export default NavBar;
