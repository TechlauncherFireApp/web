import React, { Component } from "react";
import "./Request.scss";

class Request extends Component {

    // constructor(props) {
    //     super(props);
    // }

    onClose = () => {
        this.props.removeAsset(this.props.id);
    }

    render() {
        return (
            <request-body>
                <img className="close" alt="Asset" src={require("../../assets/x.png")} onClick={this.onClose} />
                <div>
                    <img className="poster" alt="Asset" src={require("../../assets/nothing.png")} />
                    <div>
                        <span>{this.props.assetType}</span>
                        <div>
                            <span>Start</span>
                            <span>{this.props.startDateTime.toLocaleDateString("en-GB",{day:"numeric",month:"long",year:"numeric"})} | {this.props.startDateTime.toLocaleTimeString("en-US",{hour:"numeric",minute:"numeric",hour12:true})}</span>
                        </div>
                        <div>
                            <span>End</span>
                            <span>{this.props.endDateTime.toLocaleDateString("en-GB",{day:"numeric",month:"long",year:"numeric"})} | {this.props.endDateTime.toLocaleTimeString("en-US",{hour:"numeric",minute:"numeric",hour12:true})}</span>
                        </div>
                    </div>
                </div>
            </request-body>
        );
    }
}
export default Request;
