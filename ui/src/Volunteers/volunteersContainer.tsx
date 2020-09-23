import React, { Component } from "react";
import axios, { AxiosResponse, AxiosError } from "axios";

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
    selectedVolunteer: undefined
  };
  select_volunteer: React.RefObject<HTMLSelectElement>;


  constructor(props: any) {
    super(props);
    this.select_volunteer = React.createRef();
  }

  componentDidMount(): void {
    let l: volunteer[] = [];
    axios.request({
      url: "volunteer/all",
      baseURL: "http://localhost:5000/",
      method: "GET",
      timeout: 15000,
      // withCredentials: true,
      headers: { "X-Requested-With": "XMLHttpRequest" }
    }).then((res: AxiosResponse): void => {
      let tmp = res.data["results"]
      for (const v of tmp) {
        let convertedAvailabilities: any = [];
        for (const a of v.availabilities) {
          const start = new Date(Date.parse(a[0]));
          const end = new Date(Date.parse(a[1]));
          convertedAvailabilities.push({ startTime: start, endTime: end });
        }
        v.availabilities = convertedAvailabilities;
      }
      l = tmp

      //sort the list alphabetically by name
      l.sort((a, b) => ((a.firstName > b.firstName) ? 1 : ((a.firstName === b.firstName) ? ((a.lastName > b.lastName) ? 1 : -1) : -1)));
      console.log(l)
      this.setState({ volunteers: l })
    }).catch((err: AxiosError): void => {
      alert(err.message);
    });
  }

  test = (): void => {

    let id: string = this.select_volunteer.current ? this.select_volunteer.current.value : "";

    //find the volunteer we selected from the list
    let v: (volunteer | undefined) = undefined;
    for (let i = 0; i < this.state.volunteers.length; i++) {
      if (this.state.volunteers[i].ID === id) {
        v = this.state.volunteers[i];
        i = this.state.volunteers.length;
      }
    }
    this.setState({ selectedVolunteer: v }, () => { this.loadVolunteer() });
  }

  loadVolunteer = (): void => {
    if (this.state.selectedVolunteer === undefined) {
      console.log("no volunteer selected");
    } else {
      window.open(window.location.origin + `/volunteer/${this.state.selectedVolunteer.ID}`, "_self", "", false)
    }
  }

  render() {
    return (
      <div className="padding">
        <h4>Volunteers</h4>
        <hr />
        <p>Select a volunteer to view their personalised volunteer page.</p>
        <select ref={this.select_volunteer}>
          <option value="" hidden selected>Select a volunteer</option>
          {this.state.volunteers.map((v: volunteer) =>
            <option value={v.ID}>{v.firstName} {v.lastName}</option>
          )}
        </select>
        <button className="type-1 margin" onClick={this.test}>View Volunteer</button>
      </div>
    );
  }
}