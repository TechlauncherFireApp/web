import React, { Component } from "react";

import NewAssetRequest from "./NewAssetRequest";
import AssetRecommendation from "./components/assetRecommendation";

class AssetRequestContainer extends Component {
  state = {
    assetsSubmitted: false,
    vehicleTimes: [],
    vehicleList: [],
    // TO TOM - can change volunteerList to [] after you link the back end
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
    },
    {
      id: 5123,
      name: "Joe Blob",
      role: "Driver",
      qualifications: [
        "heavy rigid license",
        "pump training",
        "crew leader training",
        "advanced training",
      ],
      contact_info: [{ detail: "0412 490 340" }],
    },
    {
      id: 649,
      name: "Jane Doe",
      role: "Advanced",
      qualifications: ["advanced training", "crew leader training"],
      contact_info: [{ detail: "0412 490 340" }],
    },
    {
      id: 5342,
      name: "person three",
      role: "Advanced",
      qualifications: ["advanced training", "crew leader training"],
      contact_info: [{ detail: "0412 490 340" }],
    },
    {
      id: 423,
      name: "person four",
      role: "Advanced",
      qualifications: ["advanced training", "crew leader training"],
      contact_info: [{ detail: "0412 490 340" }],
    },
    {
      id: 123,
      name: "person five",
      role: "Advanced",
      qualifications: ["advanced training", "crew leader training"],
      contact_info: [{ detail: "0412 490 340" }],
    },
    {
      id: 32,
      name: "Mary Blank",
      role: "Driver",
      qualifications: [
        "heavy rigid license",
        "pump training",
        "crew leader training",
        "advanced training",
      ],
      contact_info: [{ detail: "0412 490 340" }],
    },
    {
      id: 89,
      name: "John Connor",
      role: "Advanced",
      qualifications: ["advanced training", "crew leader training"],
      contact_info: [{ detail: "0412 490 340" }],
    },],
    assignedVolunteers: new Map(),
  };

  updateVehicleTimes = (list) => {
    this.setState({ vehicleTimes: list });
  };

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

  identifyAssignedVolunteers = (list) => {
    //create a new map
    let map = new Map();
    // for each vehicle in the request
    list.map((v) => {
      // for each volunteer in the vehicle
      v.volunteers.map((vol) => {
        // create a map entry for them
        map.set(vol.volunteer_id, { asset_id: v.asset_id, position: vol.position_id })
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
            assignedVolunteers={this.state.assignedVolunteers}
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
