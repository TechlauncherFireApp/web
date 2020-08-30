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
  volunteer: volunteer; //not to be saved in database
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

  // 1.2.3, merges the vehicle times and vehicle list to create one central list with all relevant info for display
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

    //TODO get allVolunteers data from database
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
        let convertedAvailabilities : any = [];
        for (const a of v.availabilities) {
          const start = new Date(Date.parse(a[0]));
          const end = new Date(Date.parse(a[1]));
          convertedAvailabilities.push({startTime: start, endTime: end});
        }
        v.availabilities = convertedAvailabilities;
      }
      volunteerList = tmp

      if (recommendation.length != 0) {
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
        if (volunteerList.length != 0) {
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
        if (volunteerList.length != 0) {
          let assetRequest = this.mapVolunteersToRequest(recommendation, volunteerList);
          const assignedVolunteers = this.identifyAssignedVolunteers(assetRequest);
          this.setState({ assetRequest, volunteerList, assignedVolunteers })
        }
      }).catch((err: AxiosError): void => {
        alert(err.message);
      });
    }
  }

  // TESTING FUNCTION
  getTestData = (): void => {
    //   let assetRequest: any = [];
    //   let volunteerList: any = [];
    //   let now: Date = new Date();

    //   const asset1: any = {
    //     shiftID: 1,
    //     assetClass: "Light Unit",
    //     startTime: new Date(2020, 5, 10, 10),
    //     endTime: new Date(2020, 5, 10, 16),
    //     volunteers: [{
    //       positionID: 0,
    //       volunteerID: "1",
    //       roles: ["Driver", "Crew Leader"]
    //     },
    //     {
    //       positionID: 1,
    //       volunteerID: "2",
    //       roles: ["Crew Member"]
    //     }
    //     ]
    //   }
    //   const asset2: any = {
    //     shiftID: 2,
    //     assetClass: "Light Unit",
    //     startTime: now,
    //     endTime: now,
    //     volunteers: [{
    //       positionID: 0,
    //       volunteerID: "3",
    //       roles: ["Driver", "Crew Leader"]
    //     },
    //     {
    //       positionID: 1,
    //       volunteerID: "4",
    //       roles: ["Crew Member"]
    //     }
    //     ]
    //   }
    //   const recommendation: any[] = [asset1, asset2];

    //   const vol1: volunteer = {
    //     id: "1",
    //     firstName: "Caleb",
    //     lastName: "Addison",
    //     email: "caleb.blah@blah.com",
    //     mobileNo: "0412490340",
    //     prefHours: 10,
    //     possibleRoles: ["Driver", "Crew Leader", "Crew Member"],
    //     qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
    //     availability: [{ startTime: new Date(2020, 5, 10, 8), endTime: new Date(2020, 5, 10, 12) },
    //     { startTime: new Date(2020, 5, 10, 15), endTime: new Date(2020, 5, 10, 20) }]
    //   };
    //   const vol2: volunteer = {
    //     id: "2",
    //     firstName: "Tom",
    //     lastName: "Willis",
    //     email: "tom.blah@blah.com",
    //     mobileNo: "0411222333",
    //     prefHours: 15,
    //     possibleRoles: ["Crew Member"],
    //     qualifications: ["advanced training"],
    //     availability: [{ startTime: new Date(2022, 1, 1), endTime: new Date(2022, 2, 1) }]
    //   };
    //   const vol3: volunteer = {
    //     id: "3",
    //     firstName: "Amandeep",
    //     lastName: "Singh",
    //     email: "aman.blah@blah.com",
    //     mobileNo: "1234567890",
    //     prefHours: 8,
    //     possibleRoles: ["Driver", "Crew Leader", "Crew Member"],
    //     qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
    //     availability: [{ startTime: new Date(1990, 1, 1, 1, 1, 1, 1), endTime: new Date(1991, 1, 1, 1, 1, 1, 1) }]
    //   };
    //   const vol4: volunteer = {
    //     id: "4",
    //     firstName: "Stavros",
    //     lastName: "Dimos",
    //     email: "divos.blah@blah.com",
    //     mobileNo: "9876543120",
    //     prefHours: 20,
    //     possibleRoles: ["Driver", "Crew Leader", "Crew Member"],
    //     qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
    //     availability: [{ startTime: new Date(1990, 1, 1, 1, 1, 1, 1), endTime: new Date(1991, 1, 1, 1, 1, 1, 1) },
    //     { startTime: new Date(2020, 5, 10, 8), endTime: new Date(2020, 5, 10, 20) }]
    //   };
    //   const vol5: volunteer = {
    //     id: "5",
    //     firstName: "Cyrus",
    //     lastName: "Safdsar",
    //     email: "cyrus.blah@blah.com",
    //     mobileNo: "541234345",
    //     prefHours: 7,
    //     possibleRoles: ["Crew Member"],
    //     qualifications: ["advanced training",],
    //     availability: [{ startTime: new Date(2020, 1, 1, 1, 1, 1, 1), endTime: new Date(2021, 1, 1, 1, 1, 1, 1) }]
    //   };
    //   const vol6: volunteer = {
    //     id: "6",
    //     firstName: "Charles",
    //     lastName: "Luchetti",
    //     email: "charles.blah@blah.com",
    //     mobileNo: "123451234",
    //     prefHours: 14,
    //     possibleRoles: ["Driver", "Crew Member"],
    //     qualifications: ["heavy rigid license", "pump training", "advanced training",],
    //     availability: [{ startTime: new Date(2020, 1, 1, 1, 1, 1, 1), endTime: new Date(2021, 1, 1, 1, 1, 1, 1) }]
    //   };
    //   volunteerList.push(vol1);
    //   volunteerList.push(vol2);
    //   volunteerList.push(vol3);
    //   volunteerList.push(vol4);
    //   volunteerList.push(vol5);
    //   volunteerList.push(vol6);

    //   assetRequest = this.mapVolunteersToRequest(recommendation, volunteerList);
    //   const assignedVolunteers = this.identifyAssignedVolunteers(assetRequest);
    //   this.setState({ assetRequest, volunteerList, assignedVolunteers })
  }

  submitData(): void {
    //TODO need aman's help with this function (this is 1.3.8)
    //need to save the 'assetRequest' list in the database (IGNORING the volunteer field in each list of volunteers, i.e. only store the ID not all volunteer data)
    //can either happen every time a position is updated OR when the captain clicks save

    // TODO remove volunteer feild from each volunteer
    let shifts: any = this.state.assetRequest

    //path must be defined as "/assetRequest/volunteers/:id/:isNew"
    if (this.props.match.params.isNew === "new") {
      axios.request({
        url: "shift/request?requestID=" + this.props.id,
        baseURL: "http://localhost:5000/",
        method: "POST",
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

  //1.2.3, handles display
  render() {

    return (
      <React.Fragment>
        <h4 className="mt-2">New Asset Request</h4>
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