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
    for (let i = 0; i < vehicleTimes.length; i++) {
      vehicleList[i].startDateTime = vehicleTimes[i].startDateTime;
      vehicleList[i].endDateTime = vehicleTimes[i].endDateTime;
    }
    this.state.vehicleListComplete = vehicleList;

    console.log(this.state.vehicleListComplete);
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
