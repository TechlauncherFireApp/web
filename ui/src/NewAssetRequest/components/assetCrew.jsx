import React, { Component } from "react";
import { Table } from "react-bootstrap";
import Volunteer from "./volunteer";

class AssetCrew extends Component {
  state = {
    showQualifications: false,
  };

  toggleQualificationsVisibility = () => {
    const showQualifications = !this.state.showQualifications;
    this.setState({ showQualifications });
  };

  render() {
    const { recommendationInfo } = this.props;

    return (
      <Table className="mt-4" striped bordered hover size="sm">
        <thead>
          <tr>
            <th width="20%">{recommendationInfo.asset_class}</th>
            <th colSpan="5">[time slot]</th>
          </tr>
        </thead>
        <tbody>
          {recommendationInfo.volunteers.map((v) => (
            <Volunteer key={v.volunteer_id} volunteerInfo={v} />
          ))}
        </tbody>
      </Table>
    );
  }
}

export default AssetCrew;
