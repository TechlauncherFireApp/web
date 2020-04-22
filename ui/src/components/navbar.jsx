import React, { Component } from "react";
import { NavLink } from "react-router-dom";
import { Navbar, Nav } from "react-bootstrap";

class NavBar extends Component {
  // state = {  }
  render() {
    return (
      <Navbar bg="dark" variant="dark">
        <Navbar.Brand href="/">Fire App</Navbar.Brand>
        <Nav className="mr-auto">
          <Nav.Link href="/assetRequest">New Asset Request</Nav.Link>
          <Nav.Link href="/recommendation">Recommendation (filler)</Nav.Link>
          <Nav.Link href="/volunteers">Volunteers</Nav.Link>
        </Nav>
      </Navbar>
      /* <Navbar bg="dark">
        <Navbar.Brand>
          <NavLink className="text-white" to="/">
            Fire App
          </NavLink>
        </Navbar.Brand>
        <Nav className="mr-auto">
          <NavLink className="p-2 bg-dark text-white" to="/newAssetRequest">
            New Asset Request
          </NavLink>
          <NavLink className="p-2 bg-dark text-white" to="/volunteers">
            Volunteers
          </NavLink>
        </Nav>
      </Navbar> */
    );
  }
}

export default NavBar;
