import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import NavBar from './components/Navbar/navbar';
import AssetRequestVehicle from './routes/AssetRequestVehicle/AssetRequestVehicle';
import AssetRequestVolunteers from './routes/AssetRequestVolunteers/assetRequestVolunteers';
import AssetTypeRoles from './routes/AssetTypeRoles';
import Login from './routes/Authentication/login';
import Logout from './routes/Authentication/logout';
import Register from './routes/Authentication/register';
import BrigadeCaptainHome from './routes/BrigadeCaptainHome/brigadeCaptainHome';
import Home from './routes/Home/Home';
import AssetTypes from './routes/Reference/assetTypes';
import Qualifications from './routes/Reference/qualifications';
import Roles from './routes/Reference/roles';
import VolunteerRoles from './routes/VolunteerRoles';
import Availability from './routes/Volunteers/Availability/Availability';
import Volunteer from './routes/Volunteers/volunteer';
import VolunteersContainer from './routes/Volunteers/volunteersContainer';

export default function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <div className={'main-body'}>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/login" component={Login} />
          <Route exact path="/logout" component={Logout} />
          <Route exact path="/register" component={Register} />
          <Route exact path="/reference/roles" component={Roles} />
          <Route
            exact
            path="/reference/qualifications"
            component={Qualifications}
          />
          <Route exact path="/reference/asset_types" component={AssetTypes} />
          <Route exact path="/captain" component={BrigadeCaptainHome} />
          <Route
            exact
            path="/assetRequest/vehicles/:id"
            component={AssetRequestVehicle}
          />
          <Route
            exact
            path="/assetRequest/volunteers/:id"
            component={AssetRequestVolunteers}
          />
          <Route exact path="/volunteer" component={VolunteersContainer} />
          <Route exact path="/volunteer-roles" component={VolunteerRoles} />
          <Route exact path="/asset-type-roles" component={AssetTypeRoles} />
          <Route exact path="/volunteer/:id" component={Volunteer} />
          <Route
            exact
            path="/volunteer/:id/availability"
            component={Availability}
          />
        </Switch>
      </div>
    </BrowserRouter>
  );
}
