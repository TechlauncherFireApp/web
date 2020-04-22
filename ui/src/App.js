import React from "react";
import "./App.css";

import NavBar from "./components/navbar";
import RecommendationPage from "./components/recommendationPage";
import VolunteersPage from "./components/volunteersPage";
import HomePage from "./components/homePage";
import AssetRequestPage from "./components/assetRequestPage";

import { BrowserRouter, Route, Switch } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <div className="container">
        <NavBar />

        <Switch>
          <Route path="/" component={HomePage} exact />
          <Route path="/assetRequest" component={AssetRequestPage} />
          <Route path="/recommendation" component={RecommendationPage} />
          <Route path="/volunteers" component={VolunteersPage} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
