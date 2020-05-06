import React, { Component } from "react";

import NewAssetRequest from "./NewAssetRequest";
import AssetRecommendation from "./components/assetRecommendation";

class AssetRequestContainer extends Component {
  state = {
    assetsSubmitted: false,
    vehicleTimes: [],
    vehicleList: [],
  };

  updateVehicleTimes = (list) => {
    const vehicleTimes = list;
    this.setState({ vehicleTimes });
  };

  handleDisplayRequest = (outputVehicleList) => {
    const assetsSubmitted = !this.state.assetsSubmitted;
    const vehicleList = outputVehicleList;
    this.setState({ assetsSubmitted, vehicleList });
  };

  handleSaveRequest = () => {
    /* Stub function for now, just takes you back to the asset request screen */
    const assetsSubmitted = !this.state.assetsSubmitted;
    this.setState({ assetsSubmitted });
  };

  updateVehicleTimes = (newList) => {
    const vehicleTimes = newList;
    this.setState({ vehicleTimes });
  }

  updateVehicle = (newVehicle) => {

    let vehicleList = this.state.vehicleList;
    for (let i = 0; i < vehicleList.length; i++) {
      if (vehicleList[i].asset_id === newVehicle.asset_id) vehicleList[i] = newVehicle;
    }
    this.setState({ vehicleList });
  };

  render() {
    return (
      <div>
        {this.state.assetsSubmitted ? (
          <AssetRecommendation
            onSaveRequest={this.handleSaveRequest}
            vehicleList={this.state.vehicleList}
            vehicleTimes={this.state.vehicleTimes}
            updateVehicle={(vehicle) => this.updateVehicle(vehicle)}
          />
        ) : (
            <NewAssetRequest
              onDisplayRequest={this.handleDisplayRequest}
              updateVehicleTimes={this.updateVehicleTimes}
            />
          )}
      </div>
    );
  }
}

export default AssetRequestContainer;
