import React from "react";

import NavBar from "./components/navbar";
import Home from "./Home/Home";
import AssetRequestVehicle from "./AssetRequestVehicle/AssetRequestVehicle";
import AssetRequestVolunteers from "./AssetRequestVolunteers/assetRequestVolunteers";
import AssetRequestContainer from "./NewAssetRequest/assetRequestContainer";
import Volunteers from "./Volunteers/Volunteers";

import { BrowserRouter, Route, Switch } from "react-router-dom";

export default function App() {

  return (
    <BrowserRouter>
      <NavBar />
      <main-body>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/assetRequest/vehicle/:id" component={AssetRequestVehicle} />
          <Route path="/assetRequest/test" component={AssetRequestVolunteers} />
          <Route path="/NewAssetRequest" component={AssetRequestContainer} />
          <Route path="/volunteers" component={Volunteers} />
        </Switch>
      </main-body>
    </BrowserRouter>
  );
}