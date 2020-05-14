import React, { Component } from "react";
import "./Request.scss";

class Request extends Component {

    onClose = () => {
        this.props.removeAsset(this.props.id);
    }

    render() {
        return (
            <request-body>
                <img className="close" src={require("../../assets/x.png")} onClick={this.onClose} />
                <h2>{this.props.assetType}</h2>

                <div className="cont-1">
                    <div className="cont-2">
                        <label>Start</label>
                        <br/>
                        <div className="cont-3">{this.props.startDateTime.toLocaleDateString("en-GB",{day:"numeric",month:"long",year:"numeric"})}</div>
                        <div className="cont-3">{this.props.startDateTime.toLocaleTimeString("en-US",{hour:"numeric",minute:"numeric",hour12:true})}</div>
                    </div>
                    <div className="cont-2">
                        <label>End</label>
                        <br/>
                        <div className="cont-3">{this.props.endDateTime.toLocaleDateString("en-GB",{day:"numeric",month:"long",year:"numeric"})}</div>
                        <div className="cont-3">{this.props.endDateTime.toLocaleTimeString("en-US",{hour:"numeric",minute:"numeric",hour12:true})}</div>
                    </div>
                </div>
            </request-body>
        );
    }
}
export default Request;
