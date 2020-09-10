import React from "react";
import "./Availability.scss";
import axios, { AxiosResponse, AxiosError } from "axios";
import { contains } from "../../functions";

type Day = "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday" | "Saturday" | "Sunday";
type Schedule = { [key in Day]: number[][] };

interface State {
  currentSchedule?: Schedule;
  allow_getCurrentSchedule: boolean;
  allow_patchCurrentSchedule: boolean;
}

export default class Availability extends React.Component<any, State> {
  // Initial Fields and Methods 
  state: State = {
    allow_getCurrentSchedule: true,
    allow_patchCurrentSchedule: true
  };

  componentDidMount(): void {
    this.getCurrentSchedule();
  }

  // Component Methods
  inData(k: Day, n: number): boolean {
    if (this.state.currentSchedule && contains(this.state.currentSchedule, this.state.currentSchedule[k]))
      for (let l of this.state.currentSchedule[k]) if (l.includes(n) || ((n > l[0]) && (n < l[1]))) return true;
    return false;
  }

  editData(k: Day, n: number): void {
    if (this.state.currentSchedule && contains(this.state.currentSchedule)) {
      // console.clear();
      const d: Schedule = this.state.currentSchedule;
      if (this.inData(k, n)) {
        // Remove
        for (let i: number = 0; i < d[k].length; i++) {
          if (d[k][i].includes(n)) {
            if (d[k][i][0] === d[k][i][1]) d[k].splice(i, 1);
            else if (d[k][i][0] === n) d[k][i][0] += 0.5;
            else if (d[k][i][1] === n) d[k][i][1] -= 0.5;
            break;
          } else if ((n > d[k][i][0]) && (n < d[k][i][1])) {
            d[k].push([n + 0.5, d[k][i][1]]);
            d[k][i][1] = n - 0.5;
            break;
          }
        }
      } else {
        // Insert
        let b: boolean = true;
        for (let i: number = 0; i < d[k].length; i++) {
          if ((d[k][i][0] - 0.5) === n) { d[k][i][0] = n; b = false; }
          else if ((d[k][i][1] + 0.5) === n) { d[k][i][1] = n; b = false; }

          if (contains(d[k][i + 1]) && ((d[k][i][1] + 0.5) === d[k][i + 1][0])) {
            d[k][i][1] = d[k][i + 1][1];
            d[k].splice(i + 1, 1);
            b = false;
          }
          if (!b) break;
        }
        if (b) d[k].push([n, n]);
      }
      d[k].sort(function (a, b: number[]): number { return ((a[0] === b[0]) ? 0 : ((a[0] < b[0]) ? -1 : 1)); });
      this.setState({ currentSchedule: d });
      // console.log(JSON.stringify(this.data[k]));
    }
  }

  // Backend Requests
  getCurrentSchedule(): void {
    if (!this.state.allow_getCurrentSchedule) return;
    this.setState({ allow_getCurrentSchedule: false });

    axios.request({
      url: "/volunteer/availability",
      method: "GET",
      params: { "volunteerID": "1XrptA7sjhrys1D" },
      timeout: 15000
    }).then((res: AxiosResponse): void => {
      console.log(res.data);
      if ((typeof res.data === "object") && (res.data["success"])) {
        this.setState({ currentSchedule: res.data["availability"][0] as Schedule });
      } else alert(res.data);
      this.setState({ allow_getCurrentSchedule: true });
    }).catch((err: AxiosError): void => {
      alert(err.message);
      this.setState({ allow_getCurrentSchedule: true });
    });
  }

  patchCurrentSchedule(): void {
    if (!this.state.allow_patchCurrentSchedule && !contains(this.state.currentSchedule)) return;
    this.setState({ allow_patchCurrentSchedule: false });
    
    console.log({ "volunteerID": "1XrptA7sjhrys1D", "availability": this.state.currentSchedule });

    axios.request({
      url: "/volunteer/availability",
      method: "PATCH",
      params: { "volunteerID": "1XrptA7sjhrys1D", "availability": this.state.currentSchedule },
      timeout: 15000
    }).then((res: AxiosResponse): void => {
      console.log(res.data);
      // alert(res.data);
      this.setState({ allow_patchCurrentSchedule: true });
    }).catch((err: AxiosError): void => {
      alert(err.message);
      this.setState({ allow_patchCurrentSchedule: true });
    });
  }

  // Render Component
  render(): JSX.Element {
    let l: number[] = [];
    for (let i = 0; i <= 23.5; i += 0.5) l.push(i);

    return (
      <availability is="x3d">
        {contains(this.state.currentSchedule) ? <>
          <table>
            <tr>
              <th></th>
              {this.state.currentSchedule && Object.keys(this.state.currentSchedule).map((k: string) => <th>{k}</th>)}
            </tr>
            {l.map((i: number) =>
              <tr>
                <th>{((i % 1) === 0) ? `${i < 10 ? "0" : ""}${i}:00` : `${Math.floor(i) < 10 ? "0" : ""}${Math.floor(i)}:30`}</th>
                {this.state.currentSchedule && Object.keys(this.state.currentSchedule).map((k: string) =>
                  <th data-selected={this.inData((k as Day), i)} onClick={(): void => this.editData((k as Day), i)}></th>
                )}
              </tr>
            )}
          </table>
          <button className="type-1" onClick={(): void => this.patchCurrentSchedule()}>
            {this.state.allow_patchCurrentSchedule ? "Update" : "Loading"}
          </button>
        </> : <>
            <h1>{this.state.allow_getCurrentSchedule ? "Nothing Found" : "Loading"}</h1>
          </>}
      </availability>
    );
  }
}