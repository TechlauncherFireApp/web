import React from "react";
import "./brigadeCaptainHome.scss";
import axios, { AxiosResponse, AxiosError } from "axios";
import { contains } from "../functions";

interface State {
  request_title: string;
  allow_makeNewRequest: boolean;
}

export default class BrigadeCaptainHome extends React.Component<any, State> {

  state: State = {
    request_title: "",
    allow_makeNewRequest: true
  };

  makeNewRequest(): void {
    if (!this.state.allow_makeNewRequest) return;
    this.setState({ allow_makeNewRequest: false });

    if (!contains(this.state.request_title)) {
      alert("Title not assigned");
      this.setState({ allow_makeNewRequest: true });
      return;
    }

    axios.request({
      url: "new_request",
      baseURL: "http://localhost:5000/",
      method: "POST",
      data: { "title": this.state.request_title },
      timeout: 15000,
      // withCredentials: true,
      headers: { "X-Requested-With": "XMLHttpRequest" }
    }).then((res: AxiosResponse): void => {
      if ((typeof res.data === "object") && contains(res.data["id"])) window.open(window.location.origin + `/assetRequest/vehicles/${res.data["id"]}`, "_self", "", false);
      else if (typeof res.data === "string") {
        alert(res.data);
        this.setState({ allow_makeNewRequest: true });
      }
    }).catch((err: AxiosError): void => {
      alert(err.message);
      this.setState({ allow_makeNewRequest: true });
    });
  }

  viewExistingRequests(): void {
    window.open(window.location.origin + `/viewExistingRequest`, "_self", "", false)
  }

  render() {
    return (
      <div className="padding">
        <h4>Brigade Captain</h4>
        <hr />
        <brigadeCaptainHome>
          <input type="text" placeholder="Request Title" title="Request Title" value={this.state.request_title}
            onChange={(e: any) => this.setState({ request_title: e.target.value })} />
          <button className="type-1" onClick={() => this.makeNewRequest()}>{this.state.allow_makeNewRequest ? "Make New Request" : "Loading"}</button>
        </brigadeCaptainHome>
        <hr />
        <brigadeCaptainHome>
          <button className="type-1" onClick={() => this.viewExistingRequests()}>Manage Existing Requests</button>
        </brigadeCaptainHome>
      </div>
    );
  }
}