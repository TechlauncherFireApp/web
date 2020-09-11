import React from "react";

import AssetRequestVehicle from "./AssetRequestVehicle/AssetRequestVehicle";
import AssetRequestVolunteers from "./AssetRequestVolunteers/assetRequestVolunteers";

interface State {
  assetsSubmitted: boolean;
  assetRequest: any;
}

export default class AssetRequestContainer extends React.Component<any, State> {
  state = {
    assetsSubmitted: false,
    assetRequest: [],
  };


  submitRequest = (request: any): void => {





    this.setState({ assetsSubmitted: true, assetRequest: request });
  };

  render() {
    return (
      <React.Fragment>
        {this.state.assetsSubmitted ? (
          <AssetRequestVolunteers
            thisRequest={this.state.assetRequest}
            isNew={true}
            id={this.props.match.params.id}
          />
        ) : (
            <AssetRequestVehicle
              submitRequest={(r: any) => this.submitRequest(r)}
              id={this.props.match.params.id}
            />
          )}
      </React.Fragment>
    );
  }
}