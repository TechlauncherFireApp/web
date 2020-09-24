import React from "react";

import NavBar from "./Navbar/navbar";
import BrigadeCaptainHome from "./BrigadeCaptainHome/brigadeCaptainHome";
import AssetRequestVehicle from "./AssetRequestVehicle/AssetRequestVehicle";
import AssetRequestVolunteers from "./AssetRequestVolunteers/assetRequestVolunteers";
import VolunteersContainer from "./Volunteers/volunteersContainer";
import Volunteer from "./Volunteers/volunteer";
import Availability from "./Volunteers/Availability/Availability";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import ExistingRequestContainer from "./ViewExistingRequests/existingRequestContainer";
import Home from "./Home/Home";

export default function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <main-body>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/captain" component={BrigadeCaptainHome} />
          <Route exact path="/assetRequest/vehicles/:id" component={AssetRequestVehicle} />
          <Route exact path="/assetRequest/volunteers/:id" component={AssetRequestVolunteers} />
          <Route exact path="/viewExistingRequest/" component={ExistingRequestContainer} />
          <Route exact path="/volunteer" component={VolunteersContainer} />
          <Route exact path="/volunteer/:id" component={Volunteer} />
          <Route exact path="/volunteer/:id/availability" component={Availability} />
        </Switch>
      </main-body>
    </BrowserRouter>
  );
}
