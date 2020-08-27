import React, { Component } from "react";
import "./editModal.scss";
import { contains, parseDateTime } from "../functions";
import { Modal, Button, Table } from "react-bootstrap";
import "./volunteer.scss"

interface State {
  //related to display elements
  searchValue: string;
  filteredVolunteerList: any; //list of volunteers
  searchResults: any; //list of volunteers
  filter: {
    position: boolean; //should search results be filtered by position
    availability: boolean; //should search results be filtered by availability
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
      availability: true,
    },
    volunteerList: [],
    selectedVolunteer: undefined,
  };

  constructor(props: any) {
    super(props);
    const volunteerList: any = props.volunteerList;
    this.state.volunteerList = volunteerList;
    const l: any = this.filterVolunteerList(volunteerList, this.state.filter);
    this.state.filteredVolunteerList = l
    this.state.searchResults = l;
  }

  //TODO - this is currently (i.e you can't search)
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
      if (this.props.position.assigned && vol.id === this.props.position.volunteer.id) {
        alert("You can't change a volunteer to themselves")
      } else if (map.has(vol.id)) {
        alert(vol.name + " is already assigned to asset " + map.get(vol.id).shiftID + " position " + map.get(vol.id).positionID)
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
    let filter: { position: boolean, availability: boolean } = this.state.filter;
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

  filterVolunteerList = (baseList: any, filter: { position: boolean, availability: boolean }): any => {

    // exclude the volunteer themselves from this list (position.assignedVolunteer.id if position.assignedVolunteer != null)
    // rework this to do both filters in one pass

    const targetRole = this.props.position.role[0]; //TODO make this work for multiple roles
    let l = [];
    if (filter.position) {
      let v;
      for (v of baseList) {
        v.possibleRoles.includes(targetRole) && l.push(v);
      }
    } else {
      l = [...baseList];
    }

    if (filter.availability) {
      //TODO
    }
    return l;
  }

  onHide = (): void => {
    //need to reset if you've selected a volunteer.
    const l = this.filterVolunteerList(this.state.volunteerList, { position: true, availability: true });
    this.setState({ filter: { position: true, availability: true }, searchValue: "", searchResults: l, filteredVolunteerList: l, selectedVolunteer: undefined })
    this.props.onHide();
  }

  generateModalHeading = (): string => {
    // UNTESTED
    const position = this.props.position;
    let s: string = ""
    s += position.assetClass + " -";
    for (const r of position.role) {
      s += " " + r + "/";
    }
    return s.slice(0, -1);
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
            <div><i>This position is currently unassigned</i></div> :
            <div>Assigned to: <b>{position.volunteer.firstName} {position.volunteer.lastName}</b></div>
          }

          <br />

          <form>
            <input id='searchBar' type="text" placeholder="Search Volunteer via Name" value={this.state.searchValue} onChange={this.insertSearch} />
            &nbsp;
            <input
              className="positionFilter"
              type="checkbox"
              id="positionFilter"
              defaultChecked
              onClick={this.togglePositionFilter}
            /> Only show {position.role[0]}s {/*TODO need to make this work with multiple position roles*/}


            <hr />
            <div className="con-vols">
              {((typeof this.state.searchResults === "object") && this.state.searchResults.length > 0) &&
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Qualifications</th>
                      <th>Phone No</th>
                    </tr>
                  </thead>
                  <tbody>
                    {this.state.searchResults.map((t: any) => (
                      <tr className="view" onClick={() => { this.setState({ selectedVolunteer: t }); }}>
                        <td>{this.props.assignedVolunteers.has(t.id) ? <div title="Already assigned">{t.firstName}{" "}{t.lastName}{" "}<img src={require("../assets/assigned.png")} /></div> : <div>{t.firstName}{" "}{t.lastName}</div>}</td>
                        <td>
                          {t.qualifications.map((q: string) => <div>- {q}</div>)}
                        </td>
                        <td>{t.mobileNo}</td>
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
              <p>Position will be assigned to:</p> /* TODO make sure this works properly*/}
            {contains(this.state.selectedVolunteer) ?
              <Table striped bordered hover size="sm">
                <tbody>
                  <tr>
                    <td>{this.state.selectedVolunteer.firstName} {this.state.selectedVolunteer.lastName}</td>{/* TODO make sure this line works*/}
                    <td>
                      {this.state.selectedVolunteer.qualifications.map((q: string) => <div>- {q}</div>)}
                    </td>
                    <td>{this.state.selectedVolunteer.mobileNo}</td>{/*TODO probably not needed */}
                  </tr>
                </tbody>
              </Table> :
              <i>Select a volunteer</i>

            }
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button className="danger" onClick={this.saveChange}>
            Replace Volunteer
          </Button>
          {position.assigned &&
            <Button className="danger" onClick={this.removeVolunteer}>
              Remove Volunteer
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