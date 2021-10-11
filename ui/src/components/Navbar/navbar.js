import './navbar.scss';

import axios from "axios";
import React, { useEffect, useState } from 'react';
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
import { useLocation } from 'react-router-dom';

import {backendPath} from "../../config";

function NavBar() {
  let location = useLocation();
  const [authenticated, setAuthenticated] = useState(
    localStorage.getItem('access_token') !== null
  );
  const [role] = useState(localStorage.getItem('role'));
  const [id] = useState(localStorage.getItem('id'));

  const [activeConfig, setActiveConfig] = useState(undefined);
  let [title] = useState(localStorage.getItem('title'));
  let [colour] = useState(localStorage.getItem('nav_colour'));
  let [font] = useState(localStorage.getItem('font'))

  // Apply the latest configuration, or fetch if undefined
  useEffect(() => {
      console.log(activeConfig)
    if (activeConfig === undefined || title === undefined) {
      title = 'FireApp';
      colour = 'CC0000';
      font = 'Segoe UI';
      getConfig()
      return
    }
    localStorage.setItem('title', activeConfig['title']);
    localStorage.setItem('font', activeConfig['font']);
    localStorage.setItem('nav_colour', activeConfig['nav_colour']);

  }, [activeConfig, location])


  // Get the currently active configuration
   function getConfig(){
    setAuthenticated(localStorage.getItem('access_token') !== null);
    axios
        .get(backendPath + 'tenancy_config', {
          headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')},
          params: {getAll: 'false'}
        })
        .then((resp) => {
          setActiveConfig(resp.data.results[0])
        });
  }

  return (
    <Navbar style={{backgroundColor: colour}}>
      <Navbar.Collapse>
        <Navbar.Brand href="/" style={{fontfamily: font}}>{title}</Navbar.Brand>
        {authenticated && (role === 'ROOT_ADMIN' || role === 'ADMIN') && (
          <>
            <Nav.Link href="/captain">Request Administration</Nav.Link>
            <Nav.Link href="/asset-type-roles">Asset Planning</Nav.Link>
            <NavDropdown
              title="Volunteer Data"
              id="basic-nav-dropdown"
              className={'white'}>
              <NavDropdown.Item href="/volunteer-roles">Volunteer Roles</NavDropdown.Item>
              <NavDropdown.Item href="/user-privileges">User Privileges</NavDropdown.Item>
              <NavDropdown.Item href={"/volunteer/" + id}>My Volunteer Page</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown
              title="Reference Data"
              id="basic-nav-dropdown"
              className={'white'}>
              <NavDropdown.Item href="/reference/roles">Roles</NavDropdown.Item>
              <NavDropdown.Item href="/reference/qualifications">Qualifications</NavDropdown.Item>
              <NavDropdown.Item href="/reference/asset_types">Asset Types</NavDropdown.Item>
              <NavDropdown.Item href="/tenancy-configs">Website Customisation</NavDropdown.Item>
            </NavDropdown>
          </>
        )}
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
