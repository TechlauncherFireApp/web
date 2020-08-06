import React, { Component } from "react";
import { Button } from "react-bootstrap";
import EditModal from "./editModal";
import "./volunteer.scss";

/* User Story Map references (Ctrl + F the following reference numbers to find associated code) 
 1.3.5 - I want to be able to manually add, remove, and swap volunteers to assets. 
 1.2.3 - I want to be shown a list of recommended volunteers with their respective vehicle assignments, contact info, and qualifications 
 1.5.4 - I want to be able to mark that a volunteer has confirmed their availability for this assignment */

class Volunteer extends Component {
  state = {
    showEditModal: false,
    availablilityConfirmed: false,
    qualificationsVisible: false,
  };

  // 1.3.5
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
  toggleEditModalVisibility = () => {
    const showEditModal = !this.state.showEditModal;
    this.setState({ showEditModal });
=======
>>>>>>> Stashed changes
  toggleEditScreenVisibility = () => {
    const showEditScreen = !this.state.showEditScreen;
    this.setState({ showEditScreen });
>>>>>>> sprint-1-frontend
  };

  // 1.5.4
  handleToggleColour = () => {
    const availablilityConfirmed = !this.state.availablilityConfirmed;
    this.setState({ availablilityConfirmed });
  };

  // 1.3.5, if a volunteer is changed update the relevant fields and propogate the change up through parent components
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

<<<<<<< Updated upstream
=======
<<<<<<< HEAD
  removeVolunteer = () => {
    let result = {
      volunteer_id: undefined,
      position_id: this.props.volunteerInfo.position_id,
      volunteer_name: undefined,
      role: this.props.volunteerInfo.role,
      qualifications: undefined,
      contact_info: undefined,
    };
    this.state.availablilityConfirmed = false;
    this.props.updateVolunteer(result)

  }

=======
>>>>>>> sprint-1-frontend
>>>>>>> Stashed changes
  // 1.2.3, toggles the visibility of qualifications for this volunteer
  showHideQualifications = () => {
    const qualificationsVisible = !this.state.qualificationsVisible;
    this.setState({ qualificationsVisible });
  }

  // 1.2.3, handles displaying the list of qualifications
  displayQualsList = (quals) => {
    let result = [];
    for (let i = 0; i < quals.length - 1; i++) {
      result.push(<div>- {quals[i]}</div>)
    }
    result.push(<div>- {quals[quals.length - 1]} <img src={require("../../assets/collapse.png")} /></div>)
    return result;
  }

  // 1.2.3
  render() {
    const { volunteerInfo, vehicleType } = this.props;
    const bgColourNotConfirmed = "#ececec";
    const bgColourConfirmed = "#abff95";

    return (
      <React.Fragment>

<<<<<<< Updated upstream
=======
<<<<<<< HEAD
        <EditModal //1.3.5
          show={this.state.showEditModal}
          onHide={this.toggleEditModalVisibility}
=======
>>>>>>> Stashed changes
        <EditScreenModal //1.3.5
          show={this.state.showEditScreen}
          onHide={this.toggleEditScreenVisibility}
>>>>>>> sprint-1-frontend
          onSave={(newVolunteerInfo) => this.updateVolunteer(newVolunteerInfo)}
          removeVolunteer={this.removeVolunteer}
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
            <Button //1.3.5
              className="btn-warning"
              onClick={this.toggleEditModalVisibility}
            >
              Change
            </Button>
          </td>
          <td width="10%">

            <div >
              <input //1.5.4
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
