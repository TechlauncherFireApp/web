import './navbar.scss';

import axios from "axios";
import React, {useEffect, useState} from 'react';
import {Nav, Navbar, NavDropdown} from 'react-bootstrap';
import {useLocation} from 'react-router-dom';

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
    let [font] = useState(localStorage.getItem('font'));

    // Apply the latest configuration, or fetch if undefined
    useEffect(() => {
        if (activeConfig === undefined || title === undefined) {
            title = 'FireApp';
            colour = '#CC0000';
            font = 'Segoe UI';
            getConfig()
            return
        }
        localStorage.setItem('title', activeConfig['title']);
        localStorage.setItem('font', activeConfig['font']);
        localStorage.setItem('nav_colour', activeConfig['nav_colour']);
    }, [activeConfig, location])


    // Get the currently active configuration
    function getConfig() {
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
                <Navbar.Brand href="/" style={{fontFamily: font}}>{title}</Navbar.Brand>
                {authenticated && (role === 'ROOT_ADMIN' || role === 'ADMIN') && (
                    <>
                        <Nav.Link href="/captain" style={{fontFamily: font}}>Request Administration</Nav.Link>
                        <Nav.Link href="/asset-type-roles" style={{fontFamily: font}}>Asset Planning</Nav.Link>
                        <NavDropdown
                            title={<span style={{fontFamily: font}}>Volunteer Data</span>}
                            id="basic-nav-dropdown"
                            className={'white'}>
                            <NavDropdown.Item href="/volunteer-roles" style={{fontFamily: font}}>
                                Volunteer Roles
                            </NavDropdown.Item>
                            <NavDropdown.Item href="/user-privileges" style={{fontFamily: font}}>
                                User Privileges
                            </NavDropdown.Item>
                            <NavDropdown.Item href={"/volunteer/" + id} style={{fontFamily: font}}>
                                My Volunteer Page
                            </NavDropdown.Item>
                        </NavDropdown>
                        <NavDropdown
                            title={<span style={{fontFamily: font}}>Reference Data</span>}
                            id="basic-nav-dropdown"
                            className={'white'}>
                            <NavDropdown.Item href="/reference/roles" style={{fontFamily: font}}>
                                Roles
                            </NavDropdown.Item>
                            <NavDropdown.Item href="/reference/qualifications" style={{fontFamily: font}}>
                                Qualifications
                            </NavDropdown.Item>
                            <NavDropdown.Item href="/reference/asset_types" style={{fontFamily: font}}>
                                Asset Types
                            </NavDropdown.Item>
                            <NavDropdown.Item href="/tenancy-configs" style={{fontFamily: font}}>
                                Branding
                            </NavDropdown.Item>
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
