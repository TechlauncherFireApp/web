import React from 'react';
import { Table } from 'react-bootstrap';
import axios, { AxiosResponse, AxiosError } from 'axios';
import Shift from './shift';
import { backendPath } from '../../config';

interface volunteer {
  ID: string;
  firstName: string;
  lastName: string;
  email: string;
  mobileNo: string;
  prefHours: number;
  expYears: number;
  possibleRoles: string[];
  qualifications: string[];
  availabilities: Timeframe[];
}

interface Timeframe {
  startTime: Date;
  endTime: Date;
}

interface State {
  loading: boolean;
  thisVolunteer?: volunteer;
  myShifts: any;
}

export default class Volunteer extends React.Component<any, State> {
  state: State = {
    loading: true,
    thisVolunteer: undefined,
    myShifts: undefined,
  };

  componentDidMount(): void {
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
      .then((res: AxiosResponse): void => {
        let tmp = res.data;
        let convertedAvailabilities: any = [];
        /*for (const a of tmp.availabilities) {
                const start = new Date(Date.parse(a[0]));
                const end = new Date(Date.parse(a[1]));
                convertedAvailabilities.push({ startTime: start, endTime: end });
            }*/
        tmp.availabilities = convertedAvailabilities;
        this.setState({ thisVolunteer: tmp, loading: false });
      })
      .catch((err: AxiosError): void => {
        // @ts-ignore
        if (err.response.status === 401) {
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
      .then((res: AxiosResponse): void => {
        let tmp = res.data['results'];
        if (tmp !== null) {
          for (const t of tmp) {
            t.vehicleFrom = new Date(Date.parse(t.vehicleFrom));
            t.vehicleTo = new Date(Date.parse(t.vehicleTo));
          }
          this.setState({ myShifts: tmp });
        }
      })
      .catch((err: AxiosError): void => {
        // @ts-ignore
        if (err.response.status === 401) {
          this.props.history.push('/login');
        } else {
          alert(err.message);
        }
      });
  }

  manageAvailability = (): void => {
    window.open(
      window.location.origin +
        `/volunteer/${this.props.match.params.id}/availability`,
      '_self',
      '',
      false
    );
  };

  updateStatus = (newStatus: string, shiftData: any): void => {
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
      .catch((err: AxiosError): void => {
        // @ts-ignore
        if (err.response.status === 401) {
          this.props.history.push('/login');
        } else {
          alert(err.message);
        }
      });
  };

  //state = {};
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
                this.state.myShifts.map((s: any) => (
                  <Shift
                    key={s.vehicleID}
                    shift={s}
                    updateStatus={(a: string, b: any) =>
                      this.updateStatus(a, b)
                    }
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
