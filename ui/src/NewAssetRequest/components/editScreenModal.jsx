import React, { Component } from "react";
import "./editScreenModal.scss";
import { contains } from "../../main.js";
import { Modal, Button, Table } from "react-bootstrap";

class EditScreenModal extends Component {
  state = {
    volunteerList: [],
    searchResults: [],
    selectedVolunteer: {
      id: null,
      name: "",
      role: null,
      qualifications: [""],
      contact_info: [{ detail: "" }],
    },
  };

  constructor(props) {
    super(props);
    const volunteerList = props.volunteerList;
    this.state.volunteerList = volunteerList;
  }

  insertSearch = (e) => {
    console.clear();
    // Get Value
    e = e.target.value;

    // Validate Value
    if (!contains(e)) { this.setState({ searchResults: [] }); return; }
    e = e.toLowerCase();

    // Search Value
    let a = [];
    for (let x of this.state.volunteerList) {
      if (x.name.toLowerCase().indexOf(e) >= 0) a.push(x);
    }

    // Search Found
    if (a.length > 0) this.setState({ searchResults: a });
    else this.setState({ searchResults: "" });
  };

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
          <div>
            {this.props.volunteer.volunteer_name}
          </div>
          <form>
            <input type="text" placeholder="Search Volunteer via Name" onChange={this.insertSearch} />
            <hr />
            <div className="con-vols">
              {((typeof this.state.searchResults === "object") && this.state.searchResults.length > 0) &&
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Experiance</th>
                      <th>Phone No</th>
                    </tr>
                  </thead>
                  <tbody>
                    {this.state.searchResults.map((t) => (
                      <tr onClick={() => { this.setState({ selectedVolunteer: t }); }}>
                        <th>{t.name}</th>
                        <th>view</th>
                        <th>{t.contact_info[0].detail}</th>
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
                <tr>
                  <th>{this.state.selectedVolunteer.name}</th>
                  <th>view</th>
                  <th>{this.state.selectedVolunteer.contact_info[0].detail}</th>
                </tr>
              </Table>
            </div>
          }
        </Modal.Body>
        <Modal.Footer>
          <Button className="danger" onClick={() => this.props.onSave(this.state.selectedVolunteer)}>
            Save
          </Button>
          <Button className="danger" onClick={this.props.onHide}>
            Cancel
          </Button>
        </Modal.Footer>
      </Modal>
    );
  }
}

export default EditScreenModal;
