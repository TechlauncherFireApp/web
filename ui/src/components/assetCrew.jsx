import React, { Component } from "react";
import { Table } from "react-bootstrap";
import { Button } from "react-bootstrap";

class AssetCrew extends Component {
  //state = {  }

  render() {
    return (
      <Table className="mt-4" striped bordered hover size="sm">
        <thead>
          <tr>
            <th width="20%">Heavy Tanker 1</th>
            <th colSpan="4">[time slot]</th>
          </tr>
        </thead>
        <tbody>
          {this.props.volunteers.map((a) => (
            <tr key={a.assetID}>
              <td>{a.Pos}</td>
              <td>{a.Name}</td>
              <td>[experience]</td>
              <td>[phone number]</td>
              <td style={{ "text-align": "center" }}>
                <Button className="btn-warning">Edit</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    );
  }
}

export default AssetCrew;
