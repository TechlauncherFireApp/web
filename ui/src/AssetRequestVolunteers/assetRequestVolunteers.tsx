import React from "react";
import Asset from "./asset";
import { Button } from "react-bootstrap";
import axios, { AxiosResponse, AxiosError } from "axios";

interface Timeframe {
  startTime: Date;
  endTime: Date;
}

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

interface Position {
  positionID: number;
  ID: string;
  volunteer: volunteer;
  role: string[];
  status: string;
}

interface asset {
  shiftID: number;
  assetClass: string;
  startTime: Date;
  endTime: Date;
  volunteers: Position[];
}

interface State {
  loading: boolean;
  allow_getInitialData: boolean;
  volunteerList: volunteer[];
  assignedVolunteers: Map<string, { shiftID: number, positionID: number }>;
  assetRequest: asset[];
}

export default class AssetRequestVolunteers extends React.Component<any, State> {

  state: State = {
    loading: true,
    allow_getInitialData: true,
    volunteerList: [],
    assignedVolunteers: new Map(),
    assetRequest: [],
  };

  constructor(props: any) {
    super(props);
    if (this.state.volunteerList.length > 0) {
      this.identifyAssignedVolunteers(this.state.assetRequest);
    }
  }

  componentDidMount(): void {
    this.getInitialData();
  }

  mapVolunteersToRequest = (assets: any[], volunteerList: volunteer[]): asset[] => {
    // this is not the most effecient method but it's very simple. I believe it's O(n^2) but as we're working with small data this should be fine
    let output = [...assets];
    for (const asset of output) {
      for (const position of asset.volunteers) {
        //find the corresponding volunteer

        if (position.ID === "") {
          //empty position
          position.volunteer = undefined;
        } else {
          for (let j = 0; j < volunteerList.length; j++) {
            if (volunteerList[j].ID === position.ID) {
              position.volunteer = { ...volunteerList[j] };
              j = volunteerList.length;
            }
          }
        }
      }
    }
    return output;
  }


  getInitialData = (): void => {

    let volunteerList: volunteer[] = [];
    let recommendation: any = [];

    //get allVolunteers data from database
    axios.request({
      url: "volunteer/all",
      baseURL: "http://localhost:5000/",
      method: "GET",
      timeout: 15000,
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
      volunteerList = tmp
      volunteerList.sort((a, b) => ((a.firstName > b.firstName) ? 1 : ((a.firstName === b.firstName) ? ((a.lastName > b.lastName) ? 1 : -1) : -1)));

      if (recommendation.length !== 0) {
        let assetRequest = this.mapVolunteersToRequest(recommendation, volunteerList);
        const assignedVolunteers = this.identifyAssignedVolunteers(assetRequest);
        this.setState({ assetRequest, volunteerList, assignedVolunteers, loading: false })
      }
    }).catch((err: AxiosError): void => {
      alert(err.message);
    });

    //get the request volunteer data from the database
    axios.request({
      url: "shift/request?requestID=" + this.props.match.params.id,
      baseURL: "http://localhost:5000/",
      method: "GET",
      timeout: 15000,
      // withCredentials: true,
      headers: { "X-Requested-With": "XMLHttpRequest" }
    }).then((res: AxiosResponse): void => {
      let tmp = res.data["results"]
      console.log("tmp:", tmp)

      for (const r of tmp) {
        r.startTime = new Date(Date.parse(r.startTime));
        r.endTime = new Date(Date.parse(r.endTime));
      }
      recommendation = tmp;

      // Both volunteerList and recommendation need to be populated
      if (volunteerList.length !== 0) {
        let assetRequest = this.mapVolunteersToRequest(recommendation, volunteerList);
        const assignedVolunteers = this.identifyAssignedVolunteers(assetRequest);
        this.setState({ assetRequest, volunteerList, assignedVolunteers, loading: false })
      }
    }).catch((err: AxiosError): void => {
      alert(err.message);
    });
  }

  submitData = (): void => {
    const shifts = this.state.assetRequest;

    //TODO implement the patch request
    axios.request({
      url: "shift/request?requestID=" + this.props.match.params.id,
      baseURL: "http://localhost:5000/",
      method: "PATCH",
      timeout: 15000,
      data: { "shifts": shifts },
      // withCredentials: true,
      headers: { "X-Requested-With": "XMLHttpRequest" }
    }).then((res: AxiosResponse): void => {
      if (res.data["success"]) {
        alert("(patch) Save Succeded")
      } else {
        alert("(patch) Save Failed")
      }
    }).catch((err: AxiosError): void => {
      alert(err.message);
    });
  }

  updateAssetRequest = (updatedAsset: any): void => {
    let assetRequest = this.state.assetRequest;
    for (let i: number = 0; i < assetRequest.length; i++) {
      if (assetRequest[i].shiftID === updatedAsset.shiftID) {
        assetRequest[i].volunteers = updatedAsset.volunteers;
        i = assetRequest.length;
      }
    }
    const assignedVolunteers = this.identifyAssignedVolunteers(assetRequest);
    this.setState({ assetRequest, assignedVolunteers });
  }

  identifyAssignedVolunteers = (assetRequest: asset[]): Map<string, { shiftID: number, positionID: number }> => {
    let map: Map<string, { shiftID: number, positionID: number }> = new Map();
    assetRequest.map((a: asset) => {
      a.volunteers.map((p: Position) => {
        let v: (volunteer | undefined) = p.volunteer;
        if (!(typeof v === 'undefined')) {
          map.set(v.ID, { shiftID: a.shiftID, positionID: p.positionID })
        }
      })
    })
    return map;
  }

  render() {

    return (
      this.state.loading ? <div className="padding"><h4>Asset Request</h4><hr />Loading...</div> :
        <div className="padding">
          <h4>Asset Request</h4>
          <hr />
          {this.state.assetRequest.map((a: any) => (
            <Asset
              key={a.shiftID}
              asset={a}
              updateAssetRequest={(a: any) => this.updateAssetRequest(a)} //1.3.5
              volunteerList={this.state.volunteerList}
              assignedVolunteers={this.state.assignedVolunteers}
            />
          ))}
          <button onClick={this.submitData} className="type-1">
            Save
        </button>
        </div>
    );
  }
}