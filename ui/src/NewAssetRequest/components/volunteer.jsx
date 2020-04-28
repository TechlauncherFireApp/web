import React, { Component } from "react";
import { Button } from "react-bootstrap";
import QualificationsModal from "./qualificationsModal";
import "./Request.scss";

class Volunteer extends Component {
  state = {
    showQualifications: false,
    availablilityConfirmed: false,
  };

  toggleQualificationsVisibility = () => {
    const showQualifications = !this.state.showQualifications;
    this.setState({ showQualifications });
  };

  handleToggleColour = () => {
    const availablilityConfirmed = !this.state.availablilityConfirmed;
    this.setState({ availablilityConfirmed });
  };

  render() {
    const { volunteerInfo } = this.props;
    const bgColourNotConfirmed = "#ececec";
    const bgColourConfirmed = "#abff95";

    return (
      <React.Fragment>
        <QualificationsModal
          show={this.state.showQualifications}
          onHide={this.toggleQualificationsVisibility}
          volunteer={volunteerInfo}
        />

        <tr
          key={volunteerInfo.volunteer_id}
          style={{
            backgroundColor: this.state.availablilityConfirmed
              ? bgColourConfirmed
              : bgColourNotConfirmed,
          }}
        >
          <td>{volunteerInfo.role}</td>
          <td>{volunteerInfo.volunteer_name}</td>
          <td>[experience]</td>
          <td>{volunteerInfo.contact_info}</td>
          <td>
            <Button
              className="btn-warning"
              onClick={this.toggleQualificationsVisibility}
            >
              Edit
            </Button>
          </td>
          <td>
            <input
              type="checkbox"
              id="availability"
              onClick={this.handleToggleColour}
            />
            Available
          </td>
        </tr>
      </React.Fragment>
    );
  }
}

export default Volunteer;
