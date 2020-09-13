import React, { Component } from "react";
import AssetRequestVolunteers from "../AssetRequestVolunteers/assetRequestVolunteers";
import ExistingRequestSelector from "./existingRequestSelector";

interface State {
    requestChosen: boolean;
    selectedRequestID: string;
}

export default class ExistingRequestContainer extends React.Component<any, State> {
    state = {
        requestChosen: false,
        selectedRequestID: "",
    };

    getRequest = (requestID: string): void => {
        this.setState({ requestChosen: true, selectedRequestID: requestID });
    };

    render() {
        return (
            <React.Fragment>
                {this.state.requestChosen ? (
                    <AssetRequestVolunteers
                        // thisRequest={this.state.selectedRequest}
                        isNew={false}
                        id={this.state.selectedRequestID}
                    />
                ) : (
                        <ExistingRequestSelector
                            getRequest={(s: string) => this.getRequest(s)}
                        />
                    )}
            </React.Fragment>
        );
    }
}