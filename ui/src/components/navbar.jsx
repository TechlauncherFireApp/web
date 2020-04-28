import React, { Component } from "react";
import "./navbar.scss";
// import { NavLink } from "react-router-dom";
import { Navbar, Nav } from "react-bootstrap";

class NavBar extends Component {
  // state = {  }
  render() {
    return (
      /* bg="dark" variant="dark" */
      <Navbar>
        <Navbar.Brand href="/">FireApp</Navbar.Brand>
        <Nav className="ml-auto navbar-right">
          <Nav.Link href="/NewAssetRequest">New Asset Request</Nav.Link>
          <Nav.Link href="/Volunteers">Volunteers</Nav.Link>
        </Nav>
      </Navbar>
    );
  }
}
export default NavBar;
