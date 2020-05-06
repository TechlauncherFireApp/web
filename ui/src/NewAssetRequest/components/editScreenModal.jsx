import React, { Component } from "react";
import { Modal, Button } from "react-bootstrap";

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
    }
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
