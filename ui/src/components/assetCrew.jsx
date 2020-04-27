import React, { Component } from "react";
import { Table } from "react-bootstrap";
import { Button } from "react-bootstrap";

class AssetCrew extends Component {
  //state = {  }

  render() {
    const { recommendationInfo } = this.props;

    return (
      <Table className="mt-4" striped bordered hover size="sm">
        <thead>
          <tr>
            <th width="20%">{recommendationInfo.asset_class}</th>
            <th colSpan="4">[time slot]</th>
          </tr>
        </thead>
        <tbody>
          {recommendationInfo.volunteers.map((v) => (
            <tr key={v.volunteer_id}>
              <td>{v.role}</td>
              <td>{v.volunteer_name}</td>
              <td>[experience]</td>
              <td>{v.contact_info}</td>
              <td>
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
