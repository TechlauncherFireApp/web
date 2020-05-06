import React, { Component } from "react";
import { Button } from "react-bootstrap";
import QualificationsModal from "./qualificationsModal";
import EditScreenModal from "./editScreenModal";
import "./Request.scss";

class Volunteer extends Component {
  state = {
    showQualifications: false,
    showEditScreen: false,
    availablilityConfirmed: false,
  };

  toggleQualificationsVisibility = () => {
    const showQualifications = !this.state.showQualifications;
    this.setState({ showQualifications });
  };

  toggleEditScreenVisibility = () => {
    const showEditScreen = !this.state.showEditScreen;
    this.setState({ showEditScreen });
  };

  handleToggleColour = () => {
    const availablilityConfirmed = !this.state.availablilityConfirmed;
    this.setState({ availablilityConfirmed });
  };

  updateVolunteer = (newVolunteerInfo) => {
    newVolunteerInfo.role = this.props.volunteerInfo.role;
    newVolunteerInfo.position_id = this.props.volunteerInfo.position_id;
    this.state.availablilityConfirmed = false;
    this.props.updateVolunteer(newVolunteerInfo);
  }

  render() {
    const { volunteerInfo, vehicleType } = this.props;
    const bgColourNotConfirmed = "#ececec";
    const bgColourConfirmed = "#abff95";

    return (
      <React.Fragment>
        <QualificationsModal
          show={this.state.showQualifications}
          onHide={this.toggleQualificationsVisibility}
          volunteer={volunteerInfo}
        />

        <EditScreenModal
          show={this.state.showEditScreen}
          onHide={this.toggleEditScreenVisibility}
          onSave={(newVolunteerInfo) => this.updateVolunteer(newVolunteerInfo)}
          volunteer={volunteerInfo}
          vehicleType={vehicleType}
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
          <td width="15%">{volunteerInfo.volunteer_name}</td>
          <td width="15%">[experience]</td>
          <td width="15%">{volunteerInfo.contact_info[0].detail}</td>
          <td>
            <Button
              className="btn-warning"
              onClick={this.toggleQualificationsVisibility}
            >
              View
            </Button>
          </td>
          <td>
            <Button
              className="btn-warning"
              onClick={this.toggleEditScreenVisibility}
            >
              Change
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
