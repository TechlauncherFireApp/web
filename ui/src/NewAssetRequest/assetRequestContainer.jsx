import React, { Component } from "react";

import NewAssetRequest from "./NewAssetRequest";
import AssetRecommendation from "./components/assetRecommendation";

class AssetRequestContainer extends Component {
  state = {
    assetsSubmitted: false,
    vehicle_list: [],
    volunteer_list: [],
  };

  updateVehicleList = (list) => {
    const vehicle_list = list;
    this.setState({ vehicle_list });
  };

  handleDisplayRequest = (outputVolunteerList) => {
    const assetsSubmitted = !this.state.assetsSubmitted;
    const volunteer_list = outputVolunteerList;
    this.setState({ assetsSubmitted, volunteer_list });
  };

  handleSaveRequest = () => {
    /* Stub function for now, just takes you back to the asset request screen */
    const assetsSubmitted = !this.state.assetsSubmitted;
    this.setState({ assetsSubmitted });
  };

  handleCrewUpdate = (assetId, newVolunteer) => {
    console.log("handle update crew called", assetId, newVolunteer);
    // stub for prototype 2
  };

  render() {
    return (
      <div>
        {this.state.assetsSubmitted ? (
          <AssetRecommendation
            onSaveRequest={this.handleSaveRequest}
            volunteer_list={this.state.volunteer_list}
            vehicle_list={this.state.vehicle_list}
            onCrewUpdate={this.handleCrewUpdate}
          />
        ) : (
          <NewAssetRequest
            onDisplayRequest={this.handleDisplayRequest}
            updateVehicleList={this.updateVehicleList}
          />
        )}
      </div>
    );
  }
}

export default AssetRequestContainer;
