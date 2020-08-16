import React, { Component } from "react";
import { Button } from "react-bootstrap";
import EditModal from "./editModal";
import "./volunteer.scss";

/* User Story Map references (Ctrl + F the following reference numbers to find associated code) 
 1.3.5 - I want to be able to manually add, remove, and swap volunteers to assets. 
 1.2.3 - I want to be shown a list of recommended volunteers with their respective vehicle assignments, contact info, and qualifications 
 1.5.4 - I want to be able to mark that a volunteer has confirmed their availability for this assignment */

class EmptyVolunteer extends Component {
  state = {
    showEditModal: false,
  };

  toggleEditModalVisibility = () => {
    const showEditModal = !this.state.showEditModal;
    this.setState({ showEditModal });
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



  // 1.2.3
  render() {
    const { volunteerInfo, vehicleType } = this.props;

    return (
      <React.Fragment>

        <EditModal //1.3.5
          show={this.state.showEditModal}
          onHide={this.toggleEditModalVisibility}
          onSave={(newVolunteerInfo) => this.updateVolunteer(newVolunteerInfo)}
          removeVolunteer={this.removeVolunteer}
          volunteer={volunteerInfo}
          vehicleType={vehicleType}
          volunteerList={this.props.volunteerList}
          assignedVolunteers={this.props.assignedVolunteers}
          emptyVolunteer={true}
        />

        <tr
          className="body"
          style={{ backgroundColor: '#ececec' }}
        >
          <td>{volunteerInfo.role}</td>
          <td width="15%"><i>Unassigned</i></td>
          <td width="15%" >          </td>
          <td width="10%"></td>
          <td width="1%">
            <Button //1.3.5
              className="btn-warning"
              onClick={this.toggleEditModalVisibility}
            >
              Add
            </Button>
          </td>
          <td width="10%">

          </td>
        </tr>
      </React.Fragment>
    );
  }
}

export default EmptyVolunteer;
