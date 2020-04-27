import React from "react";
import "./App.scss";

import NavBar from "./components/navbar";
import VolunteersPage from "./components/volunteersPage";
import HomePage from "./components/homePage";
import AssetRequestContainer from "./NewAssetRequest/assetRequestContainer";

import { BrowserRouter, Route, Switch } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <div className="container">
        <NavBar />
        <Switch>
          <Route exact path="/" component={HomePage} exact />
          <Route path="/volunteers" component={VolunteersPage} />
          <Route path="/nar" component={AssetRequestContainer} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
