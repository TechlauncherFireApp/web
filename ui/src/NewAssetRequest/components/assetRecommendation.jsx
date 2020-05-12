import React, { Component } from "react";
import AssetCrew from "./assetCrew";
import { Button } from "react-bootstrap";

class AssetRecommendation extends Component {
  state = {
    vehicleListComplete: [],
  };

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

  render() {
    return (
      <React.Fragment>
        <h4 className="mt-2">New Asset Request</h4>
        {this.state.vehicleListComplete.map((v) => (
          <AssetCrew
            key={v.asset_id}
            vehicle={v}
            updateVehicle={(v) => this.props.updateVehicle(v)}
            volunteerList={this.props.volunteerList}
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
