import React, { Component } from "react";
import "./navbar.scss";
import { Navbar, Nav } from "react-bootstrap";

class NavBar extends Component {
  render() {
    return (
      <Navbar>
        <Navbar.Collapse>
          <Navbar.Brand href="/">FireApp</Navbar.Brand>
          <Nav className="ml-auto navbar-right">
            {/* <Nav.Link href="/NewAssetRequest">New Asset Request</Nav.Link> */}
            {/* <Nav.Link href="/Volunteers">Volunteers</Nav.Link> */}
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}
export default NavBar;
