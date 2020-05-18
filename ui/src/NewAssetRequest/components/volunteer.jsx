import React, { Component } from "react";
import { Button } from "react-bootstrap";
import EditScreenModal from "./editScreenModal";
import "./volunteer.scss";

class Volunteer extends Component {
  state = {
    showEditScreen: false,
    availablilityConfirmed: false,
    qualificationsVisible: false,
  };

  toggleEditScreenVisibility = () => {
    const showEditScreen = !this.state.showEditScreen;
    this.setState({ showEditScreen });
  };

  handleToggleColour = () => {
    const availablilityConfirmed = !this.state.availablilityConfirmed;
    this.setState({ availablilityConfirmed });
  };

  updateVolunteer = (v) => {
    let result = {
      volunteer_id: v.id,
      position_id: this.props.volunteerInfo.position_id,
      volunteer_name: v.name,
      role: this.props.volunteerInfo.role,
      qualifications: v.qualifications,
      contact_info: v.contact_info,
    };
    this.state.availablilityConfirmed = false;
    this.props.updateVolunteer(result);
  }

  showHideQualifications = () => {
    const qualificationsVisible = !this.state.qualificationsVisible;
    this.setState({ qualificationsVisible });
  }

  displayQualsList = (quals) => {
    let result = [];
    for (let i = 0; i < quals.length - 1; i++) {
      result.push(<div>- {quals[i]}</div>)
    }
    result.push(<div>- {quals[quals.length - 1]} <img src={require("../../assets/collapse.png")} /></div>)
    return result;
  }

  render() {
    const { volunteerInfo, vehicleType } = this.props;
    const bgColourNotConfirmed = "#ececec";
    const bgColourConfirmed = "#abff95";

    return (
      <React.Fragment>

        <EditScreenModal
          show={this.state.showEditScreen}
          onHide={this.toggleEditScreenVisibility}
          onSave={(newVolunteerInfo) => this.updateVolunteer(newVolunteerInfo)}
          volunteer={volunteerInfo}
          vehicleType={vehicleType}
          volunteerList={this.props.volunteerList}
          assignedVolunteers={this.props.assignedVolunteers}
        />

        <tr
          key={volunteerInfo.volunteer_id}
          className="body"
          style={{
            backgroundColor: this.state.availablilityConfirmed
              ? bgColourConfirmed
              : bgColourNotConfirmed,
          }}
        >
          <td>{volunteerInfo.role}</td>
          <td width="15%">{volunteerInfo.volunteer_name}</td>
          <td width="15%" onClick={this.showHideQualifications} className="view">

            {this.state.qualificationsVisible ?
              this.displayQualsList(volunteerInfo.qualifications)
              : <div>view <img src={require("../../assets/expand.png")} /></div>}

          </td>
          <td width="10%">{volunteerInfo.contact_info[0].detail}</td>
          <td width="1%">
            <Button
              className="btn-warning"
              onClick={this.toggleEditScreenVisibility}
            >
              Change
            </Button>
          </td>
          <td width="10%">
            <div >
              <input
                className="confirm"
                type="checkbox"
                id="availability"
                onClick={this.handleToggleColour}
              />
            Confirmed
            </div>
          </td>
        </tr>
      </React.Fragment>
    );
  }
}

export default Volunteer;
