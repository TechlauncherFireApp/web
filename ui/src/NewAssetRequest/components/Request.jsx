import React, { Component } from "react";
import "./Request.scss";

class Request extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div class="Request-body">
        <p>{this.props.assetType}</p>
        &emsp;&emsp;-&emsp;&emsp;
        <p>{this.props.startTime}</p>
        &nbsp;
        <p>{this.props.startDate}</p>
        &nbsp;-&nbsp;
        <p>{this.props.endTime}</p>
        &nbsp;
        <p>{this.props.endDate}</p>
      </div>
    );
  }
}
export default Request;
