import React from "react";

import NavBar from "./components/navbar";
import Home from "./Home/Home";
// import AssetRequestVehicle from "./AssetRequestVehicle/AssetRequestVehicle";
// import AssetRequestVolunteers from "./AssetRequestVolunteers/assetRequestVolunteers";
import AssetRequestContainer from "./assetRequestContainer";
import Volunteers from "./Volunteers/Volunteers";
import Availability from "./Volunteers/Availability/Availability";

import { BrowserRouter, Route, Switch } from "react-router-dom";

export default function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <main-body>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/assetRequest/:id" component={AssetRequestContainer} />
          {/* <Route path="/assetRequest/vehicle/:id" component={AssetRequestVehicle} /> */}
          {/* <Route path="/assetRequest/volunteers/:id/:isNew" component={AssetRequestVolunteers} /> */}
          {/* <Route path="/NewAssetRequest" component={AssetRequestContainer} /> */}
          <Route exact path="/volunteers" component={Volunteers} />
          <Route exact path="/volunteers/availability" component={Availability} />



          {/* localhost:5000/shift/request */}
          {/* { "shifts" : [{ "shiftID":"3de8735f76d14d0", "volunteers":[{ "ID":"3LOToozxu5UgWFW", "positionID":0, "role": ["driver", "crewLeader"] }, { "ID":"35uwKUUugHaY2ZN", "positionID":1, "role": ["advanced"] }] }] } */}
        </Switch>
      </main-body>
    </BrowserRouter>
  );
}
