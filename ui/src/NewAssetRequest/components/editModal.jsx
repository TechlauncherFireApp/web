import React, { Component } from "react";
import "./editModal.scss";
import { contains } from "../../main.js";
import { Modal, Button, Table } from "react-bootstrap";
import "./volunteer.scss"

/* User Story Map references (Ctrl + F the following reference numbers to find associated code) 
entire class relates to 1.3.5 - I want to be able to manually add, remove, and swap volunteers to assets. */

class EditModal extends Component {
    state = {
        emptyVolunteer: null,
        searchValue: "",
        volunteerList: [],
        filteredVolunteerList: [],
        searchResults: [],
        selectedVolunteer: {
            id: null,
            name: "",
            role: null,
            qualifications: [],
            contact_info: [{ detail: "" }],
        },
        qualificationsVisible: false,
        filterByPosition: true,
    };

    constructor(props) {
        super(props);
        const volunteerList = props.volunteerList;
        this.state.volunteerList = volunteerList;
        this.state.emptyVolunteer = props.emptyVolunteer;
        const l = this.filterVolunteerList(volunteerList, this.state.filterByPosition, false);
        this.state.filteredVolunteerList = l
        this.state.searchResults = l;
    }

    insertSearch = (e) => {
        console.log("called")
        // Get Value
        e = e.target.value;
        this.state.searchValue = e;

        // Validate Value
        if (!contains(e)) { this.setState({ searchResults: this.state.filteredVolunteerList }); return; }
        e = e.toLowerCase();

        // Search Value
        let a = [];
        for (let x of this.state.filteredVolunteerList) {
            if (x.name.toLowerCase().indexOf(e) >= 0) a.push(x);
        }

        // Search Found
        if (a.length > 0) this.setState({ searchResults: a });
        else this.setState({ searchResults: "" });
    };

    displayQualsList = (quals) => {
        let result = [];
        for (let i = 0; i < quals.length - 1; i++) {
            result.push(<div>- {quals[i]}</div>)
        }
        result.push(<div>- {quals[quals.length - 1]} <img src={require("../../assets/collapse.png")} /></div>)
        return result;
    }

    showHideQualifications = () => {
        const qualificationsVisible = !this.state.qualificationsVisible;
        this.setState({ qualificationsVisible });
    }

    saveChange = () => {
        if (this.state.selectedVolunteer.id != null) {
            const map = this.props.assignedVolunteers;
            const vol = this.state.selectedVolunteer;
            if (vol.id === this.props.volunteer.volunteer_id) {
                alert("You can't change a volunteer to themselves")
            } else if (map.has(vol.id)) {
                alert(vol.name + " is already assigned to asset " + map.get(vol.id).asset_id + " position " + map.get(vol.id).position)
            } else {
                this.props.onSave(this.state.selectedVolunteer)
            }
        } else {
            this.props.onHide();
        }

    }

    toggleFilterByPosition = () => {
        const filterByPosition = !this.state.filterByPosition;
        const l = this.filterVolunteerList(this.state.volunteerList, filterByPosition, false);
        const searchValue = this.state.searchValue;
        if (searchValue == "") {
            this.setState({ filterByPosition, filteredVolunteerList: l, searchResults: l })
        } else {
            var input = document.getElementById('searchBar');
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
            nativeInputValueSetter.call(input, "");
            var ev = new Event('input', { bubbles: true });
            input.dispatchEvent(ev);
            this.setState({ filterByPosition, filteredVolunteerList: l, searchResults: l });
        }
    }

    filterVolunteerList = (baseList, byPosition, byAvailability) => {
        const targetRole = this.props.volunteer.role;
        let l = [];
        if (byPosition) {
            let v;
            for (v of baseList) {
                v.possibleRoles.includes(targetRole) && l.push(v);
            }
        } else {
            l = [...baseList];
        }

        if (byAvailability) {
            //TODO
        }
        return l;
    }

    onHide = () => {
        //need to reset if you've selected a volunteer.
        const l = this.filterVolunteerList(this.state.volunteerList, true, false);
        this.setState({ qualificationsVisible: false, filterByPosition: true, searchValue: "", searchResults: l, filteredVolunteerList: l })
        this.props.onHide();
    }

    render() {
        return (
            <Modal
                {...this.props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        {this.props.vehicleType} - {this.props.volunteer.role}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {this.state.emptyVolunteer ?
                        <i>This position is currently unassigned</i> :
                        <div><b>{this.props.volunteer.volunteer_name}</b>
                            <div className="view" onClick={this.showHideQualifications} >
                                {this.state.qualificationsVisible ?
                                    this.displayQualsList(this.props.volunteer.qualifications)
                                    : <div>View qualifications <img src={require("../../assets/expand.png")} /></div>}
                            </div></div>
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
                            onClick={this.toggleFilterByPosition}
                        /> Only show {this.props.volunteer.role}s


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
                                        {this.state.searchResults.map((t) => (
                                            <tr className="view" onClick={() => { this.setState({ selectedVolunteer: t }); }}>
                                                <td>{this.props.assignedVolunteers.has(t.id) ? <div title="Already assigned">{t.name}{" "}<img src={require("../../assets/assigned.png")} /></div> : <div>{t.name}</div>}</td>
                                                <td>
                                                    {t.qualifications.map((q) => <div>- {q}</div>)}
                                                </td>
                                                <td>{t.contact_info[0].detail}</td>
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
                    {contains(this.state.selectedVolunteer) &&
                        <div className="con-vol">
                            <p>
                                {this.props.volunteer.volunteer_name} will change to:
              </p>
                            <Table striped bordered hover size="sm">
                                <tbody>
                                    <tr>
                                        <td>{this.state.selectedVolunteer.name}</td>
                                        <td>
                                            {this.state.selectedVolunteer.qualifications.map((q) => <div>- {q}</div>)}
                                        </td>
                                        <td>{this.state.selectedVolunteer.contact_info[0].detail}</td>
                                    </tr>
                                </tbody>
                            </Table>
                        </div>
                    }
                </Modal.Body>
                <Modal.Footer>
                    <Button className="danger" onClick={this.saveChange}>
                        Save Changes
          </Button>
                    {this.state.emptyVolunteer ? <div></div> :
                        <Button className="danger" onClick={this.props.removeVolunteer}>
                            Remove Volunteer
          </Button>}
                    <Button className="danger" onClick={this.onHide}>
                        Cancel
          </Button>
                </Modal.Footer>
            </Modal>
        );
    }
}

export default EditModal;