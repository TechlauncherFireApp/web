import React, { Component } from "react";
import AssetCrew from "./assetCrew";
import { Button } from "react-bootstrap";

class RecommendationPage extends Component {
  state = {
    vols: [
      { ID: 1, Pos: "Driver", Name: "Caleb Addison" },
      { ID: 2, Pos: "Crew Leader", Name: "Stavros Dimos" },
      { ID: 3, Pos: "Firefighter", Name: "Tom Willis" },
      { ID: 4, Pos: "Firefighter", Name: "Amandeep Singh" },
      { ID: 5, Pos: "Firefighter", Name: "Cyrus Safdar" },
    ],
  };

  render() {
    return (
      //example format of a 'vehicle recommendation' component or something of the like
      <React.Fragment>
        <h4 className="mt-2">New Asset Request</h4>
        <AssetCrew volunteers={this.state.vols} />
        <AssetCrew volunteers={this.state.vols} />
        <Button className="btn-med">Save</Button>
      </React.Fragment>
    );
  }
}

export default RecommendationPage;
