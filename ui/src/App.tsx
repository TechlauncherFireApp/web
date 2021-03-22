import React from 'react';

import NavBar from './Navbar/navbar';
import BrigadeCaptainHome from './BrigadeCaptainHome/brigadeCaptainHome';
import AssetRequestVehicle from './AssetRequestVehicle/AssetRequestVehicle';
import AssetRequestVolunteers from './AssetRequestVolunteers/assetRequestVolunteers';
import VolunteersContainer from './Volunteers/volunteersContainer';
import Volunteer from './Volunteers/volunteer';
import Availability from './Volunteers/Availability/Availability';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import ExistingRequestSelector from './ViewExistingRequests/existingRequestSelector';
import Login from './Authentication/login';
import Register from './Authentication/register';
import Home from './Home/Home';
import Logout from './Authentication/logout';

export default function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <main-body>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/login" component={Login} />
          <Route exact path="/logout" component={Logout} />
          <Route exact path="/register" component={Register} />
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
          <Route
            exact
            path="/viewExistingRequest/"
            component={ExistingRequestSelector}
          />
          <Route exact path="/volunteer" component={VolunteersContainer} />
          <Route exact path="/volunteer/:id" component={Volunteer} />
          <Route
            exact
            path="/volunteer/:id/availability"
            component={Availability}
          />
        </Switch>
      </main-body>
    </BrowserRouter>
  );
}
