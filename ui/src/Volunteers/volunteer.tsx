import React, { Component } from "react";
import { Button, Table } from "react-bootstrap";
import axios, { AxiosResponse, AxiosError } from "axios";
import Shift from "./shift";

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
    loading: boolean,
    thisVolunteer?: volunteer;
    myShifts: any;
}

export default class Volunteer extends React.Component<any, State> {

    state: State = {
        loading: true,
        thisVolunteer: undefined,
        myShifts: undefined
    }

    constructor(props: any) {
        super(props);
    }

    componentDidMount(): void {

        let id: string = this.props.match.params.id;
        let l: volunteer[] = [];
        axios.request({
            url: "volunteer",
            method: "GET",
            params: { "volunteerID": this.props.match.params.id },
            timeout: 15000,
            // withCredentials: true,
            headers: { "X-Requested-With": "XMLHttpRequest" }
        }).then((res: AxiosResponse): void => {
            let tmp = res.data
            let convertedAvailabilities: any = [];
            for (const a of tmp.availabilities) {
                const start = new Date(Date.parse(a[0]));
                const end = new Date(Date.parse(a[1]));
                convertedAvailabilities.push({ startTime: start, endTime: end });
            }
            tmp.availabilities = convertedAvailabilities;
            this.setState({ thisVolunteer: tmp, loading: false })
        }).catch((err: AxiosError): void => {
            alert(err.message);
        });

        axios.request({
            url: "volunteer/shifts",
            method: "GET",
            params: { "volunteerID": this.props.match.params.id },
            timeout: 15000,
            // withCredentials: true,
            headers: { "X-Requested-With": "XMLHttpRequest" }
        }).then((res: AxiosResponse): void => {
            let tmp = res.data["results"]
            if (tmp !== null) {
                for (const t of tmp) {
                    t.vehicleFrom = new Date(Date.parse(t.vehicleFrom));
                    t.vehicleTo = new Date(Date.parse(t.vehicleTo));
                }
                this.setState({ myShifts: tmp })
            }

        }).catch((err: AxiosError): void => {
            alert(err.message);
        });
    }

    //testing function that generates some dummy data (in the format I would like it to be returned from DB)
    getDummyShiftData = (): any => {
        const shift1: any = {
            requestTitle: "Kowen fire",
            vehicleID: "veh1",
            vehicleType: "lightUnit",
            vehicleFrom: new Date(2020, 6, 10, 10),
            vehicleTo: new Date(2020, 6, 10, 16),
            volunteerRoles: ["driver", "crewLeader"],
            volunteerStatus: "confirmed",
        }

        /* Given a 'volID' I need a list of the following objects returned,
            (for all asset-request_volunteer where asset-request_volunteer.idVolunteer == volID */
        const shift3: any = {
            requestTitle: "Orroral Valley",         //asset-request.title            (String)  
            vehicleID: "veh2",                      //asset-request_vehicle.id       (String)
            vehicleType: "heavyTanker",             //vehicle.type                   (String)
            vehicleFrom: new Date(2020, 6, 12, 14), //asset-request_vehicle.from     (Date)
            vehicleTo: new Date(2020, 6, 12, 20), //asset-request_vehicle.to       (Date)
            volunteerRoles: ["crewLeader"],         //asset-request_volunteer.roles  (string[])
            volunteerStatus: "pending",             //asset-request_volunteer.status (string)
        }
        const shift2: any = {
            requestTitle: "Orroral Valley",
            vehicleID: "veh3",
            vehicleType: "heavyTanker",
            vehicleFrom: new Date(2020, 6, 16, 22),
            vehicleTo: new Date(2020, 6, 17, 6),
            volunteerRoles: ["driver"],
            volunteerStatus: "pending",
        }
        let shifts: any[] = [shift1, shift2, shift3];
        shifts.sort((a, b) => ((a.vehicleFrom > b.vehicleFrom) ? 1 : -1));
        return shifts;
    }

    manageAvailability = (): void => {
        window.open(window.location.origin + `/volunteer/${this.props.match.params.id}/availability`, "_self", "", false)

    }

    updateStatus = (newStatus: string, shiftData: any): void => {
        //console.log(newStatus, shiftData);
        const info = {
            idVolunteer: this.state.thisVolunteer?.ID,
            idVehicle: shiftData.vehicleID,
            status: newStatus
        }

        axios.request({
            url: "volunteer/status",
            method: "PATCH",
            timeout: 15000,
            params: info,
            headers: { "X-Requested-With": "XMLHttpRequest" }
        }).catch((err: AxiosError): void => {
            alert(err.message);
        });

    }

    //state = {};
    render() {
        return (
            this.state.loading ? <div className="padding"><h4>Volunteers</h4><hr />Loading...</div> :

                <div className="padding">
                    <div>
                        <h4>{this.state.thisVolunteer?.firstName} {this.state.thisVolunteer?.lastName}</h4>
                        <hr />
                        <p>This is the volunteer page for {this.state.thisVolunteer?.firstName} {this.state.thisVolunteer?.lastName}.</p>
                        <p>Here they will be able to see their assigned shifts, update their availability, and update their preferred hours.</p>
                        <button className="type-1" onClick={this.manageAvailability}>Manage Availability</button>
                    </div>
                    <div className="mt-3">
                        <h5>My Shifts</h5>
                        <Table className="mt-2" striped bordered hover size="sm">

                            <thead>
                                <tr>
                                    <th>Date and Time</th>
                                    <th>Role</th>
                                    <th>Asset</th>
                                    <th>Request Title</th>
                                    <th>My Status</th>
                                </tr>
                            </thead>
                            <tbody>

                                {(this.state.myShifts === undefined)
                                    ? <tr><td colSpan={5}>None</td></tr>
                                    : this.state.myShifts.map((s: any) =>
                                        <Shift key={s.vehicleID}
                                            shift={s}
                                            updateStatus={(a: string, b: any) => this.updateStatus(a, b)} />
                                    )

                                }

                            </tbody>
                        </Table>

                    </div>
                </div>
        );
    }
}