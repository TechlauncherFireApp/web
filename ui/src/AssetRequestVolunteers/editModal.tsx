import React from "react";
import "./editModal.scss";
import { contains, parseDateTime, parseRolesAsString, isAvailable, toSentenceCase } from "../functions";
import { Modal, Button, Table } from "react-bootstrap";

interface State {
  //related to display elements
  searchValue: string;
  filteredVolunteerList: any; //list of volunteers
  searchResults: any; //list of volunteers
  filter: {
    position: boolean; //should search results be filtered by position
  };
  //related to data needed 
  volunteerList: any;  //list of volunteers
  selectedVolunteer: any; //the replacement volunteer selected from the list
}

export default class EditModal extends React.Component<any, State> {

  state: State = {
    searchValue: "",
    filteredVolunteerList: [],
    searchResults: [],
    filter: {
      position: true,
    },
    volunteerList: [],
    selectedVolunteer: undefined,
  };

  constructor(props: any) {
    super(props);
    const volunteerList: any = props.volunteerList;
    this.state.volunteerList = volunteerList;
    const l = this.filterVolunteerList(volunteerList, this.state.filter);
    this.state.filteredVolunteerList = l;
    this.state.searchResults = l;
  }

  insertSearch = (e: any): void => {
    // Get Value
    if (!(typeof e === 'string')) {
      e = e.target.value;
      this.state.searchValue = e;
    }

    // Validate Value
    if (!contains(e)) { this.setState({ searchResults: this.state.filteredVolunteerList }); return; }
    e = e.toLowerCase();

    // Search Value
    let a = [];
    for (let x of this.state.filteredVolunteerList) {
      let name: string = x.firstName + " " + x.lastName;
      if (name.toLowerCase().indexOf(e) >= 0) a.push(x);
    }

    // Search Found
    if (a.length > 0) this.setState({ searchResults: a });
    else this.setState({ searchResults: "" });
  };

  saveChange = (): void => {
    if (!(typeof this.state.selectedVolunteer === 'undefined')) {
      const map: any = this.props.assignedVolunteers;
      const vol: any = this.state.selectedVolunteer;
      if (this.props.position.assigned && vol.ID === this.props.position.volunteer.ID) {
        alert("You can't change a volunteer to themselves")
      } else if (map.has(vol.ID)) {
        alert(vol.name + " is already assigned to asset " + map.get(vol.ID).shiftID + " position " + map.get(vol.ID).positionID)
      } else {
        this.props.onSave(this.state.selectedVolunteer)
        this.onHide();
      }
    } else {
      this.onHide();
    }
  }

  removeVolunteer = (): void => {
    this.props.removeVolunteer();
    this.onHide();
  }

  togglePositionFilter = (): void => {
    let filter: { position: boolean } = this.state.filter;
    filter.position = !filter.position;
    const l = this.filterVolunteerList(this.state.volunteerList, filter);
    const searchValue = this.state.searchValue;
    if (searchValue == "") {
      this.setState({ filter, filteredVolunteerList: l, searchResults: l });
    } else {
      this.setState({ filter, filteredVolunteerList: l }, () => {
        this.insertSearch(searchValue);
      });
    }
  }

  filterVolunteerList = (allVolunteers: any, filter: { position: boolean }): any => {

    // exclude the volunteer themselves from this list (position.assignedVolunteer.id if position.assignedVolunteer != null)
    // rework this to do both filters in one pass

    const targetRoles = this.props.position.roles;
    let list = [];
    if (filter.position) {
      //let v: any;
      for (const v of allVolunteers) {
        targetRoles.every((r: string) => v.possibleRoles.includes(r)) && list.push(v); //if the volunteer in question can fulfil all vehicle requirements add this volunteer to the list
      }
    } else {
      list = [...allVolunteers];
    }

    // work out who is available
    let yes: any = [];
    let no: any = [];
    for (const l of list) {
      let l_copy = { ...l };
      if (isAvailable(l.availabilities, { startTime: this.props.position.startTime, endTime: this.props.position.endTime })) {

        l_copy.available = true;
        yes.push(l_copy)
      } else {

        l_copy.available = false;
        no.push(l_copy);
      }
    }
    list = [...yes, ...no];
    return list.filter(l => (!this.props.position.assigned || l.ID != this.props.position.volunteer.ID));
  }

  onHide = (): void => {
    //need to reset if you've selected a volunteer.
    const l = this.filterVolunteerList(this.state.volunteerList, { position: true });
    this.setState({ filter: { position: true }, searchValue: "", searchResults: l, filteredVolunteerList: l, selectedVolunteer: undefined })
    this.props.onHide();
  }

  generateModalHeading = (): string => {
    // UNTESTED
    const position = this.props.position;
    let s: string = ""
    s += toSentenceCase(position.assetClass) + " - ";
    s += parseRolesAsString(position.roles);
    return s
  }

  render() {
    const { position } = this.props;

    return (
      <Modal
        {...this.props}//TODO unsure what this does
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
        backdrop="static"
      >
        <Modal.Header closeButton closeLabel="cancel" onHide={this.onHide}>
          <Modal.Title id="contained-modal-title-vcenter">
            {this.generateModalHeading()}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>{parseDateTime(position.startTime, position.endTime)}</p>
          {!this.props.position.assigned ?
            <p><i>This position is currently unassigned</i></p> :
            <p>Assigned to: <b>{position.volunteer.firstName} {position.volunteer.lastName}</b></p>
          }

          <form>
            <input id='searchBar' type="text" placeholder="Search Volunteer via Name" value={this.state.searchValue} onChange={this.insertSearch} />
            &nbsp;
            <input
              className="positionFilter"
              type="checkbox"
              id="positionFilter"
              defaultChecked
              onClick={this.togglePositionFilter}
            /> Only show '{parseRolesAsString(position.roles)}'s



            <hr />
            <div className="con-vols">
              {((typeof this.state.searchResults === "object") && this.state.searchResults.length > 0) &&
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Qualifications</th>
                      <th>Available For This Shift</th>
                    </tr>
                  </thead>
                  <tbody>
                    {this.state.searchResults.map((t: any) => (
                      <tr className="view" onClick={() => { this.setState({ selectedVolunteer: t }); }}>
                        <td>{this.props.assignedVolunteers.has(t.ID) ? <div title="Already assigned">{t.firstName}{" "}{t.lastName}{" "}<img src={require("../assets/assigned.png")} /></div> : <div>{t.firstName}{" "}{t.lastName}</div>}</td>
                        <td>
                          {t.qualifications.map((q: string) => <div>- {q}</div>)}
                        </td>
                        <td>{t.available ? "Available" : "Unavailable"}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              }
              {(this.state.searchResults === "") &&
                <p>Nothing found</p>
              }
            </div>
          </form>
          <div className="con-vol">
            {position.assigned ?
              <p>{position.volunteer.firstName} {position.volunteer.lastName} will be replaced with:</p> :
              <p>Position will be assigned to:</p>}
            {contains(this.state.selectedVolunteer) ?
              <Table striped bordered hover size="sm">
                <tbody>
                  <tr>
                    <td>{this.state.selectedVolunteer.firstName} {this.state.selectedVolunteer.lastName}</td>
                    <td>
                      {this.state.selectedVolunteer.qualifications.map((q: string) => <div>- {q}</div>)}
                    </td>
                    <td>{this.state.selectedVolunteer.available ? "Available" : "Unavailable"}</td>
                  </tr>
                </tbody>
              </Table> :
              <i>Select a volunteer</i>

            }
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button className="danger" onClick={this.saveChange}>
            {position.assigned ?
              "Replace"
              : "Assign Volunteer"}
          </Button>
          {position.assigned &&
            <Button className="danger" onClick={this.removeVolunteer}>
              Remove
            </Button>
          }
          <Button className="danger" onClick={this.onHide}>
            Cancel
          </Button>
        </Modal.Footer>
      </Modal>
    );
  }
}