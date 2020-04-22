import React, { Component } from "react";
import { Table } from "react-bootstrap";
import { Button } from "react-bootstrap";

class RecommendationPage extends Component {
  state = {
    volunteers: [
      { ID: 1, Pos: "Driver", Name: "Caleb Addison" },
      { ID: 2, Pos: "Crew Leader", Name: "Stavros Dimos" },
      { ID: 3, Pos: "Firefighter", Name: "Tom Willis" },
      { ID: 4, Pos: "Firefighter", Name: "Amandeep Singh" },
      { ID: 5, Pos: "Firefighter", Name: "Cyrus Safdar" },
    ],
  };

  render() {
    return (
      //example format of a 'vehicle recommendation' component or something of the like
      <React.Fragment>
        <h4 className="mt-2">New Asset Request</h4>

        <Table className="mt-4" striped bordered hover size="sm">
          <thead>
            <tr>
              <th width="20%">Heavy Tanker 1</th>
              <th colSpan="4">[time slot]</th>
            </tr>
          </thead>
          <tbody>
            {this.state.volunteers.map((a) => (
              <tr key={a.assetID}>
                <td>{a.Pos}</td>
                <td>{a.Name}</td>
                <td>[experience]</td>
                <td>[phone number]</td>
                <td>
                  <Button className="btn-warning">Edit</Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </React.Fragment>
    );
  }
}

export default RecommendationPage;
