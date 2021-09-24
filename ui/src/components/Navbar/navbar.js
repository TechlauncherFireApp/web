import './navbar.scss';

// import React from "react";
import React, { useEffect, useState } from 'react';
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
// import Container from 'react-bootstrap/Container';
// import { useLocation } from 'react-router-dom';

function NavBar() {
  // let location = useLocation();
  const [authenticated, setAuthenticated] = useState(
    localStorage.getItem('access_token') !== null
  );
  // const [role] = useState(localStorage.getItem('role'));
  // const [id] = useState(localStorage.getItem('id'))

  useEffect(() => {
    setAuthenticated(localStorage.getItem('access_token') !== null);
  }, [location]);

  return (
      <Navbar expand="xl">
          <Navbar.Brand href="/">FireApp</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav"/>
          <Navbar.Collapse id="basic-navbar-nav">
                {/*<Nav className="me-auto">*/}
                    <Nav.Link href="#home">Home</Nav.Link>
                    <Nav.Link href="#link">Link</Nav.Link>
                    <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                        <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                        <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
                        <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                        <NavDropdown.Divider />
                        <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
                    </NavDropdown>
              <Nav className="ml-auto navbar-right">
                  {authenticated ? (
                <Nav.Link href="/logout">Logout</Nav.Link>
              ) : (
                <Nav.Link href="/login">Login</Nav.Link>
              )}
              </Nav>
                {/*</Nav>*/}
          </Navbar.Collapse>
      </Navbar>

      //
      //     <Navbar.Collapse>
      //     <Navbar.Brand href="/">FireApp</Navbar.Brand>
      //     <Navbar.Toggle aria-controls="basic-navbar-nav"/>
      //
      //       {authenticated && (role === 'ROOT_ADMIN' || role === 'ADMIN') && (
      //         <>
      //           <Nav.Link href="/captain">Request Administration</Nav.Link>
      //           <Nav.Link href="/asset-type-roles">Asset Planning</Nav.Link>
      //           <NavDropdown
      //             title="Volunteer Data"
      //             id="basic-nav-dropdown"
      //             className={'white'}>
      //             <NavDropdown.Item href="/volunteer-roles">Volunteer Roles</NavDropdown.Item>
      //             <NavDropdown.Item href="/user-privileges">User Privileges</NavDropdown.Item>
      //             <NavDropdown.Item href={"/volunteer/" + id}>My Volunteer Page</NavDropdown.Item>
      //           </NavDropdown>
      //           <NavDropdown
      //             title="Reference Data"
      //             id="basic-nav-dropdown"
      //             className={'white'}>
      //             <NavDropdown.Item href="/reference/roles">Roles</NavDropdown.Item>
      //             <NavDropdown.Item href="/reference/qualifications">
      //               Qualifications
      //             </NavDropdown.Item>
      //             <NavDropdown.Item href="/reference/asset_types">
      //               Asset Types
      //             </NavDropdown.Item>
      //           </NavDropdown>
      //         </>
      //       )}
      //       <Nav className="ml-auto navbar-right">
      //         {authenticated ? (
      //           <Nav.Link href="/logout">Logout</Nav.Link>
      //         ) : (
      //           <Nav.Link href="/login">Login</Nav.Link>
      //         )}
      //       </Nav>
      //     </Navbar.Collapse>
      // </Navbar>
  );
}
export default NavBar;
