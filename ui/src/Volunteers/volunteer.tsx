import React, { Component } from "react";
import { Button } from "react-bootstrap";
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
    thisVolunteer?: volunteer;
}

export default class Volunteer extends React.Component<any, State> {

    state: State = {
        thisVolunteer: undefined
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
    }



    test = (): void => {
        console.log(this.state.thisVolunteer);
    }

    //state = {};
    render() {
        return (
            <div className="mt-2">
                <h4>{this.state.thisVolunteer?.firstName} {this.state.thisVolunteer?.lastName}</h4>
                <hr />
                <p>This is the volunteer page for {this.state.thisVolunteer?.firstName} {this.state.thisVolunteer?.lastName}.</p>
                <p>Here they will be able to see their assigned shifts, update their availability, and update their preferred hours.</p>

                <Button onClick={this.test} className="btn-med">print volunteer data (this.state.thisVolunteer) to console</Button>

            </div>
        );
    }
}