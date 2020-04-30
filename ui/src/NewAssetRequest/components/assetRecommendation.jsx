import React, { Component } from "react";
import AssetCrew from "./assetCrew";
import { Button } from "react-bootstrap";

class AssetRecommendation extends Component {
  convertFromTimeblock = (timeblock) => {
    // This processing can be completed avoided by passing the time and date directly from the request component?
    const day = Math.floor(timeblock / 48);
    let hour = Math.floor((timeblock % 48) / 2);
    const halfhour = timeblock % 2 === 0 ? ":00" : ":30";
    let isAM = hour >= 12 ? " PM" : " AM";
    if (hour >= 13) {
      hour = hour - 12;
    }
    console.log(day, hour + halfhour + isAM);
  };

  render() {
    return (
      //example format of a 'vehicle recommendation' component or something of the like
      <React.Fragment>
        <h4 className="mt-2">New Asset Request</h4>
        {this.props.volunteer_list.map((vl) => (
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
