import React, { Component } from "react";

import NewAssetRequest from "./NewAssetRequest";
import AssetRecommendation from "./components/assetRecommendation";


/* User Story Map references (Ctrl + F the following reference numbers to find associated code) 
 1.3.5 - I want to be able to manually add, remove, and swap volunteers to assets. 
 1.2.3 - I want to be shown a list of recommended volunteers with their respective vehicle assignments, contact info, and qualifications */

class AssetRequestContainer extends Component {
  state = {
    assetsSubmitted: false,
    vehicleTimes: [],
    vehicleList: [],
    volunteerList: [],
    assignedVolunteers: new Map(),
  };

  updateVehicleTimes = (list) => {
    this.setState({ vehicleTimes: list });
  };

  // 1.3.5, when volunteers are changed ensure that the root vehicle list is up to date
  updateVehicle = (newVehicle) => {
    let vehicleList = this.state.vehicleList;
    for (let i = 0; i < vehicleList.length; i++) {
      if (vehicleList[i].asset_id === newVehicle.asset_id) vehicleList[i] = newVehicle;
    }
    this.identifyAssignedVolunteers(vehicleList);
    this.setState({ vehicleList });
  };

  handleDisplayRequest = (outputVehicleList, outputVolunteerList) => {
    this.identifyAssignedVolunteers(outputVehicleList);
    const assetsSubmitted = !this.state.assetsSubmitted;
    this.setState({ assetsSubmitted, vehicleList: outputVehicleList, volunteerList: outputVolunteerList });

  };

  // This function ensures that the root volunteer list is up to date after changes are made
  identifyAssignedVolunteers = (list) => {
    //create a new map
    let map = new Map();
    // for each vehicle in the request
    list.map((v) => {
      // for each volunteer in the vehicle
      v.volunteers.map((vol) => {
        // create a map entry for them
        vol.volunteer_id !== undefined && map.set(vol.volunteer_id, { asset_id: v.asset_id, position: vol.position_id })
      })
    })
    //set the state to the new map
    this.setState({ assignedVolunteers: map });
    console.log(map);
  }

  handleSaveRequest = () => {
    /* Stub function for now, just takes you back to the asset request screen */
    const assetsSubmitted = !this.state.assetsSubmitted;
    this.setState({ assetsSubmitted });
  };


  // 1.2.3 nested components are used to display an asset request. The heirarchy is assetRequestContainer > AssetRecommendation > AssetCrew(s) > Volunteer(s)
  render() {
    return (
      <React.Fragment>
        {this.state.assetsSubmitted ? (
          <AssetRecommendation
            onSaveRequest={this.handleSaveRequest}
            vehicleList={this.state.vehicleList}
            vehicleTimes={this.state.vehicleTimes}
            updateVehicle={(vehicle) => this.updateVehicle(vehicle)} //1.3.5
            volunteerList={this.state.volunteerList}
            assignedVolunteers={this.state.assignedVolunteers}
          />
        ) : (
            <NewAssetRequest
              onDisplayRequest={this.handleDisplayRequest}
              updateVehicleTimes={this.updateVehicleTimes}
            />
          )}
      </React.Fragment>
    );
  }
}

export default AssetRequestContainer;
