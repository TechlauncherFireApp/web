import axios from 'axios';
import React from 'react';
import { Table } from 'react-bootstrap';

import { backendPath } from '../../config';
import Shift from './shift';

export default class Volunteer extends React.Component {
  state = {
    loading: true,
    thisVolunteer: undefined,
    myShifts: undefined,
  };

  componentDidMount() {
    axios
      .request({
        url: backendPath + 'volunteer',
        method: 'GET',
        params: { volunteerID: this.props.match.params.id },
        timeout: 15000,
        // withCredentials: true,
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((res) => {
        const tmp = res.data;
        tmp.availabilities = [];
        this.setState({ thisVolunteer: tmp, loading: false });
      })
      .catch((err) => {
        if (err.response !== undefined && err.response.status === 401) {
          this.props.history.push('/login');
        } else {
          alert(err.message);
        }
      });

    axios
      .request({
        url: backendPath + 'volunteer/shifts',
        method: 'GET',
        params: { volunteerID: this.props.match.params.id },
        timeout: 15000,
        // withCredentials: true,
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((res) => {
        const tmp = res.data['results'];
        if (tmp !== null) {
          for (const t of tmp) {
            t.vehicleFrom = new Date(Date.parse(t.vehicleFrom));
            t.vehicleTo = new Date(Date.parse(t.vehicleTo));
          }
          this.setState({ myShifts: tmp });
        }
      })
      .catch((err) => {
        if (err.response !== undefined && err.response.status === 401) {
          this.props.history.push('/login');
        } else {
          alert(err.message);
        }
      });
  }

  manageAvailability = () => {
    window.open(
      window.location.origin +
        `/volunteer/${this.props.match.params.id}/availability`,
      '_self',
      '',
      false
    );
  };

  updateStatus = (newStatus, shiftData) => {
    //console.log(newStatus, shiftData);
    const info = {
      idVolunteer: this.state.thisVolunteer?.ID,
      idVehicle: shiftData.vehicleID,
      status: newStatus,
    };

    axios
      .request({
        url: backendPath + 'volunteer/status',
        method: 'PATCH',
        timeout: 15000,
        params: info,
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .catch((err) => {
        if (err.response !== undefined && err.response.status === 401) {
          this.props.history.push('/login');
        } else {
          alert(err.message);
        }
      });
  };

  render() {
    return this.state.loading ? (
      <div className="padding">
        <h4>Volunteers</h4>
        <hr />
        Loading...
      </div>
    ) : (
      <div className="padding">
        <div>
          <h4>
            {this.state.thisVolunteer?.firstName}{' '}
            {this.state.thisVolunteer?.lastName}
          </h4>
          <hr />
          <p>
            This is the volunteer page for {this.state.thisVolunteer?.firstName}{' '}
            {this.state.thisVolunteer?.lastName}.
          </p>
          <p>
            Here they will be able to see their assigned shifts, update their
            availability, and update their preferred hours.
          </p>
          <button className="type-1" onClick={this.manageAvailability}>
            Manage Availability
          </button>
        </div>
        <div className="mt-3">
          <h5>My Shifts</h5>
          <Table className="mt-2" striped bordered hover size="sm">
            <thead>
              <tr>
                <th>Date and Time</th>
                <th>Role</th>
                <th>Asset</th>
                <th>Request Title</th>
                <th>My Status</th>
              </tr>
            </thead>
            <tbody>
              {this.state.myShifts === undefined ? (
                <tr>
                  <td colSpan={5}>None</td>
                </tr>
              ) : (
                this.state.myShifts.map((s) => (
                  <Shift
                    key={s.vehicleID}
                    shift={s}
                    updateStatus={(a, b) => this.updateStatus(a, b)}
                  />
                ))
              )}
            </tbody>
          </Table>
        </div>
      </div>
    );
  }
}
