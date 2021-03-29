import React from 'react';
import axios, { AxiosResponse, AxiosError } from 'axios';
import { backendPath } from '../config';

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
  volunteers: volunteer[];
  selectedVolunteer?: volunteer;
}

export default class VolunteersContainer extends React.Component<any, State> {
  state: State = {
    volunteers: [],
    selectedVolunteer: undefined,
  };
  select_volunteer: React.RefObject<HTMLSelectElement>;

  constructor(props: any) {
    super(props);
    this.select_volunteer = React.createRef();
  }

  componentDidMount(): void {
    axios
      .get(backendPath + 'volunteer/all', {
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((res: AxiosResponse): void => {
        let l = res.data['results'];

        //sort the list alphabetically by name
        l.sort(
          (
            a: { firstName: number; lastName: number },
            b: { firstName: number; lastName: number }
          ) =>
            a.firstName > b.firstName
              ? 1
              : a.firstName === b.firstName
              ? a.lastName > b.lastName
                ? 1
                : -1
              : -1
        );
        console.log(l);
        this.setState({ volunteers: l });
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

  test = (): void => {
    let id: string = this.select_volunteer.current
      ? this.select_volunteer.current.value
      : '';

    //find the volunteer we selected from the list
    let v: volunteer | undefined = undefined;
    for (let i = 0; i < this.state.volunteers.length; i++) {
      if (this.state.volunteers[i].ID === id) {
        v = this.state.volunteers[i];
        i = this.state.volunteers.length;
      }
    }
    this.setState({ selectedVolunteer: v }, () => {
      this.loadVolunteer();
    });
  };

  loadVolunteer = (): void => {
    if (this.state.selectedVolunteer === undefined) {
      console.log('no volunteer selected');
    } else {
      window.open(
        window.location.origin +
          `/volunteer/${this.state.selectedVolunteer.ID}`,
        '_self',
        '',
        false
      );
    }
  };

  render() {
    return (
      <div className="padding">
        <h4>Volunteers</h4>
        <hr />
        <p>Select a volunteer to view their personalised volunteer page.</p>
        <select ref={this.select_volunteer}>
          <option value="" hidden selected>
            Select a volunteer
          </option>
          {this.state.volunteers.map((v: volunteer) => (
            <option value={v.ID}>
              {v.firstName} {v.lastName}
            </option>
          ))}
        </select>
        <button className="type-1 margin" onClick={this.test}>
          View Volunteer
        </button>
      </div>
    );
  }
}
