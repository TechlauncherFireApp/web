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
    thisVolunteer?: volunteer;
    myShifts: any;
}

export default class Volunteer extends React.Component<any, State> {

    state: State = {
        thisVolunteer: undefined,
        myShifts: undefined
    }

    constructor(props: any) {
        super(props);
    }

    componentDidMount(): void {

        let id: string = this.props.match.params.id;
        // temp solution, get all volunteers from database and find the matching one
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

            let v: (volunteer | undefined) = undefined;
            for (let i = 0; i < l.length; i++) {
                if (l[i].ID === id) {
                    v = l[i];
                    i = l.length;
                }
            }
            this.setState({ thisVolunteer: v })
        }).catch((err: AxiosError): void => {
            alert(err.message);
        });


        /* the way it should be done: query the database to return only the specific volunteer in question:
           
           query might look something like the following:
           
        query = """
            SELECT
                `id` AS `ID`,`firstName`,`lastName`,`email`,`mobileNo`,`prefHours`,`expYears`,`possibleRoles`,`qualifications`,`availabilities`
            FROM
                `volunteer`
            WHERE
                `id` = $id
            LIMIT
                1;"""           
           */

        // axios.request({
        //     url: "volunteer/specific",
        //     baseURL: "http://localhost:5000/",
        //     method: "POST",
        //     data: { "id:": id },
        //     timeout: 15000,
        //     // withCredentials: true,
        //     headers: { "X-Requested-With": "XMLHttpRequest" }

        // }).then((res: AxiosResponse): void => {
        //     let vol = res.data["results"]
        //     let convertedAvailabilities: any = [];
        //     for (const a of vol.availabilities) {
        //         const start = new Date(Date.parse(a[0]));
        //         const end = new Date(Date.parse(a[1]));
        //         convertedAvailabilities.push({ startTime: start, endTime: end });
        //     }
        //     vol.availabilities = convertedAvailabilities;
        //     this.setState({ thisVolunteer: vol })
        // }).catch((err: AxiosError): void => {
        //     alert(err.message);
        // });

        this.state.myShifts = this.getDummyShiftData();
    }

    //testing function that generates some dummy data (in the format I would like it to be returned from DB)
    getDummyShiftData = (): any => {
        const shift1: any = {
            requestID: "req1",
            requestTitle: "Kowen fire",
            vehicleID: "veh1",
            vehicleType: "lightUnit",
            vehicleFrom: new Date(2020, 6, 10, 10),
            vehicleTo: new Date(2020, 6, 10, 16),
            shiftID: "shf1",
            volunteerRoles: ["driver", "crewLeader"],
            volunteerStatus: "confirmed",
        }
        const shift3: any = {
            requestID: "req2",
            requestTitle: "Orroral Valley",
            vehicleID: "veh2",
            vehicleType: "heavyTanker",
            vehicleFrom: new Date(2020, 6, 12, 14),
            vehicleTo: new Date(2020, 6, 12, 20),
            shiftID: "shf2",
            volunteerRoles: ["crewLeader"],
            volunteerStatus: "pending",
        }
        const shift2: any = {
            requestID: "req3",
            requestTitle: "Orroral Valley",
            vehicleID: "veh3",
            vehicleType: "heavyTanker",
            vehicleFrom: new Date(2020, 6, 16, 22),
            vehicleTo: new Date(2020, 6, 17, 6),
            shiftID: "shf3",
            volunteerRoles: ["driver"],
            volunteerStatus: "pending",
        }
        let shifts: any[] = [shift1, shift2, shift3];
        shifts.sort((a, b) => ((a.vehicleFrom > b.vehicleFrom) ? 1 : -1));
        return shifts;
    }

    test = (): void => {
        console.log(this.state.thisVolunteer);
    }

    updateStatus = (newStatus: string, shiftData: any): void => {
        //TODO update the asset_request_volunteer.status in the database
        console.log(newStatus, shiftData);

    }

    //state = {};
    render() {
        return (
            <div className="mt-2">
                <div>
                    <h4>{this.state.thisVolunteer?.firstName} {this.state.thisVolunteer?.lastName}</h4>
                    <hr />
                    <p>This is the volunteer page for {this.state.thisVolunteer?.firstName} {this.state.thisVolunteer?.lastName}.</p>
                    <p>Here they will be able to see their assigned shifts, update their availability, and update their preferred hours.</p>
                    <Button onClick={this.test} className="btn-med">print volunteer data (this.state.thisVolunteer) to console</Button>
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
                                ? <tr></tr>
                                : this.state.myShifts.map((s: any) =>
                                    <Shift key={s.shiftID}
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