import React, { Component } from "react";

import NewAssetRequest from "./NewAssetRequest";
import AssetRecommendation from "./components/assetRecommendation";

class AssetRequestContainer extends Component {
  state = {
    assetsSubmitted: false,
    request_list: [],
    volunteer_list: [],
  };

  updateRequestList = (list) => {
    const request_list = list;
    this.setState({ request_list });
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

  debugging = () => {
    /* this is a testing funtion */
    console.log(this.state.request_list);
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
            onCrewUpdate={this.handleCrewUpdate}
          />
        ) : (
          <NewAssetRequest
            onDisplayRequest={this.handleDisplayRequest}
            updateRequestList={this.updateRequestList}
          />
        )}
        <br />
        <button onClick={this.debugging} className="btn-warning">
          [debugging button]
        </button>
      </div>
    );
  }
}

export default AssetRequestContainer;
