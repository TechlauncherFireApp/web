import React from 'react';
import Asset from './asset';
import axios, { AxiosResponse, AxiosError } from 'axios';
import { dateToBackend, dateFromBackend } from '../functions';

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
  assignedVolunteers: Map<string, { shiftID: number; positionID: number }>;
  assetRequest: asset[];
}

export default class AssetRequestVolunteers extends React.Component<
  any,
  State
> {
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

  mapVolunteersToRequest = (
    assets: any[],
    volunteerList: volunteer[]
  ): asset[] => {
    // this is not the most efficient method but it's very simple. I believe it's O(n^2) but as we're working with small data this should be fine
    let output = [...assets];
    for (const asset of output) {
      for (const position of asset.volunteers) {
        //find the corresponding volunteer

        if (position.ID === '') {
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
  };

  getVolunteerList = (): Promise<volunteer[]> => {
    // Get the current 'global' time from an API using Promise
    return new Promise((resolve) => {
      axios
        .request({
          url: 'volunteer/all',
          method: 'GET',
          timeout: 15000,
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        })
        .then((res: AxiosResponse): void => {
          let tmp = res.data['results'];
          for (const v of tmp) {
            let convertedAvailabilities: any = [];
            // for (const a of v.availabilities) {
            //   const start = dateFromBackend(a[0]);
            //   const end = dateFromBackend(a[1]);
            //   convertedAvailabilities.push({ startTime: start, endTime: end });
            // }
            v.availabilities = convertedAvailabilities;
          }
          resolve(tmp);
        })
        .catch((err: AxiosError): void => {
          // @ts-ignore
          if (err.response.status === 401) {
            this.props.history.push('/login');
          } else {
            alert(err.message);
          }
        });
    });
  };

  getInitialData = (): void => {
    let volunteerList: volunteer[] = [];
    let recommendation: any = [];

    //get allVolunteers data from database
    this.getVolunteerList().then((tmp: volunteer[]): void => {
      // Assign volunteer list
      volunteerList = tmp;
      volunteerList.sort((a, b) =>
        a.firstName > b.firstName
          ? 1
          : a.firstName === b.firstName
          ? a.lastName > b.lastName
            ? 1
            : -1
          : -1
      );

      if (recommendation.length !== 0) {
        let assetRequest = this.mapVolunteersToRequest(
          recommendation,
          volunteerList
        );
        const assignedVolunteers = this.identifyAssignedVolunteers(
          assetRequest
        );
        this.setState({
          assetRequest,
          volunteerList,
          assignedVolunteers,
          loading: false,
        });
      }
    });

    //get the request volunteer data from the database
    axios
      .request({
        url: 'shift/request?requestID=' + this.props.match.params.id,
        method: 'GET',
        timeout: 15000,
        // withCredentials: true,
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((res: AxiosResponse): void => {
        console.log(res);
        let tmp = res.data['results'];
        if (tmp !== null) {
          for (const r of tmp) {
            r.startTime = dateFromBackend(r.startTime);
            r.endTime = dateFromBackend(r.endTime);
          }
        }
        recommendation = tmp;
        // Both volunteerList and recommendation need to be populated
        if (volunteerList.length !== 0) {
          let assetRequest = this.mapVolunteersToRequest(
            recommendation,
            volunteerList
          );
          const assignedVolunteers = this.identifyAssignedVolunteers(
            assetRequest
          );
          this.setState({
            assetRequest,
            volunteerList,
            assignedVolunteers,
            loading: false,
          });
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
  };

  submitData = (): void => {
    const shifts = this.state.assetRequest;

    let requestData: any = [];
    shifts.forEach((shift) => {
      requestData.push({
        shiftID: shift.shiftID,
        assetClass: shift.assetClass,
        startTime: dateToBackend(shift.startTime),
        endTime: dateToBackend(shift.endTime),
        volunteers: shift.volunteers,
      });
    });

    //Patch request
    axios
      .request({
        url: 'shift/request?requestID=' + this.props.match.params.id,
        method: 'PATCH',
        timeout: 15000,
        data: { shifts: requestData },
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((res: AxiosResponse): void => {
        if (res.data['success']) {
          alert('Save Succeeded');
        } else {
          alert('Save Failed');
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
  };

  deleteData = (): void => {
    const params = {
      requestID: String = this.props.match.params.id,
    };
    const headers = {
      Authorization: 'Bearer ' + localStorage.getItem('access_token'),
    };
    axios
      .delete('new_request',{ params: params, headers: headers })
      .then((resp) => {
        window.open(
        window.location.origin + '/captain',
        'self_',
        '',
        false
        );
      })
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
  };

  identifyAssignedVolunteers = (
    assetRequest: asset[]
  ): Map<string, { shiftID: number; positionID: number }> => {
    let map: Map<string, { shiftID: number; positionID: number }> = new Map();
    assetRequest.map((a: asset) => {
      a.volunteers.map((p: Position) => {
        let v: volunteer | undefined = p.volunteer;
        if (!(typeof v === 'undefined')) {
          map.set(v.ID, { shiftID: a.shiftID, positionID: p.positionID });
        }
      });
    });
    return map;
  };

  render() {
    return this.state.loading ? (
      <div className="padding">
        <h4>Asset Request</h4>
        <hr />
        Loading...
      </div>
    ) : (
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
        <button onClick={this.deleteData} className="type-2">
          Delete
        </button>
      </div>
    );
  }
}
