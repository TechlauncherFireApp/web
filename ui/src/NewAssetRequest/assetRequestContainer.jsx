import React, { Component } from "react";

import NewAssetRequest from "./NewAssetRequest";
import AssetRecommendation from "./components/assetRecommendation";

class AssetRequestContainer extends Component {
  state = {
    assetsSubmitted: false,
    vehicleTimes: [],
    vehicleList: [],
    volunteerList: [{
      id: 1,
      name: "Cyrus",
      role: "Advanced",
      qualifications: ["advanced training", "crew leader training"],
      contact_info: [{ detail: "0412 490 340" }],
    }, {
      id: 2,
      name: "Caleb",
      role: "Basic",
      qualifications: ["village firefighter training"],
      contact_info: [{ detail: "0412 490 340" }],
    }, {
      id: 3,
      name: "Stavros",
      role: "Advanced",
      qualifications: ["advanced training", "heavy rigid license", "pump training"],
      contact_info: [{ detail: "0412 490 340" }],
    }, {
      id: 4,
      name: "Aman",
      role: "Crew Leader",
      qualifications: ["advanced training", "crew leader training"],
      contact_info: [{ detail: "0412 490 340" }],
    }, {
      id: 5,
      name: "Tom",
      role: "Driver",
      qualifications: ["advanced training", "crew leader training", "heavy rigid license"],
      contact_info: [{ detail: "0412 490 340" }],
    },],
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

    console.log("assetRequestContainer: ", vehicleList);
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
            volunteerList={this.state.volunteerList}
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
