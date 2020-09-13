import React from "react";

import NavBar from "./components/navbar";
import Home from "./Home/Home";
// import AssetRequestVehicle from "./AssetRequestVehicle/AssetRequestVehicle";
// import AssetRequestVolunteers from "./AssetRequestVolunteers/assetRequestVolunteers";
import AssetRequestContainer from "./assetRequestContainer";
import VolunteersContainer from "./Volunteers/volunteersContainer";
import Volunteer from "./Volunteers/volunteer";
import Availability from "./Volunteers/Availability/Availability";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import ExistingRequestContainer from "./viewExistingRequests/existingRequestContainer";

export default function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <main-body>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/assetRequest/:id" component={AssetRequestContainer} />
          <Route path="/viewExistingRequest/" component={ExistingRequestContainer} />
          <Route exact path="/volunteer" component={VolunteersContainer} />
          <Route exact path="/volunteer/:id" component={Volunteer} />
          <Route exact path="/volunteer/:id/availability" component={Availability} />
        </Switch>
      </main-body>
    </BrowserRouter>
  );
}
