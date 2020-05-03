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
          <td width="20%">{volunteerInfo.volunteer_name}</td>
          <td width="20%">[experience]</td>
          <td width="20%">{volunteerInfo.contact_info[0].detail}</td>
          <td>
            <Button
              className="btn-warning"
              onClick={this.toggleQualificationsVisibility}
            >
              View
            </Button>
          </td>
          <td>
            <input
              type="checkbox"
              id="availability"
              onClick={this.handleToggleColour}
            />
            Confirmed
          </td>
        </tr>
      </React.Fragment>
    );
  }
}

export default Volunteer;
