import React, { Component } from "react";
import AssetCrew from "./assetCrew";
import { Button } from "react-bootstrap";

/* User Story Map references (Ctrl + F the following reference numbers to find associated code) 
 1.3.5 - I want to be able to manually add, remove, and swap volunteers to assets. 
 1.2.3 - I want to be shown a list of recommended volunteers with their respective vehicle assignments, contact info, and qualifications */

class AssetRecommendation extends Component {
  state = {
    vehicleListComplete: [],
  };

  // 1.2.3, merges the vehicle times and vehicle list to create one central list with all relevant info for display
  constructor(props) {
    super(props);
    const vehicleTimes = props.vehicleTimes;
    let vehicleList = props.vehicleList;
    let map = new Map()
    for (let i = 0; i < vehicleTimes.length; i++) {
      vehicleList[i].startDateTime = vehicleTimes[i].startDateTime;
      vehicleList[i].endDateTime = vehicleTimes[i].endDateTime;
      if (map.has(vehicleList[i].asset_class)) {
        const old = map.get(vehicleList[i].asset_class)
        map.set(vehicleList[i].asset_class, old + 1);
      } else {
        map.set(vehicleList[i].asset_class, 1)

      }
      vehicleList[i].number = map.get(vehicleList[i].asset_class);
    }
    this.state.vehicleListComplete = vehicleList;
  }

  //1.2.3, handles display
  render() {
    return (
      <React.Fragment>
        <h4 className="mt-2">New Asset Request</h4>
        <hr />
        {this.state.vehicleListComplete.map((v) => (
          <AssetCrew
            key={v.asset_id}
            vehicle={v}
            updateVehicle={(v) => this.props.updateVehicle(v)} //1.3.5
            volunteerList={this.props.volunteerList}
            assignedVolunteers={this.props.assignedVolunteers}
          />
        ))}
        <Button onClick={this.props.onSaveRequest} className="btn-med">
          Save
        </Button>
      </React.Fragment>
    );
  }
}

export default AssetRecommendation;
