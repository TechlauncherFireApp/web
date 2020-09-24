import React, { Component } from "react";
import { Button } from "react-bootstrap";


// just a dummy state for now, implement however desired
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
        /* to view a request already existing in the database, simply call the below line window.open
           with 'id' replaced with the id of the selected request. */
        const id = "2a8a0f8767364af"
        window.open(window.location.origin + `/assetRequest/volunteers/${id}`, "_self", "", false);
    }

    render() {
        return (
            <div className="padding">
                <h4>View Existing Requests</h4>
                <hr />
                <button className="type-1" onClick={this.getRequest}>View: 2a8a0f8767364af</button>
            </div>
        );
    }
}