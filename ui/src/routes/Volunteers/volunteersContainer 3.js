import axios from 'axios';
import React from 'react';

import { backendPath } from '../../config';

export default class VolunteersContainer extends React.Component {
  state = {
    volunteers: [],
    selectedVolunteer: undefined,
  };
  select_volunteer;

  constructor(props) {
    super(props);
    this.select_volunteer = React.createRef();
  }

  componentDidMount() {
    axios
      .get(backendPath + 'volunteer/all', {
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((res) => {
        const l = res.data['results'];

        //sort the list alphabetically by name
        l.sort((a, b) =>
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
      .catch((err) => {
        if (err.response !== undefined && err.response.status === 401) {
          this.props.history.push('/login');
        } else {
          alert(err.message);
        }
      });
  }

  test = () => {
    const id = this.select_volunteer.current
      ? this.select_volunteer.current.value
      : '';

    //find the volunteer we selected from the list
    let v = undefined;
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

  loadVolunteer = () => {
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
          {this.state.volunteers.map((v) => (
            <option key={v.ID} value={v.ID}>
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
