import React from "react";
import "./volunteer.scss";
import { Button } from "react-bootstrap";
import EditModal from "./editModal";

interface State {
  //related to display elements
  showEditModal: boolean; // Is the edit modal being displayed
  availabilityConfirmed: boolean; //TODO this needs to be made dynamic, need to see how shifts are stored in database
  qualificationsVisible: boolean; //are qualifications being displayed for the volunteer in this position
}


export default class Position extends React.Component<any, State> {
  state: State = {
    showEditModal: false,
    availabilityConfirmed: false,
    qualificationsVisible: false,
  };

  constructor(props: any) {
    super(props);
  }

  // 1.3.5
  toggleEditModalVisibility = (): void => {
    const showEditModal = !this.state.showEditModal;
    this.setState({ showEditModal });
  };

  // 1.5.4
  handleToggleColour = (): void => {
    const availabilityConfirmed = !this.state.availabilityConfirmed;
    this.setState({ availabilityConfirmed });
  };

  // 1.3.5, if a volunteer is changed update the relevant fields and propogate the change up through parent components
  updatePosition = (v: any): void => {
    let newPosition = this.props.position;
    newPosition.assigned = true;
    newPosition.volunteer = v;
    this.setState({ availabilityConfirmed: false, qualificationsVisible: false });
    this.props.updateAsset(newPosition);
  }

  removeVolunteer = (): void => {
    let newPosition: any = this.props.position;
    newPosition.assigned = false;
    newPosition.volunteer = undefined;
    this.state.availabilityConfirmed = false;
    this.props.updateAsset(newPosition);
  }

  // 1.2.3, toggles the visibility of qualifications for this volunteer
  showHideQualifications = (): void => {
    const qualificationsVisible = !this.state.qualificationsVisible;
    this.setState({ qualificationsVisible });
  }

  // 1.2.3, handles displaying the list of qualifications
  displayQualsList = (quals: string[]): any => {
    let result: any = [];
    for (let i = 0; i < quals.length - 1; i++) {
      result.push(<div>- {quals[i]}</div>)
    }
    result.push(<div>- {quals[quals.length - 1]} <img src={require("../assets/collapse.png")} /></div>)
    return result;
  }

  // 1.2.3
  render() {
    const { position } = this.props;
    const assigned: boolean = this.props.position.assigned;
    const bgColourNotConfirmed = "#ececec";
    const bgColourConfirmed = "#abff95";

    return (
      <React.Fragment>

        <EditModal //1.3.5
          show={this.state.showEditModal}
          onHide={this.toggleEditModalVisibility}
          onSave={(v: any) => this.updatePosition(v)}
          removeVolunteer={this.removeVolunteer}
          volunteerList={this.props.volunteerList}
          assignedVolunteers={this.props.assignedVolunteers}
          position={this.props.position}
        />

        <tr
          key={position.positionID}
          className="body"
          style={{
            backgroundColor: this.state.availabilityConfirmed
              ? bgColourConfirmed
              : bgColourNotConfirmed,
          }}
        >
          <td>{position.role[0]}</td> {/* TODO fix this to handle mutltiple rows */}
          {assigned ?
            <React.Fragment>
              <td width="15%">{position.volunteer.firstName} {position.volunteer.lastName}</td>
              <td width="15%" onClick={this.showHideQualifications} className="view">
                {this.state.qualificationsVisible ?
                  this.displayQualsList(position.volunteer.qualifications)
                  : <div>view <img src={require("../assets/expand.png")} /></div>}
              </td>
              <td width="10%">{position.volunteer.mobileNo}</td>
            </React.Fragment>
            :
            <React.Fragment>
              <td width="15%"><i>Unassigned</i></td>
              <td width="15%" />
              <td width="10%" />
            </React.Fragment>
          }
          <td width="1%">
            <Button //1.3.5
              className="btn-warning"
              onClick={this.toggleEditModalVisibility}
            >
              {assigned ? "Change" : "Add"} {/* TODO unsure if this syntax will work */}
            </Button>
          </td>
          {assigned ?
            <td width="10%">
              <div >
                <input //1.5.4
                  className="confirm"
                  type="checkbox"
                  id="availability"
                  checked={this.state.availabilityConfirmed}
                  onClick={this.handleToggleColour}
                />
            Confirmed
            </div>
            </td> :
            <td width="10%" />
          }
        </tr>
      </React.Fragment>
    );
  }
}
