import React from 'react';
import './position.scss';
import { Button } from 'react-bootstrap';
import { parseRolesAsString, toSentenceCase } from '../functions';
import EditModal from './editModal';

interface State {
  //related to display elements
  showEditModal: boolean; // Is the edit modal being displayed
  qualificationsVisible: boolean; //are qualifications being displayed for the volunteer in this position
}

export default class Position extends React.Component<any, State> {
  state: State = {
    showEditModal: false,
    qualificationsVisible: false,
  };

  // 1.3.5
  toggleEditModalVisibility = (): void => {
    const showEditModal = !this.state.showEditModal;
    this.setState({ showEditModal });
  };

  // 1.3.5, if a volunteer is changed update the relevant fields and propogate the change up through parent components
  updatePosition = (v: any): void => {
    let newPosition = this.props.position;
    newPosition.assigned = true;
    newPosition.volunteer = v;
    newPosition.status = 'pending';

    if (
      newPosition.roles.includes('advanced') &&
      !v.possibleRoles.includes('advanced')
    ) {
      newPosition.roles = ['basic'];
    } else if (
      newPosition.roles.includes('basic') &&
      v.possibleRoles.includes('advanced')
    ) {
      newPosition.roles = ['advanced'];
    }

    console.log('look here!', newPosition, v);

    this.setState({ qualificationsVisible: false });
    this.props.updateAsset(newPosition);
  };

  removeVolunteer = (): void => {
    let newPosition: any = this.props.position;
    newPosition.assigned = false;
    newPosition.volunteer = undefined;
    newPosition.status = 'pending';
    this.props.updateAsset(newPosition);
  };

  // 1.2.3, toggles the visibility of qualifications for this volunteer
  showHideQualifications = (): void => {
    const qualificationsVisible = !this.state.qualificationsVisible;
    this.setState({ qualificationsVisible });
  };

  // 1.2.3, handles displaying the list of qualifications
  displayQualsList = (quals: string[]): any => {
    let result: any = [];
    for (let i = 0; i < quals.length - 1; i++) {
      result.push(<div>- {quals[i]}</div>);
    }
    result.push(
      <div>
        - {quals[quals.length - 1]}{' '}
        <img src={require('../images/collapse.png')} alt="" />
      </div>
    );
    return result;
  };

  // 1.2.3
  render() {
    const { position } = this.props;
    const assigned: boolean = this.props.position.assigned;
    const bgGrey = '#ececec';
    const bgConfirmed = '#abff95';
    const bgWarning = '#FFCCCC';
    let bgColour: string;
    if (!assigned || position.status === 'rejected') {
      bgColour = bgWarning;
    } else if (position.status === 'confirmed') {
      bgColour = bgConfirmed;
    } else {
      bgColour = bgGrey;
    }
    console.log(position.positionID, bgColour);
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
            backgroundColor: bgColour,
          }}>
          <td>{parseRolesAsString(position.roles)}</td>
          {assigned ? (
            <React.Fragment>
              <td width="15%">
                {position.volunteer.firstName} {position.volunteer.lastName}
              </td>
              <td
                width="15%"
                onClick={this.showHideQualifications}
                className="view">
                {this.state.qualificationsVisible ? (
                  this.displayQualsList(position.volunteer.qualifications)
                ) : (
                  <div>
                    view <img src={require('../images/expand.png')} alt="" />
                  </div>
                )}
              </td>
              <td width="10%">{position.volunteer.mobileNo}</td>
            </React.Fragment>
          ) : (
            <React.Fragment>
              <td width="15%">
                <i>Unassigned</i>
              </td>
              <td width="15%" />
              <td width="10%" />
            </React.Fragment>
          )}
          <td width="1%">
            <Button //1.3.5
              className="btn-warning fill"
              onClick={this.toggleEditModalVisibility}>
              {assigned ? 'Change' : 'Add'}
            </Button>
          </td>
          {assigned ? (
            <td width="10%">
              <div>{toSentenceCase(position.status)}</div>
            </td>
          ) : (
            <td width="10%" />
          )}
        </tr>
      </React.Fragment>
    );
  }
}
