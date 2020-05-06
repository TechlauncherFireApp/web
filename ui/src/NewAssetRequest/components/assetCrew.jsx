import React, { Component } from "react";
import { Table } from "react-bootstrap";
import Volunteer from "./volunteer";

class AssetCrew extends Component {
  state = {
    showQualifications: false,
  };

  toggleQualificationsVisibility = () => {
    const showQualifications = !this.state.showQualifications;
    this.setState({ showQualifications });
  };

  parseDateTime = (date1, date2) => {
    let str = "";
    if (
      date1.getMonth() === date2.getMonth() &&
      date1.getDate() === date2.getDate() &&
      date1.getFullYear() === date2.getFullYear()
    ) {
      //if the request starts and ends on the same day
      str =
        str +
        (date1.getHours() === 0
          ? "12"
          : date1.getHours() > 12
            ? date1.getHours() - 12
            : date1.getHours());
      str =
        str +
        ":" +
        (date1.getMinutes() === 30 ? "30 " : "00 ") +
        (date1.getHours() > 11 ? "pm - " : "am - ");
      str =
        str +
        (date2.getHours() === 0
          ? "12"
          : date2.getHours() > 12
            ? date2.getHours() - 12
            : date2.getHours());
      str =
        str +
        ":" +
        (date2.getMinutes() === 30 ? "30 " : "00 ") +
        (date2.getHours() > 11 ? "pm, " : "am, ") +
        date2.toLocaleDateString();
    } else {
      //if the request spans multiple days
      str =
        str +
        (date1.getHours() === 0
          ? "12"
          : date1.getHours() > 12
            ? date1.getHours() - 12
            : date1.getHours());
      str =
        str +
        ":" +
        (date1.getMinutes() === 30 ? "30 " : "00 ") +
        (date1.getHours() > 11 ? "pm " : "am ") +
        date1.toLocaleDateString() +
        " - ";
      str =
        str +
        (date2.getHours() === 0
          ? "12"
          : date2.getHours() > 12
            ? date2.getHours() - 12
            : date2.getHours());
      str =
        str +
        ":" +
        (date2.getMinutes() === 30 ? "30 " : "00 ") +
        (date2.getHours() > 11 ? "pm " : "am ") +
        date2.toLocaleDateString();
    }
    return str;
  };

  updateVolunteer = (newVolunteer) => {
    let volunteers = this.props.vehicle.volunteers;
    for (let i = 0; i < volunteers.length; i++) {
      if (volunteers[i].position_id === newVolunteer.position_id) volunteers[i] = newVolunteer;
    }
    let vehicle = this.props.vehicle;
    vehicle.volunteers = volunteers;
    this.props.updateVehicle(vehicle);
  }

  render() {
    const { vehicle } = this.props;

    return (
      <Table className="mt-4" striped bordered hover size="sm">
        <thead>
          <tr>
            <th width="20%">{vehicle.asset_class}</th>
            <td colSpan="6">
              <span>
                {this.parseDateTime(
                  vehicle.startDateTime,
                  vehicle.endDateTime
                )}
              </span>
            </td>
          </tr>
        </thead>
        <tbody>
          {vehicle.volunteers.map((v) => (
            <Volunteer key={v.volunteer_id} volunteerInfo={v} vehicleType={vehicle.asset_class} updateVolunteer={(details) => this.updateVolunteer(details)} />
          ))}
        </tbody>
      </Table>
    );
  }
}

export default AssetCrew;
