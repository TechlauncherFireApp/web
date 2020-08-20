import React from "react";

import NavBar from "./components/navbar";
import Home from "./Home/Home";
import AssetRequestContainer from "./NewAssetRequest/assetRequestContainer";
import Volunteers from "./Volunteers/Volunteers";

import { BrowserRouter, Route, Switch } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <main-body>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/NewAssetRequest" component={AssetRequestContainer} />
          <Route path="/volunteers" component={Volunteers} />
        </Switch>
      </main-body>
    </BrowserRouter>
  );
}
export default App;