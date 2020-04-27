import React, { Component } from "react";
import AssetCrew from "./assetCrew";
import { Button } from "react-bootstrap";

class AssetRecommendation extends Component {
  state = {
    /* 'volunteer-lsit' is some dummy data for what would be returned from the back end */
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
            volunteer_name: "John Blank",
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

  render() {
    return (
      //example format of a 'vehicle recommendation' component or something of the like
      <React.Fragment>
        <h4 className="mt-2">New Asset Request</h4>
        {this.state.volunteer_list.map((vl) => (
          <AssetCrew key={vl.asset_id} recommendationInfo={vl} />
        ))}
        <Button onClick={this.props.onSaveRequest} className="btn-med">
          Save
        </Button>
      </React.Fragment>
    );
  }
}

export default AssetRecommendation;
