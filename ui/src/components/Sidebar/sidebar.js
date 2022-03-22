import './sidebar.scss';

import {
  CDBSidebar,
  CDBSidebarContent,
  CDBSidebarHeader,
  CDBSidebarMenu,
  CDBSidebarMenuItem
} from 'cdbreact';
import React from "react";
import { Link } from "react-router-dom";

const Sidebar = () => {
    return (
        <div style={{ height: '100vh', overflow: 'scroll initial', width: '10px' }} className='custom-sidebar'>
            <CDBSidebar>
                <CDBSidebarHeader prefix={<i className="fa fa-bars" />}>Menu</CDBSidebarHeader>
                <CDBSidebarContent>
                    <CDBSidebarMenu>
                        <div>
                            <CDBSidebarMenuItem>
                                <h1 className='submenu-heading'>Resources</h1>
                            </CDBSidebarMenuItem>
                        </div>
                        <ul className='sidebar-list'>
                            <li>
                                <a href='https://esa.act.gov.au/cbr-be-emergency-ready/bushfires/bushfire-ready' target='none' rel='noopener noreferrer'>
                                    <CDBSidebarMenuItem>Bushfire ready</CDBSidebarMenuItem>
                                </a>
                            </li>
                            <li>
                                <a href='https://esa.act.gov.au/be-emergency-ready/extreme-heat' target='none' rel='noopener noreferrer'>
                                    <CDBSidebarMenuItem>Extreme heat</CDBSidebarMenuItem>
                                </a>
                            </li>
                            <li>
                                <a href='https://esa.act.gov.au/be-emergency-ready/fire-safety' target='none' rel='noopener noreferrer'>
                                    <CDBSidebarMenuItem>Total fire bans</CDBSidebarMenuItem>
                                </a>
                            </li>
                            <li>
                                <a href='https://esa.act.gov.au/cbr-be-emergency-ready/emergency-arrangements' target='none' rel='noopener noreferrer'>
                                    <CDBSidebarMenuItem>Emergency</CDBSidebarMenuItem>
                                </a>
                            </li>
                        </ul>

                        <CDBSidebarMenuItem><hr className='sidebar-hr'/></CDBSidebarMenuItem>

                        <Link exact to='/quiz'>
                            <CDBSidebarMenuItem>Take a quiz</CDBSidebarMenuItem>
                        </Link>

                        <CDBSidebarMenuItem><hr className='sidebar-hr'/></CDBSidebarMenuItem>

                        <Link exact to='/'>
                            <CDBSidebarMenuItem>Home</CDBSidebarMenuItem>
                        </Link>
                    </CDBSidebarMenu>
                </CDBSidebarContent>
            </CDBSidebar>
        </div>
    );
}

export default Sidebar;