import React, { Component } from "react";
import axios, { AxiosResponse, AxiosError } from "axios";

interface AssetRequest {
  id: string;
  title: string;
}

interface State {
  requests: AssetRequest[];
  selectedRequest?: AssetRequest;
}

export default class existingRequestSelector extends React.Component<any, State> {

  state: State = {
    requests: [],
    selectedRequest: undefined
  };
  select_request: React.RefObject<HTMLSelectElement>;

  constructor(props: any) {
    super(props);
    this.select_request = React.createRef();
  }

  componentDidMount(): void {
    let l: AssetRequest[] = [];
    axios.request({
      url: "existing_requests",
      baseURL: "http://localhost:5000/",
      method: "GET",
      timeout: 15000,
      // withCredentials: true,
      headers: { "X-Requested-With": "XMLHttpRequest" }
    }).then((res: AxiosResponse): void => {
      l = res.data["results"];

      console.log("Data from backend returned:")
      console.log(l);

      this.setState({ requests: l })
    }).catch((err: AxiosError): void => {
      alert(err.message);
    });
  }

  selectRequest = (): void => {
    let selectedID: string = this.select_request.current ? this.select_request.current.value : "";

    let v: (AssetRequest | undefined) = undefined;
    for (let i = 0; i < this.state.requests.length; i++) {
      if (this.state.requests[i].id === selectedID) {
        v = this.state.requests[i];
        i = this.state.requests.length;
      }
    }
    this.setState({ selectedRequest: v }, () => { this.loadRequest() });
  }

  loadRequest = (): void => {
    if (this.state.selectedRequest === undefined) {
      console.log("no request selected");
    } else {
      window.open(window.location.origin + `/assetRequest/volunteers/${this.state.selectedRequest.id}`, "_self", "", false);
    }
  }

  render() {
    return (
      <div className="padding">
        <h4>Saved Requests</h4>
        <hr />
        <p>Select a saved request to see further information.</p>
        <select ref={this.select_request}>
          <option value="" hidden selected>Select saved request</option>
          {this.state.requests.map((v: AssetRequest) =>
            <option value={v.id}>{v.title}</option>
          )}
        </select>
        <button className="type-1 margin" onClick={() => this.selectRequest()}>View Assignment</button>
      </div>
    );
  }
}