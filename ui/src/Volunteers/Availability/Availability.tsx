import React from "react";
import "./Availability.scss";
import axios, { AxiosResponse, AxiosError } from "axios";
import { contains, att } from "../../functions";
import { addBusinessDays } from "date-fns";

type Day = "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday" | "Saturday" | "Sunday";
type Schedule = { [key in Day]: number[][] };

interface State {
  // Pref Hours
  prefHours?: number;
  allow_getPrefHours: boolean;
  allow_patchPrefHours: boolean;
  // Availability
  currentSchedule?: Schedule;
  allow_getCurrentSchedule: boolean;
  allow_patchCurrentSchedule: boolean;
  
  // Click Function
  key?: Day;
}

export default class Availability extends React.Component<any, State> {
  // Initial Fields and Methods 
  state: State = {
    allow_getPrefHours: true,
    allow_patchPrefHours: true,
    allow_getCurrentSchedule: true,
    allow_patchCurrentSchedule: true
  };

  componentDidMount(): void {
    this.getPrefHours();
    this.getCurrentSchedule();
  }

  // Component Methods
  inData(k: Day, n: number): boolean {
    if (this.state.currentSchedule && contains(this.state.currentSchedule, this.state.currentSchedule[k]))
      for (let l of this.state.currentSchedule[k]) if ((n === l[0]) || ((n > l[0]) && (n < l[1]))) return true;
    return false;
  }

  editData(k: Day, n: number): void {
    if (this.state.currentSchedule && contains(this.state.currentSchedule)) {
      // console.clear();
      if (this.inData(k, n)) this.deleteData(k, n);
      else this.insertData(k, n);
      console.log(JSON.stringify(this.state.currentSchedule[k]), "\n");
    }
  }

  insertData(k: Day, n: number): void {
    if (this.state.currentSchedule && contains(this.state.currentSchedule) && !this.inData(k, n)) {
      const d: Schedule = this.state.currentSchedule;
      let b: boolean = true;
      
      for (let i: number = 0; i < d[k].length; i++) {
        if ((d[k][i][0] - 0.5) === n) { d[k][i][0] = n; b = false; }
        else if ((d[k][i][1] + 0.5) === (n + 0.5)) { d[k][i][1] = n + 0.5; b = false; }

        if (contains(d[k][i + 1]) && (d[k][i][1] === d[k][i + 1][0])) {
          d[k][i][1] = d[k][i + 1][1];
          d[k].splice(i + 1, 1);
          b = false;
        }
        if (!b) break;
      }
      if (b) d[k].push([n, n + 0.5]);
      d[k].sort(function (a, b: number[]): number { return ((a[0] === b[0]) ? 0 : ((a[0] < b[0]) ? -1 : 1)); });
      this.setState({ currentSchedule: d });
    }
  }

  deleteData(k: Day, n: number): void {
    if (this.state.currentSchedule && contains(this.state.currentSchedule) && this.inData(k, n)) {
      const d: Schedule = this.state.currentSchedule;
      
      for (let i: number = 0; i < d[k].length; i++) {
        if ((d[k][i][0] === n) || (d[k][i][1] === (n + 0.5))) {
          if (d[k][i][0] === (d[k][i][1] - 0.5)) d[k].splice(i, 1);
          else if (d[k][i][0] === n) d[k][i][0] += 0.5;
          else if (d[k][i][1] === (n + 0.5)) d[k][i][1] -= 0.5;
          break;
        } else if ((n > d[k][i][0]) && (n < d[k][i][1])) {
          d[k].push([n + 0.5, d[k][i][1]]);
          d[k][i][1] = n;
          break;
        }
      }
      d[k].sort(function (a, b: number[]): number { return ((a[0] === b[0]) ? 0 : ((a[0] < b[0]) ? -1 : 1)); });
      this.setState({ currentSchedule: d });
    }
  }

  // Backend Requests
  getPrefHours(): void {
    if (!this.state.allow_getPrefHours) return;
    this.setState({ allow_getPrefHours: false });

    axios.request({
      url: "/volunteer/prefhours",
      method: "GET",
      params: { "volunteerID": this.props.match.params.id },
      headers: { "Authorization": "Bearer "+localStorage.getItem('access_token') }
    }).then((res: AxiosResponse): void => {
      // console.log(res.data);
      if ((typeof res.data === "object") && (res.data["success"])) {
        this.setState({ prefHours: res.data["prefHours"] as number });
      } else alert("Request Failed");
      this.setState({ allow_getPrefHours: true });
    }).catch((err: AxiosError): void => {
      alert(err.message);
      this.setState({ allow_getPrefHours: true });
    });
  }

  getCurrentSchedule(): void {
    if (!this.state.allow_getCurrentSchedule) return;
    this.setState({ allow_getCurrentSchedule: false });

    axios.request({
      url: "/volunteer/availability",
      method: "GET",
      params: { "volunteerID": this.props.match.params.id },
      headers: { "Authorization": "Bearer "+localStorage.getItem('access_token') }
    }).then((res: AxiosResponse): void => {
      // console.log(res.data);
      if ((typeof res.data === "object") && (res.data["success"])) {
        let n: Schedule = res.data["availability"] as Schedule;
        // console.log(n instanceof Schedule);
        this.setState({ currentSchedule: n });
      } else alert("Request Failed");
      this.setState({ allow_getCurrentSchedule: true });
    }).catch((err: AxiosError): void => {
      alert(err.message);
      this.setState({ allow_getCurrentSchedule: true });
    });
  }

  patchPrefHours(): void {
    if (!this.state.allow_patchPrefHours && !contains(this.state.allow_patchPrefHours)) return;
    this.setState({ allow_patchPrefHours: false });

    axios.request({
      url: "/volunteer/prefhours",
      method: "PATCH",
      params: { "volunteerID": this.props.match.params.id, "prefHours": Number(this.state.prefHours) },
      headers: { "Authorization": "Bearer "+localStorage.getItem('access_token') }
    }).then((res: AxiosResponse): void => {
      // console.log(res.data);
      alert(res.data["success"] ? "Updated - prefHours" : "Request Failed");
      this.setState({ allow_patchPrefHours: true });
    }).catch((err: AxiosError): void => {
      alert(err.message);
      this.setState({ allow_patchPrefHours: true });
    });
  }

  patchCurrentSchedule(): void {
    if (!this.state.allow_patchCurrentSchedule && !contains(this.state.currentSchedule)) return;
    this.setState({ allow_patchCurrentSchedule: false });

    axios.request({
      url: "/volunteer/availability",
      method: "PATCH",
      params: { "volunteerID": this.props.match.params.id },
      data: { "availability": this.state.currentSchedule },
      headers: { "Authorization": "Bearer "+localStorage.getItem('access_token') }
    }).then((res: AxiosResponse): void => {
      // console.log(res.data);
      alert(res.data["success"] ? "Updated - Availability" : "Request Failed");
      this.setState({ allow_patchCurrentSchedule: true });
    }).catch((err: AxiosError): void => {
      alert(err.message);
      this.setState({ allow_patchCurrentSchedule: true });
    });
  }

  exit(): void {
    window.open(`${window.location.origin}/volunteer/${this.props.match.params.id}`, "_self", "", false);
  }

  // Render Component
  render(): JSX.Element {
    let l: number[] = [];
    for (let i = 0; i <= 23.5; i += 0.5) l.push(i);

    return (
      <availability is="x3d">
        <input type="number" placeholder="Select PrefHours" title="Set PrefHours" value={this.state.prefHours}
          onChange={(e: any): void => this.setState({ prefHours: Number(e.target.value) })} />
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
                    <th {...att("selectd",this.inData((k as Day),i))} onClick={(): void => this.editData((k as Day), i)}></th>
                  )}
                </tr>
              )}
            </table>
            <button className="type-1" onClick={(): void => { this.patchPrefHours(); this.patchCurrentSchedule(); }}>
              {this.state.allow_patchCurrentSchedule ? "Update" : "Loading"}
            </button>
          </> : <>
            <h1 onClick={(): void => this.getCurrentSchedule()}>
              {this.state.allow_getCurrentSchedule ? "Nothing Found" : "Loading"}
            </h1>
          </>}
        <button className="type-1" onClick={(): void => this.exit()}>Return</button>
      </availability>
    );
  }
}