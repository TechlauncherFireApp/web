import React, { Component } from "react";

import NewAssetRequest from "./NewAssetRequest";
import AssetRecommendation from "./components/assetRecommendation";

class AssetRequestContainer extends Component {
  state = {
    assetsSubmitted: false,
    request_list: [],
    volunteer_list: [
      {
        asset_id: 1,
        asset_class: "Medium Unit",
        start_time: 24,
        end_time: 34,
        position: [
          {
            position_id: 1,
            role: "Driver",
            qualifications: [
              "heavy rigid license",
              "pump training",
              "crew leader training",
            ],
          },
          {
            position_id: 2,
            role: "Advanced",
            qualifications: ["advanced training"],
          },
        ],
        volunteers: [
          {
            volunteer_id: 5123,
            position_id: 1,
            volunteer_name: "Joe Blob",
            role: "Driver",
            qualifications: [
              "heavy rigid license",
              "pump training",
              "crew leader training",
              "advanced training",
            ],
            contact_info: "0412 490 340",
          },
          {
            volunteer_id: 649,
            position_id: 2,
            volunteer_name: "Jane Doe",
            role: "Advanced",
            qualifications: ["advanced training", "crew leader training"],
            contact_info: "0412 490 340",
          },
        ],
      },
      {
        asset_id: 2,
        asset_class: "Light Unit",
        start_time: 24,
        end_time: 34,
        position: [
          {
            position_id: 1,
            role: "Driver",
            qualifications: [
              "heavy rigid license",
              "pump training",
              "crew leader training",
            ],
          },
          {
            position_id: 2,
            role: "Advanced",
            qualifications: ["advanced training"],
          },
        ],
        volunteers: [
          {
            volunteer_id: 5123,
            position_id: 1,
            volunteer_name: "Mary Blank",
            role: "Driver",
            qualifications: [
              "heavy rigid license",
              "pump training",
              "crew leader training",
              "advanced training",
            ],
            contact_info: "0412 490 340",
          },
          {
            volunteer_id: 649,
            position_id: 2,
            volunteer_name: "John Connor",
            role: "Advanced",
            qualifications: ["advanced training", "crew leader training"],
            contact_info: "0412 490 340",
          },
        ],
      },
    ],
  };

  updateRequestList = (list) => {
    const request_list = list;
    this.setState({ request_list });
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
