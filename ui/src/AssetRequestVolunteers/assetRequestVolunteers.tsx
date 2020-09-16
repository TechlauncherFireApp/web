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
}

interface asset {
  shiftID: number;
  assetClass: string;
  startTime: Date;
  endTime: Date;
  volunteers: Position[];
}

interface State {
  allow_getInitialData: boolean;
  volunteerList: volunteer[];
  assignedVolunteers: Map<string, { shiftID: number, positionID: number }>;
  assetRequest: asset[];
}

export default class AssetRequestVolunteers extends React.Component<any, State> {

  state: State = {
    allow_getInitialData: true,
    volunteerList: [],
    assignedVolunteers: new Map(),
    assetRequest: []
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
        for (let j = 0; j < volunteerList.length; j++) {
          if (volunteerList[j].ID === position.ID) {
            position.volunteer = { ...volunteerList[j] };
            j = volunteerList.length;
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
      volunteerList = tmp
      volunteerList.sort((a, b) => ((a.firstName > b.firstName) ? 1 : ((a.firstName === b.firstName) ? ((a.lastName > b.lastName) ? 1 : -1) : -1)));

      if (recommendation.length !== 0) {
        let assetRequest = this.mapVolunteersToRequest(recommendation, volunteerList);
        const assignedVolunteers = this.identifyAssignedVolunteers(assetRequest);
        this.setState({ assetRequest, volunteerList, assignedVolunteers })
      }
    }).catch((err: AxiosError): void => {
      alert(err.message);
    });



    if (this.props.isNew) {
      //TODO get new recommendation from scheduler

      let requestData: any = [];
      for (const asset of this.props.thisRequest) {
        requestData.push({
          shiftID: asset.idVehicle,
          assetClass: asset.type,
          startTime: asset.startDateTime.toISOString(),
          endTime: asset.endDateTime.toISOString()
        });
      }

      //TODO get the vehicle information for the request
      axios.request({
        url: "recommendation",
        baseURL: "http://localhost:5000/",
        method: "POST",
        data: { "request": requestData },
        timeout: 15000,
        // withCredentials: true,
        headers: { "X-Requested-With": "XMLHttpRequest" }
      }).then((res: AxiosResponse): void => {
        let tmp = res.data["results"]

        for (const r of tmp) {
          r.startTime = new Date(Date.parse(r.startTime));
          r.endTime = new Date(Date.parse(r.endTime));
        }
        recommendation = tmp;
        // Both volunteerList and recommendation need to be populated
        if (volunteerList.length !== 0) {
          let assetRequest = this.mapVolunteersToRequest(recommendation, volunteerList);
          const assignedVolunteers = this.identifyAssignedVolunteers(assetRequest);
          this.setState({ assetRequest, volunteerList, assignedVolunteers })
        }
      }).catch((err: AxiosError): void => {
        alert(err.message);
      });
    } else {
      //TODO get saved asset request data from database
      axios.request({
        url: "shift/request?requestID=" + this.props.id,
        baseURL: "http://localhost:5000/",
        method: "GET",
        timeout: 15000,
        // withCredentials: true,
        headers: { "X-Requested-With": "XMLHttpRequest" }
      }).then((res: AxiosResponse): void => {
        recommendation = res.data["results"]

        // Both volunteerList and recommendation need to be populated
        if (volunteerList.length !== 0) {
          let assetRequest = this.mapVolunteersToRequest(recommendation, volunteerList);
          const assignedVolunteers = this.identifyAssignedVolunteers(assetRequest);
          this.setState({ assetRequest, volunteerList, assignedVolunteers })
        }
      }).catch((err: AxiosError): void => {
        alert(err.message);
      });
    }
  }

  submitData = (): void => {
    //TODO need aman's help with this function (this is 1.3.8)
    //need to save the 'assetRequest' list in the database (IGNORING the volunteer field in each list of volunteers, i.e. only store the ID not all volunteer data)
    //can either happen every time a position is updated OR when the captain clicks save

    // format the data as expected by the endpoint
    //const shifts = this.formatForDB(this.state.assetRequest);

    const shifts = this.state.assetRequest;
    console.log(shifts)

    if (this.props.isNew === true) {
      axios.request({
        url: "shift/request?requestID=" + this.props.id,
        baseURL: "http://localhost:5000/",
        method: "POST",
        timeout: 15000,
        data: { "shifts": shifts },
        // withCredentials: true,
        headers: { "X-Requested-With": "XMLHttpRequest" }
      }).then((res: AxiosResponse): void => {
        console.log(res.data)
        if (res.data.success) {
          alert("Save Succeded")
        } else {
          alert("Save Failed")
        }
      }).catch((err: AxiosError): void => {
        alert(err.message);
      });
    } else {
      axios.request({
        url: "shift/request?requestID=" + this.props.id,
        baseURL: "http://localhost:5000/",
        method: "PATCH",
        timeout: 15000,
        data: { "shifts": shifts },
        // withCredentials: true,
        headers: { "X-Requested-With": "XMLHttpRequest" }
      }).then((res: AxiosResponse): void => {
        if (res.data["success"]) {
          alert("Save Succeded")
        } else {
          alert("Save Failed")
        }
      }).catch((err: AxiosError): void => {
        alert(err.message);
      });
    }
  }

  //we only need certain fields in the assetRequest for storing in the database
  //this function returns a new object that only has those required fields
  formatForDB = (request: any): any => {
    console.log("inside formatForDB", request)
    let shifts = [];
    for (let s of request) {
      let shift: any = { shiftID: "", volunteers: [] }
      shift.shiftID = s.shiftID;
      for (let v of s.volunteers) {
        shift.volunteers.push({ ID: v.ID, positionID: v.positionID, roles: v.role });
      }
      shifts.push(shift);
    }
    return shifts;
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
        let v: volunteer = p.volunteer;
        if (!(typeof v === 'undefined')) {
          map.set(v.ID, { shiftID: a.shiftID, positionID: p.positionID })
        }
      })
    })
    return map;
  }

  render() {

    return (
      <React.Fragment>
        <h4 className="mt-2">Asset Request</h4>
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
        <Button onClick={this.submitData} className="btn-med">
          Save
        </Button>
      </React.Fragment>
    );
  }
}