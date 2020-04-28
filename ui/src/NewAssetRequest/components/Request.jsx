import React, { Component } from "react";
import "./Request.scss";

class Request extends Component {

    constructor(props) {
        super(props);
    }

    onClose = () => {
        this.props.Remove_Asset(JSON.stringify({
            assetType: this.props.assetType,
            startDate: this.props.startDate,
            startTime: this.props.startTime,
            endDate: this.props.endDate,
            endTime: this.props.endTime
        }));
    }

    render() {
        return (
            <request-body>
                <img className="close" src={require("../../assets/x.png")} onClick={this.onClose} />
                <div>
                    <img className="poster" src={require("../../assets/nothing.png")} />
                    <div>
                        <span>{this.props.assetType}</span>
                        <div>
                            <span>Start</span>
                            <span>{this.props.startDateTime.toLocaleDateString()} | {this.props.startDateTime.toLocaleTimeString()}</span>
                        </div>
                        <div>
                            <span>End</span>
                            <span>{this.props.endDateTime.toLocaleDateString()} | {this.props.endDateTime.toLocaleTimeString()}</span>
                        </div>
                    </div>
                </div>
            </request-body>
        );
    }
}
export default Request;
