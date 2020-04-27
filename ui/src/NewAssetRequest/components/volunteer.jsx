import React, { Component } from "react";
import { Button } from "react-bootstrap";
import QualificationsModal from "./qualificationsModal";

class Volunteer extends Component {
  state = {
    showQualifications: false,
  };

  toggleQualificationsVisibility = () => {
    const showQualifications = !this.state.showQualifications;
    this.setState({ showQualifications });
  };

  render() {
    const { volunteerInfo } = this.props;

    return (
      <React.Fragment>
        <QualificationsModal
          show={this.state.showQualifications}
          onHide={this.toggleQualificationsVisibility}
          volunteer={volunteerInfo}
        />

        <tr key={volunteerInfo.volunteer_id}>
          <td>{volunteerInfo.role}</td>
          <td>{volunteerInfo.volunteer_name}</td>
          <td>[experience]</td>
          <td>{volunteerInfo.contact_info}</td>
          <td>
            <Button
              onClick={this.toggleQualificationsVisibility}
              className="btn-warning"
            >
              Edit
            </Button>
          </td>
        </tr>
      </React.Fragment>
    );
  }
}

export default Volunteer;
