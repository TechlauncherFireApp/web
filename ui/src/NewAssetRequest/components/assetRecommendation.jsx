import React, { Component } from "react";
import AssetCrew from "./assetCrew";
import { Button } from "react-bootstrap";

class AssetRecommendation extends Component {
  state = {
    volunteer_list_complete: [],
  };

  constructor(props) {
    super(props);
    const vehicle_list = props.vehicle_list;
    let volunteer_list = props.volunteer_list;
    for (let i = 0; i < vehicle_list.length; i++) {
      volunteer_list[i].startDateTime = vehicle_list[i].startDateTime;
      volunteer_list[i].endDateTime = vehicle_list[i].endDateTime;
    }
    this.state.volunteer_list_complete = volunteer_list;

    console.log(this.state.volunteer_list_complete);
  }

  render() {
    return (
      <React.Fragment>
        <h4 className="mt-2">New Asset Request</h4>
        {this.state.volunteer_list_complete.map((vl) => (
          <AssetCrew
            key={vl.asset_id}
            recommendationInfo={vl}
            onUpdateCrew={this.onCrewUpdate}
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
