import React, { Component } from "react";
import "./editScreenModal.scss";
import { contains } from "../../main.js";
import { Modal, Button, Table } from "react-bootstrap";

class EditScreenModal extends Component {
  state = {
    dummyNewVol: {
      volunteer_id: 762,
      position_id: 0,
      volunteer_name: "Changed Volunteer",
      role: "??",
      qualifications: [
        "some quals",
        "other quals",
      ],
      contact_info: [{ detail: "09172342413" }],
    },
    searchDummyData: [
      {name:"aman", experiance:"[Experiace]", phNo:"0000-000-000"},
      {name:"cyrus", experiance:"[Experiace]", phNo:"0000-000-000"},
      {name:"caleb", experiance:"[Experiace]", phNo:"0000-000-000"},
      {name:"stavros", experiance:"[Experiace]", phNo:"0000-000-000"},
      {name:"tom", experiance:"[Experiace]", phNo:"0000-000-000"}
    ],
    searchResults: [],
    selectedVolunteer: null
  };

  insertSearch = (e) => {
    console.clear();
    // Get Value
    e = e.target.value;
    
    // Validate Value
    if (!contains(e)) { this.setState({ searchResults: [] }); return; }
    e = e.toLowerCase();

    // Search Value
    let a = [];
    for (let x of this.state.searchDummyData) {
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
            <input type="text" placeholder="Search Volunteer via Name" onChange={this.insertSearch}/>
            <hr/>
            <div className="con-vols">
              {(this.state.searchResults === "") &&
                <p>Nothing found</p>
              }
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
                        <th>{t.experiance}</th>
                        <th>{t.phNo}</th>
                      </tr>
                    ))}
                  </tbody>
                </Table>
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
                  <th>{this.state.selectedVolunteer.experiance}</th>
                  <th>{this.state.selectedVolunteer.phNo}</th>
                </tr>
              </Table>
            </div>
          }
        </Modal.Body>
        <Modal.Footer>
          <Button className="danger" onClick={() => this.props.onSave(this.state.dummyNewVol)}>
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
