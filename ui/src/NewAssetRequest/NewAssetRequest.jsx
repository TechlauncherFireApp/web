// import PropTypes from "prop-types";
import React, { Component } from "react";
import "./NewAssetRequest.scss";
import { contains } from "../main.js";

import "react-datepicker/dist/react-datepicker.css";
import DatePicker from "react-datepicker";              // -> PACKAGE FROM : npm i --save react-datepicker
import { Button } from "react-bootstrap";

/*
  User Story Map references (Ctrl + F the following reference numbers to find associated code)
*/

// https://xd.adobe.com/view/2856aec3-f800-48bc-5922-bdfc629bf833-5e67/?fullscreen
class NewAssetRequest extends Component {
  state = {
    startDateTime: null,
    endDateTime: null,
    requestList: [
      { id: 1, assetType: "Heavy Tanker", startDateTime: new Date("2020-10-28T17:00"), endDateTime: new Date("2020-12-01T14:30") },
    ],
    // Dummy list used to test recommendation UI without running the backend 
    dummy_list: [
      {
        asset_id: 1,
        asset_class: "Light Unit",
        volunteers: [
          {
            volunteer_id: 10,
            position_id: 1,
            volunteer_name: "eg a",
            role: "Driver",
            possibleRoles: ["Driver", "CrewLeader", "Crew Member",],
            qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
            contact_info: [{ detail: "0412 490 340" }],
          },
          {
            volunteer_id: 20,
            position_id: 2,
            volunteer_name: "eg b",
            role: "CrewLeader",
            possibleRoles: ["CrewLeader", "Crew Member",],
            qualifications: ["advanced training", "crew leader training"],
            contact_info: [{ detail: "0412 490 340" }],
          },]
      }
    ],

    volunteer_list: [
      {
        id: 10,
        name: "eg a",
        role: null,
        possibleRoles: ["Driver", "CrewLeader", "Crew Member",],
        qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
        contact_info: [{ detail: "0412 490 340" }],
      }, {
        id: 20,
        name: "eg b",
        role: null,
        possibleRoles: ["CrewLeader", "Crew Member",],
        qualifications: ["advanced training", "crew leader training"],
        contact_info: [{ detail: "0412 490 340" }],
      }, {
        id: 110,
        name: "person one",
        role: null,
        possibleRoles: ["Driver", "CrewLeader", "Crew Member",],
        qualifications: ["heavy rigid license", "pump training", "crew leader training", "advanced training",],
        contact_info: [{ detail: "0412 490 340" }],
      }, {
        id: 111,
        name: "person two",
        role: null,
        possibleRoles: ["CrewLeader", "Crew Member",],
        qualifications: ["crew leader training", "advanced training",],
        contact_info: [{ detail: "0412 490 340" }],
      }, {
        id: 112,
        name: "person three",
        role: null,
        possibleRoles: ["Crew Member",],
        qualifications: ["advanced training",],
        contact_info: [{ detail: "0412 490 340" }],
      }, {
        id: 113,
        name: "person four",
        role: null,
        possibleRoles: ["Driver", "Crew Member",],
        qualifications: ["heavy rigid license", "pump training", "advanced training",],
        contact_info: [{ detail: "0412 490 340" }],
      }, {
        id: 114,
        name: "person five",
        role: null,
        possibleRoles: ["Crew Member",],
        qualifications: ["advanced training",],
        contact_info: [{ detail: "0412 490 340" }],
      }, {
        id: 115,
        name: "person six",
        role: null,
        possibleRoles: ["Crew Member",],
        qualifications: [],
        contact_info: [{ detail: "0412 490 340" }],
      }, {
        id: 116,
        name: "person seven",
        role: null,
        possibleRoles: ["CrewLeader", "Crew Member",],
        qualifications: ["crew leader training", "advanced training",],
        contact_info: [{ detail: "0412 490 340" }],
      },
    ],

  };

  constructor(props) {
    super(props);
    this.insert_assetType = React.createRef();
  }

  processAssetRequest = () => {
    console.clear();
    /* This function needs to: 
            1. Pass the request list to the assetRequestContainer via this.state.updateRequestList
            2. convert this.state.requestList into the list that will be posted and expected by the backend [{id/type/timeblock/timeblock}] 
            3. pass that list to the backend
            4. receive the recommendation list from the backend 
            5. Pass the recommendation list to the assetRequestContainer via onDisplayRequest(list)
            */

    // 1.
    const requestList = this.state.requestList;
    this.props.updateVehicleTimes(requestList);

    // 2.
    let postData = [];                                      // [ { assetId: int, assetClass: String, startTime: int, endTime: int } ]
    for (let x of requestList) {
      postData.push({
        "asset_id": x.id,
        "asset_name": x.assetType,
        "start_time": this.toTimeblock(x.startDateTime),
        "end_time": this.toTimeblock(x.endDateTime)
      });
    }

    // Don't get recommendations for no assets requested
    if (postData.length === 0) {
      alert("At least one asset needs to be selected");
      return false;
    }

    // 3.
    postData = { "asset_list": postData }

    const axios = require('axios');
    axios.post('http://localhost:5000/recommendation', postData)

      // 4.
      //  response.data.recommendation_list is the list of assets with volunteer recommendations
      //  response.data.volunteer_list is a list of all volunteers and all their stored data
      // 5.

      .then(response => this.props.onDisplayRequest(response.data.recommendation_list, response.data.volunteer_list))
      .catch(function (error) {
        // handle error
        console.log(error);
      })
  };

  toTimeblock = (d) => {
    if (!contains(d) || d === "Invalid Date") return 0;
    return d.getDay() * 48 + d.getHours() * 2 + (d.getMinutes() === 0 ? 0 : 1);
  };

  insertAsset = () => {
    // Get Data
    console.clear();
    const o = this.state.requestList;
    let a = {
      id: o.length + 1,
      assetType: this.insert_assetType.current.value,
      startDateTime: new Date(this.state.startDateTime),
      endDateTime: new Date(this.state.endDateTime),
    };

    // Validate Data
    for (let x in a)
      if (!contains(a[x]) || a[x] === "Invalid Date") {
        alert(x + " not entered");
        return;
      }

    // Detect same records --> for (let x of o) if (JSON.stringify(a) === JSON.stringify(x)) { alert("Same Record already exists"); return; }

    // Check Start and End DateTime Range
    if (a.startDateTime.valueOf() < (new Date()).valueOf()) { alert("Start DateTime has to be in the future"); return; }
    if (a.startDateTime.valueOf() >= a.endDateTime.valueOf()) { alert("Start DateTime has to be earlier than End DateTime"); return; }

    // Check Shift Length
    if ((Math.abs(a.startDateTime - a.endDateTime) / 3600000) > 14) alert("This request exceeds the maximum shift length, consider breaking down into multiple shifts");

    // Validated Successfully
    o.push(a);
    this.setState({ requestList: o });
  };

  removeAsset = (i) => {
    console.clear();
    const o = this.state.requestList;

    // Find and Remove Element, then update id
    for (let y = 0; y < o.length; y++) {
      if (o[y].id === i) {
        o.splice(y, 1);
        // Update id
        for (let x = 0; x < o.length; x++) o[x].id = x + 1;
        break;
      }
    }

    // Update Data
    this.setState({ requestList: o });
  };

  componentDidMount = () => {
    console.clear();
    // Assign Current Time
    let t1 = new Date(),
      t2 = new Date();
    t1.setSeconds(0);
    t2.setSeconds(0);
    t1.setMinutes(t1.getMinutes() + 30);
    t1.setMinutes(t1.getMinutes() >= 30 ? 30 : 0);
    t2.setMinutes(t2.getMinutes() + 60);
    t2.setMinutes(t2.getMinutes() >= 30 ? 30 : 0);

    this.setState({ startDateTime: t1, endDateTime: t2 });
  };

  setDateTime = (v, t) => {
    console.clear();
    v = new Date(v);

    // Get & Check Value
    if (!contains(v) || v === "Invalid Date") return;

    // Modify Value
    v.setSeconds(0);
    v.setMinutes(v.getMinutes() >= 30 ? 30 : 0);

    // Set Value
    if (t === "start") this.setState({ startDateTime: v });
    else if (t === "end") this.setState({ endDateTime: v });
  };

  testFunction = () => {
    this.props.updateVehicleTimes(this.state.requestList);
    this.props.onDisplayRequest(this.state.dummy_list, this.state.volunteer_list);
  }

  render() {
    return (
      <React.Fragment>
        {/* <h4 className="mt-2">New Asset Request</h4> */}
        <h1>New Asset Request</h1>
        <hr />
        <div className="entry">
          <div className="con">
            {/* 1.2.1 I want to select the asset types required (two asset types) */}
            <label>Asset Type</label>
            <select ref={this.insert_assetType}>
              <option selected value="" disabled hidden>Select asset type</option>
              <option>Heavy Tanker</option>
              <option>Light Unit</option>
            </select>
          </div>
          {/* 1.2.2 I want to select the time frame each asset is required for */}
          <div className="con">
            <label>Start Time Date</label>
            <DatePicker
              selected={this.state.startDateTime}
              onChange={(i) => { this.setDateTime(i, "start"); }}
              showTimeSelect
              timeIntervals={30}
              timeCaption="Time"
              dateFormat="d MMMM yyyy h:mm aa" />
          </div>
          <div className="con">
            <label>End Time Date</label>
            <DatePicker
              selected={this.state.endDateTime}
              onChange={(i) => { this.setDateTime(i, "end"); }}
              showTimeSelect
              timeIntervals={30}
              timeCaption="Time"
              dateFormat="d MMMM yyyy h:mm aa" />
          </div>
          <insert onClick={this.insertAsset}></insert>
        </div>
        <hr />
        <div className="output">
          {this.state.requestList.map((t) => (
            <request-body id={t.id}>
              <img className="close" src={require("../assets/x.png")} onClick={() => { this.removeAsset(t.id); }} />
              <h2>{t.assetType}</h2>
              <div className="cont-1">
                <div className="cont-2">
                  <label>Start</label>
                  <br />
                  <div className="cont-3">{t.startDateTime.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}</div>
                  <div className="cont-3">{t.startDateTime.toLocaleTimeString("en-US", { hour: "numeric", minute: "numeric", hour12: true })}</div>
                </div>
                <div className="cont-2">
                  <label>End</label>
                  <br />
                  <div className="cont-3">{t.endDateTime.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}</div>
                  <div className="cont-3">{t.endDateTime.toLocaleTimeString("en-US", { hour: "numeric", minute: "numeric", hour12: true })}</div>
                </div>
              </div>
            </request-body>
          ))}
        </div>
        <hr />
        {/* className="btn-med" */}
        <Button
          className="type-1"
          onClick={() => this.processAssetRequest()}
        >
          Submit Request
        </Button>

        <Button
          className="type-1"
          onClick={() => this.testFunction()}>Run with hard coded test data</Button>
      </React.Fragment>
    );
  }
}
export default NewAssetRequest;
