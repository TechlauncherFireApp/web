import React from "react";
import "./Home.scss";
import axios, { AxiosResponse, AxiosError } from "axios";
import { contains } from "../functions";

interface State {
  request_title: string;
  allow_makeNewRequest: boolean;
}

export default class Home extends React.Component<any, State> {

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
      url: "NewAssetRequest",
      baseURL: "http://localhost:5000/",
      method: "POST",
      data: { "title": this.state.request_title },
      timeout: 15000,
      // withCredentials: true,
      headers: { "X-Requested-With": "XMLHttpRequest" }
    }).then((res: AxiosResponse): void => {
      if ((typeof res.data === "object") && contains(res.data["id"])) window.open(window.location.origin + `/assetRequest/${res.data["id"]}`, "_self", "", false);
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
      <React.Fragment>
        <home>
          <input type="text" placeholder="Title for the request" title="Title for the request" value={this.state.request_title}
            onChange={(e: any) => this.setState({ request_title: e.target.value })} />
          <button className="type-1" onClick={() => this.makeNewRequest()}>{this.state.allow_makeNewRequest ? "Make New Request" : "Loading"}</button>
        </home>
        <hr />
        <home>
          <button className="type-1" onClick={() => this.viewExistingRequests()}>View Existing Requests</button>
        </home>
      </React.Fragment>
    );
  }
}