import React, { Component } from "react";
import Asset from "./asset";
import { Button } from "react-bootstrap";

interface Timeframe {
  startTime: Date;
  endTime: Date;
}

interface volunteer {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  mobileNo: string;
  prefHours: number;
  //expYears: start date
  possibleRoles: string[];
  qualifications: string[];
  availabilities: Timeframe[];
}

interface Position {
  positionID: number;
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

  // 1.2.3, merges the vehicle times and vehicle list to create one central list with all relevant info for display
  constructor(props: any) {
    super(props);
    if (this.state.volunteerList.length > 0) {
      this.identifyAssignedVolunteers(this.state.assetRequest);
    }
  }

  componentDidMount(): void {   // I think this needs to be WillMount rather than DidMount to display appropriate info
    this.getInitialData();

    // HARD CODED DUMMY DATA FOR TESTING ~ BEGIN
    let assetRequest: any = [];
    let volunteerList: any = [];
    let now: Date = new Date();


    const asset1: asset = {
      shiftID: 1,
      assetClass: "Light Unit",
      startTime: now,
      endTime: now,
      volunteers: [{
        positionID: 0,
        volunteer: {
          id: "1",
          firstName: "Caleb",
          lastName: "Addison",
          email: "caleb.blah@blah.com",
          mobileNo: "0412490340",
          prefHours: 10,
          possibleRoles: ["Driver", "Crew Leader", "Crew Member"],
          qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
          availabilities: [{ startTime: now, endTime: now }]
        },
        role: ["Driver"]
      },
      {
        positionID: 1,
        volunteer: {
          id: "2",
          firstName: "Tom",
          lastName: "Willis",
          email: "tom.blah@blah.com",
          mobileNo: "0411222333",
          prefHours: 15,
          possibleRoles: ["Crew Member"],
          qualifications: ["advanced training"],
          availabilities: [{ startTime: now, endTime: now }]
        },
        role: ["Crew Member"]
      }
      ]
    }
    const asset2: asset = {
      shiftID: 2,
      assetClass: "Light Unit",
      startTime: now,
      endTime: now,
      volunteers: [{
        positionID: 0,
        volunteer: {
          id: "3",
          firstName: "Amandeep",
          lastName: "Singh",
          email: "aman.blah@blah.com",
          mobileNo: "1234567890",
          prefHours: 8,
          possibleRoles: ["Driver", "Crew Leader", "Crew Member"],
          qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
          availabilities: [{ startTime: now, endTime: now }]
        },
        role: ["Driver"]
      },
      {
        positionID: 1,
        volunteer: {
          id: "4",
          firstName: "Stavros",
          lastName: "Dimos",
          email: "divos.blah@blah.com",
          mobileNo: "9876543120",
          prefHours: 20,
          possibleRoles: ["Driver", "Crew Leader", "Crew Member"],
          qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
          availabilities: [{ startTime: now, endTime: now }]
        },
        role: ["Crew Member"]
      }
      ]
    }
    assetRequest.push(asset1);
    assetRequest.push(asset2);

    const vol1: volunteer = {
      id: "1",
      firstName: "Caleb",
      lastName: "Addison",
      email: "caleb.blah@blah.com",
      mobileNo: "0412490340",
      prefHours: 10,
      possibleRoles: ["Driver", "Crew Leader", "Crew Member"],
      qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
      availabilities: [{ startTime: now, endTime: now }]
    };
    const vol2: volunteer = {
      id: "2",
      firstName: "Tom",
      lastName: "Willis",
      email: "tom.blah@blah.com",
      mobileNo: "0411222333",
      prefHours: 15,
      possibleRoles: ["Crew Member"],
      qualifications: ["advanced training"],
      availabilities: [{ startTime: now, endTime: now }]
    };
    const vol3: volunteer = {
      id: "3",
      firstName: "Amandeep",
      lastName: "Singh",
      email: "aman.blah@blah.com",
      mobileNo: "1234567890",
      prefHours: 8,
      possibleRoles: ["Driver", "Crew Leader", "Crew Member"],
      qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
      availabilities: [{ startTime: now, endTime: now }]
    };
    const vol4: volunteer = {
      id: "4",
      firstName: "Stavros",
      lastName: "Dimos",
      email: "divos.blah@blah.com",
      mobileNo: "9876543120",
      prefHours: 20,
      possibleRoles: ["Driver", "Crew Leader", "Crew Member"],
      qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
      availabilities: [{ startTime: now, endTime: now }]
    };
    const vol5: volunteer = {
      id: "5",
      firstName: "Cyrus",
      lastName: "Safdsar",
      email: "cyrus.blah@blah.com",
      mobileNo: "541234345",
      prefHours: 7,
      possibleRoles: ["Crew Member"],
      qualifications: ["advanced training",],
      availabilities: [{ startTime: now, endTime: now }]
    };
    const vol6: volunteer = {
      id: "6",
      firstName: "Charles",
      lastName: "Luchetti",
      email: "charles.blah@blah.com",
      mobileNo: "123451234",
      prefHours: 14,
      possibleRoles: ["Driver", "Crew Leader", "Crew Member"],
      qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
      availabilities: [{ startTime: now, endTime: now }]
    };
    volunteerList.push(vol1);
    volunteerList.push(vol2);
    volunteerList.push(vol3);
    volunteerList.push(vol4);
    volunteerList.push(vol5);
    volunteerList.push(vol6);

    const assignedVolunteers = this.identifyAssignedVolunteers(assetRequest);
    this.setState({ assetRequest, volunteerList, assignedVolunteers })
    // HARD CODED DUMMY DATA FOR TESTING ~ END
  }


  getInitialData(): void {
    //TODO need aman's help with this function
    //need to populate 'assetRequest' from the database (or from the backend, I think it would be better to go through the database however as that makes this component extendable)
    //need to populate 'volunteerList' from the database (data for all volunteers, this is okay to do because we're only working with a small amount of data ~100 entries)
  }

  submitData(): void {
    //TODO need aman's help with this function
    //need to save the 'assetRequest' list in the database
    //can either happen every time a position is updated OR when the captain clicks save
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
          map.set(v.id, { shiftID: a.shiftID, positionID: p.positionID })
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