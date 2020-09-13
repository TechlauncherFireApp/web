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
            <React.Fragment>
                <h4>selector page</h4>
                <Button onClick={this.getRequest}>View</Button>
            </React.Fragment>
        );
    }
}