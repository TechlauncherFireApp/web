import React, { Component } from "react";

import NewAssetRequest from "./NewAssetRequest";
import AssetRecommendation from "./components/assetRecommendation";

class AssetRequestContainer extends Component {
  state = {
    assetsSubmitted: false,
    volunteerList: ["mary", "bob", "joe"],
  };

  handleDisplayRequest = (outputVolunteerList) => {
    const assetsSubmitted = !this.state.assetsSubmitted;
    const volunteerList = outputVolunteerList;
    this.setState({ assetsSubmitted, volunteerList });
  };

  handleSaveRequest = () => {
    /* Stub function for now, just takes you back to the asset request screen */
    const assetsSubmitted = !this.state.assetsSubmitted;
    this.setState({ assetsSubmitted });
  };

  handleShowState = () => {
    /* this is a testing funtion */
    console.log(this.state.assetsSubmitted, this.state.volunteerList);
  };

  render() {
    return (
      <div>
        {this.state.assetsSubmitted ? (
          <AssetRecommendation onSaveRequest={this.handleSaveRequest} />
        ) : (
          <NewAssetRequest onDisplayRequest={this.handleDisplayRequest} />
        )}
        <br />
        <button onClick={this.handleShowState} className="btn-warning">
          Log state [debugging]
        </button>
      </div>
    );
  }
}

export default AssetRequestContainer;
