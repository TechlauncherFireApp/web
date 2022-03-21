import './sidebar.scss';

import {
  CDBSidebar,
  CDBSidebarFooter,
  CDBSidebarHeader
} from 'cdbreact';
// import {
//   CDBSidebar,
//   CDBSidebarContent,
//   CDBSidebarFooter,
//   CDBSidebarHeader,
//   CDBSidebarMenu,
//   CDBSidebarMenuItem,
//   CDBSidebarSubMenu,
// } from 'cdbreact';
import React from "react";

const Sidebar = () => {
    return (
        <div style={{ height: '100vh', overflow: 'scroll initial', width: '10px' }} className='custom-sidebar'>
            <CDBSidebar>
                <CDBSidebarHeader prefix={<i className="fa fa-bars" />}>Header</CDBSidebarHeader>
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