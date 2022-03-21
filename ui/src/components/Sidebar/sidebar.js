import './sidebar.scss';

import {
  CDBSidebar,
  CDBSidebarContent,
  CDBSidebarFooter,
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
                        <a href='https://esa.act.gov.au/cbr-be-emergency-ready/bushfires/bushfire-ready'>
                            <CDBSidebarMenuItem>Bushfire ready</CDBSidebarMenuItem>
                        </a>
                        <a href='https://esa.act.gov.au/be-emergency-ready/extreme-heat'>
                            <CDBSidebarMenuItem>Extreme heat</CDBSidebarMenuItem>
                        </a>
                        <a href='https://esa.act.gov.au/be-emergency-ready/fire-safety'>
                            <CDBSidebarMenuItem>Total fire bans</CDBSidebarMenuItem>
                        </a>
                        <a href='https://esa.act.gov.au/cbr-be-emergency-ready/emergency-arrangements'>
                            <CDBSidebarMenuItem>Emergency</CDBSidebarMenuItem>
                        </a>

                        <Link exact to='/quiz'>
                            <CDBSidebarMenuItem>Take a quiz</CDBSidebarMenuItem>
                        </Link>
                    </CDBSidebarMenu>
                </CDBSidebarContent>
                <CDBSidebarFooter style={{ textAlign: 'center' }}>
                    <div
                        className="sidebar-btn-wrapper"
                        style={{padding: '20px 5px'}}
                    >
                        Footer
                    </div>
                </CDBSidebarFooter>
            </CDBSidebar>
        </div>
    );
}

export default Sidebar;