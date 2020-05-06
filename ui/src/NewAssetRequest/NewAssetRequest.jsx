import React, { Component } from "react";
import "./NewAssetRequest.scss";
import { contains, getDateSS } from "../main.js";
import Request from "./components/Request";

// https://xd.adobe.com/view/2856aec3-f800-48bc-5922-bdfc629bf833-5e67/?fullscreen

class NewAssetRequest extends Component {
  state = {
    request_list: [
      // { id:1,assetType:"Heavy Tanker",startDateTime:new Date("2020-04-28T17:50"),endDateTime:new Date("2020-05-01T14:50") }
    ],
    // Dummy list used to test recommendation UI without running the backend 
    volunteer_list: [
      {
        asset_id: 1,
        asset_class: "Medium Unit",
        volunteers: [
          {
            volunteer_id: 5123,
            position_id: 1,
            volunteer_name: "Joe Blob",
            role: "Driver",
            qualifications: [
              "heavy rigid license",
              "pump training",
              "crew leader training",
              "advanced training",
            ],
            contact_info: [{ detail: "0412 490 340" }],
          },
          {
            volunteer_id: 649,
            position_id: 2,
            volunteer_name: "Jane Doe",
            role: "Advanced",
            qualifications: ["advanced training", "crew leader training"],
            contact_info: [{ detail: "0412 490 340" }],
          },
        ],
      },
      {
        asset_id: 2,
        asset_class: "Light Unit",
        volunteers: [
          {
            volunteer_id: 5123,
            position_id: 1,
            volunteer_name: "Mary Blank",
            role: "Driver",
            qualifications: [
              "heavy rigid license",
              "pump training",
              "crew leader training",
              "advanced training",
            ],
            contact_info: [{ detail: "0412 490 340" }],
          },
          {
            volunteer_id: 649,
            position_id: 2,
            volunteer_name: "John Connor",
            role: "Advanced",
            qualifications: ["advanced training", "crew leader training"],
            contact_info: [{ detail: "0412 490 340" }],
          },
        ],
      },
    ],
  };

  constructor(props) {
    super(props);
    this.insert_assetType = React.createRef();
    this.insert_startDateTime = React.createRef();
    this.insert_endDateTime = React.createRef();
    this.output = React.createRef();
  }

  processAssetRequest = () => {
    console.clear();
    /* This function needs to: 
            1. Pass the request list to the assetRequestContainer via this.state.updateRequestList
            2. convert this.state.request_list into the list that will be posted and expected by the backend [{id/type/timeblock/timeblock}] 
            3. pass that list to the backend
            4. receive the recommendation list from the backend 
            5. Pass the recommendation list to the assetRequestContainer via onDisplayRequest(list)
            */

    // 1.
    const request_list = this.state.request_list;
    this.props.updateVehicleTimes(request_list);

    // 2.
    let postData = [];                                      // [ { assetId: int, assetClass: String, startTime: int, endTime: int } ]
    for (let x of request_list) {
      postData.push({
        "asset_id": x.id,
        "asset_name": x.assetType,
        "start_time": this.toTimeblock(x.startDateTime),
        "end_time": this.toTimeblock(x.endDateTime)
      });
    }

    // Don't get recommendations for no assets requested
    if (postData.length === 0) {
      console.log(postData.length)
      return false;
    }

    // 3. TODO
    let asset_list = { "asset_list": postData }

    const axios = require('axios');
    axios.post(`http://localhost:5000/recommendation`, asset_list)

      // 4. response.data.volunteer_list
      // 5.
      .then(response => this.props.onDisplayRequest(response.data.volunteer_list))
      .catch(function (error) {
        // handle error
        console.log(error);
      })
  };

  dummyProcessAssetRequest = () => {
    console.clear();
    /* A dummy function to display the recommendation screen using dummy data, so we can test without running the backend */
    // 1.
    const request_list = this.state.request_list;
    this.props.updateVehicleTimes(request_list);
    // 2.
    // 3.
    // 4.
    let list = this.state.volunteer_list;                   //should be the list returned by the backend, using dummy list for now
    // 5.
    this.props.onDisplayRequest(list);
  };


  toTimeblock = (d) => {
    if (!contains(d) || d === "Invalid Date") return 0;
    return d.getDay() * 48 + d.getHours() * 2 + (d.getMinutes() === 0 ? 0 : 1);
  };

  insertAsset = () => {
    // Get Data
    console.clear();
    const o = this.state.request_list;
    let a = {
      id: o.length + 1,
      assetType: this.insert_assetType.current.value,
      startDateTime: new Date(this.insert_startDateTime.current.value),
      endDateTime: new Date(this.insert_endDateTime.current.value),
    };

    // Validate Data
    for (let x in a)
      if (!contains(a[x]) || a[x] === "Invalid Date") {
        alert(x + " not entered");
        return;
      }

    // Detect same records --> for (let x of o) if (JSON.stringify(a) === JSON.stringify(x)) { alert("Same Record already exists"); return; }

    // Check Start and End DateTime Range
    if (a.startDateTime >= a.endDateTime) { alert("Start DateTime has to be earlier than End DateTime"); return; }

    // Validated Successfully
    o.push(a);
    this.setState({ request_list: o });
  };

  removeAsset = (i) => {
    console.clear();
    const o = this.state.request_list;

    // Find and Remove Element, then update id
    for (let y = 0; y < o.length; y++) {
      if (o[y].id === i) {
        o.splice(y, 1);
        // Update id
        for (let x = 0; x < o.length; x++) o[x].id = x + 1;
      }
    }

    // Update Data
    this.setState({ request_list: o });
  };

  submitData = () => {
    // Get Data
    console.clear();
    const o = this.state.request_list;

    // Validate Data
    if (o.length === 0) {
      alert("At least one asset needs to be selected");
      return;
    }

    // Validated Successfully
    console.log(o);
  };

  validateDateTimeInput = (e) => {
    console.clear();
    e = e.target;

    // Get & Check Value
    let v = new Date(e.value);
    if (!contains(v) || v === "Invalid Date") return;

    // Check Start and End Input Range --> if (e.getAttribute("name") === "start") { let v2 = new Date(this.insert_endDateTime.current.value); if (contains(v2) && v2 != "Invalid Date" && v >= v2) { v = v2; v.setMinutes(v.getMinutes() - 30); } } else { let v2 = new Date(this.insert_startDateTime.current.value); if (contains(v2) && v2 != "Invalid Date" && v <= v2) { v = v2; v.setMinutes(v.getMinutes() + 30); } }

    // Modify Value
    v.setSeconds(0);
    v.setMinutes(v.getMinutes() >= 30 ? 30 : 0);
    v = getDateSS(v);

    // Set Value
    e.value = v;
  };

  componentDidMount = () => {
    // Assign Current Time
    let t = new Date();
    t.setSeconds(0);
    t.setMinutes(t.getMinutes() >= 30 ? 30 : 0);
    this.insert_startDateTime.current.value = getDateSS(t);
    t.setMinutes(t.getMinutes() + 30);
    this.insert_endDateTime.current.value = getDateSS(t);
  };

  render() {
    return (
      <main-body>
        <h4 className="mt-2">New Asset Request</h4>
        <hr />
        <container>
          <entry>
            <div>
              <label>Asset Type</label>
              <select ref={this.insert_assetType}>
                <option value="" disabled hidden>
                  Select asset type
                </option>
                <option selected>Heavy Tanker</option>
                <option>Light Unit</option>
              </select>
            </div>
            <div>
              <label>Start Time Date</label>
              <input
                type="datetime-local"
                onChange={this.validateDateTimeInput}
                name="start"
                ref={this.insert_startDateTime}
              />
            </div>
            <div>
              <label>End Time Date</label>
              <input
                type="datetime-local"
                onChange={this.validateDateTimeInput}
                name="end"
                ref={this.insert_endDateTime}
              />
            </div>
            <insert onClick={this.insertAsset}></insert>
          </entry>
          <hr></hr>
          <output ref={this.output}>
            {this.state.request_list.map((t) => (
              <Request
                id={t.id}
                assetType={t.assetType}
                startDateTime={t.startDateTime}
                endDateTime={t.endDateTime}
                removeAsset={this.removeAsset}
              />
            ))}
          </output>
          <hr></hr>
          <button
            className="type-1"
            onClick={() => this.processAssetRequest()}
          >
            Submit Request
          </button>
          {/* BELOW IS A TESTING BUTTON */}
          <button onClick={() => this.dummyProcessAssetRequest()}>Go to recommendation screen with dummy data</button>
        </container>
      </main-body>
    );
  }
}
export default NewAssetRequest;
