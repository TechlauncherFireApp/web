import React, { Component } from "react";
import { Button } from "react-bootstrap";

interface State {
    selectedRequest: any;
    selectedID: string;
    allRequests: any;
}

export default class ExistingRequestSelector extends React.Component<any, State> {
    state = {
        selectedRequest: undefined,
        selectedID: "",
        allRequests: undefined,
    };

    getRequest = (): void => {
        this.props.getRequest("dsa")
    }

    render() {
        return (
            <div className="padding">
                <h4>selector page</h4>
                <button className="type-1" onClick={this.getRequest}>View</button>
            </div>
        );
    }
}