import React, { Component } from "react";
import { Table } from "react-bootstrap";
import Position from "./position";

interface State {

}

export default class Asset extends React.Component<any, State> {

  state: State = {

  };


  // handles display of date/time info
  parseDateTime = (date1: Date, date2: Date): string => {
    let str = date1.toLocaleTimeString("en-US", { hour12: true, hour: "numeric", minute: "numeric" });
    if (
      date1.getMonth() === date2.getMonth() &&
      date1.getDate() === date2.getDate() &&
      date1.getFullYear() === date2.getFullYear()
    ) {
      //if the request starts and ends on the same day
      str = str + " - " + date2.toLocaleTimeString("en-US", { hour12: true, hour: "numeric", minute: "numeric" }) + " "
        + date2.toLocaleDateString("en-GB");
    } else {
      str = str + " " + date1.toLocaleDateString("en-GB") + " - "
        + date2.toLocaleTimeString("en-US", { hour12: true, hour: "numeric", minute: "numeric" }) + " "
        + date2.toLocaleDateString("en-GB");
    }
    return str.toLowerCase();
  };

  // 1.3.5, if a volunteer is changed update the relevant fields and propogate the change up through parent components
  updateAsset = (newPosition: any): void => {
    let asset = this.props.asset;
    for (let i: number = 0; i < asset.volunteers.length; i++) {
      if (asset.volunteers[i].positionID === newPosition.positionID) {
        asset.volunteers[i].volunteer = newPosition.volunteer;
        i = asset.volunteers.length;
      }
    }
    this.props.updateAssetRequest(asset);
  }

  formatPositionInfo = (position: any): any => {
    /* 
    position: {
    shiftID: number
    positionID: number
    assigned: boolean
    volunteer:
    asset: string
    role: string[]
    startTime: Date
    endTime: Date
    } */
    let asset = this.props.asset
    let positionInfo = {
      shiftID: asset.shiftID,
      positionID: position.positionID,
      assigned: true,
      volunteer: position.volunteer,
      assetClass: asset.assetClass,
      role: position.role,
      startTime: asset.startTime,
      endTime: asset.endTime
    }
    if (typeof positionInfo.volunteer === 'undefined') {
      positionInfo.assigned = false;
    }
    return positionInfo;
  }

  // 1.2.3
  render() {
    const { asset } = this.props;

    return (
      <Table className="mt-4" striped bordered hover size="sm">
        <thead>
          <tr>
            <td width="15%"><b>({asset.shiftID}) {asset.assetClass}</b> </td>
            <td colSpan={6}> {/* TODO had to change this from "6" to {6}, make sure it works*/}
              <span>
                {this.parseDateTime(
                  asset.startTime,
                  asset.endTime
                )}
              </span>
            </td>
          </tr>
        </thead>
        <tbody>
          {asset.volunteers.map((position: any) =>
            <Position key={position.positionID}
              updateAsset={(a: any) => this.updateAsset(a)}
              volunteerList={this.props.volunteerList}
              assignedVolunteers={this.props.assignedVolunteers}
              position={this.formatPositionInfo(position)} />
          )}
        </tbody>
      </Table>
    );
  }
}
