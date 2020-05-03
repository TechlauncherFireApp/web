import React, { Component } from "react";
import { Modal, Button } from "react-bootstrap";

class QualificationsModal extends Component {
  state = {};

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
            {this.props.volunteer.volunteer_name}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>
            {/* {this.props.volunteer.qualifications.map((q) => (
              <p key={q}>- {q}</p>
            ))} */}
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button className="danger" onClick={this.props.onHide}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    );
  }
}

export default QualificationsModal;
