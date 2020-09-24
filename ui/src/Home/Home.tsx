import React from "react";
import "./Home.scss";
import axios, { AxiosResponse, AxiosError } from "axios";


export default class Home extends React.Component<any, any> {

    captain(): void {
        window.open(window.location.origin + `/captain`, "_self", "", false)
    }

    volunteer(): void {
        window.open(window.location.origin + `/volunteer`, "_self", "", false)
    }

    render() {
        return (
            <div className="padding">
                <button className="type-1 margin" onClick={() => this.captain()}>I am a Brigade Captain</button>
                <button className="type-1 margin" onClick={() => this.volunteer()}>I am a Volunteer</button>
            </div>
        );
    }
}