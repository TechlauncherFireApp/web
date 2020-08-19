import React from "react";
import "./NewAssetRequest.scss";
import axios, { AxiosResponse, AxiosError } from "axios";
import DatePicker from "react-datepicker"; // TYPESCRIPT -> npm i @types/react-datepicker
import { Button } from "react-bootstrap";
import { contains, toTimeblock, getValidDate } from "../functions";

// Local Types
interface RequestType {
  id: number;
  assetType: string;
  startDateTime: Date;
  endDateTime: Date;
}

// State Type
interface State {
  startDateTime: Date;
  endDateTime: Date;
  requestList: RequestType[];
}

export default class NewAssetRequest extends React.Component<any, State> {
  state: State = {
    startDateTime: getValidDate(new Date()),
    endDateTime: getValidDate(new Date()),
    requestList: [],
  };
  insert_assetType: React.RefObject<HTMLSelectElement>;

  constructor(props: any) {
    super(props);
    this.insert_assetType = React.createRef();
  }

  componentDidMount(): void {
    console.clear();
    // Assign Current Time
    let t1: Date = getValidDate(new Date()),
        t2: Date = getValidDate(new Date());

    t1.setMinutes(t1.getMinutes() + 30);
    t1 = getValidDate(t1);
    t2.setMinutes(t2.getMinutes() + 60);
    t2 = getValidDate(t2);

    this.setState({ startDateTime: t1, endDateTime: t2 });
  }

  processAssetRequest(): void {
    console.clear();
    /* This function needs to: 
            1. Pass the request list to the assetRequestContainer via this.state.updateRequestList
            2. convert this.state.requestList into the list that will be posted and expected by the backend [{id/type/timeblock/timeblock}] 
            3. pass that list to the backend
            4. receive the recommendation list from the backend 
            5. Pass the recommendation list to the assetRequestContainer via onDisplayRequest(list)
            */

    // 1.
    const requestList: RequestType[] = this.state.requestList;
    this.props.updateVehicleTimes(requestList);

    // 2.
    let postData: any = [];
    for (let x of requestList) {
      postData.push({
        "asset_id": x.id,
        "asset_name": x.assetType,
        "start_time": toTimeblock(x.startDateTime),
        "end_time": toTimeblock(x.endDateTime)
      });
    }

    // Don't get recommendations for no assets requested
    if (postData.length === 0) { alert("At least one asset needs to be selected"); return; }

    axios.request({
      url: "recommendation",
      baseURL: "http://localhost:5000/",
      method: "POST",
      data: { "asset_list": postData },
      timeout: 15000,
      withCredentials: true,
      headers: { "X-Requested-With": "XMLHttpRequest" }
    }).then((res: AxiosResponse): void => {
      this.props.onDisplayRequest(res.data.recommendation_list, res.data.volunteer_list);
    }).catch((err: AxiosError): void => {
      console.log(err);
    });
  }

  insertAsset(): void {
    // Get Data
    console.clear();

    const o: RequestType[] = this.state.requestList;
    let a: RequestType = {
      id: o.length + 1,
      assetType: this.insert_assetType.current ? this.insert_assetType.current.value : "",
      startDateTime: this.state.startDateTime,
      endDateTime: this.state.endDateTime,
    };

    // Validate Data :- Asset Type
    if (!contains(a.assetType)) { alert("Asset Type has not been selected"); return; }

    // Validate Data :- Start and End DateTime
    if (!contains(a.startDateTime)) { alert("Start DateTime has not been selected"); return; }
    else if (!contains(a.endDateTime)) { alert("End DateTime has not been selected"); return; }
    else if (a.startDateTime.valueOf() < (new Date()).valueOf()) { alert("Start DateTime has to be in the future"); return; }
    else if (a.startDateTime.valueOf() >= a.endDateTime.valueOf()) { alert("Start DateTime has to be earlier than End DateTime"); return; }

    // Detect same records --> for (let x of o) if (JSON.stringify(a) === JSON.stringify(x)) { alert("Same Record already exists"); return; }

    // Validated Successfully
    o.push(a);
    this.setState({ requestList: o });
  }

  removeAsset(i: number): void {
    console.clear();
    const o: RequestType[] = this.state.requestList;

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
  }

  setDateTime(v: Date, t: ("start" | "end")): void {
    console.clear();

    // Get & Check Value
    if (!contains(v)) return;

    // Modify Value
    v = getValidDate(v);

    // Set Value
    if (t === "start") this.setState({ startDateTime: v });
    else if (t === "end") this.setState({ endDateTime: v });
  }

  render() {
    return (
      <React.Fragment>
        {/* <h4 className="mt-2">New Asset Request</h4> */}
        <h1>New Asset Request</h1>
        <hr/>
        <div className="entry">
          <div className="con">
            <label>Asset Type</label>
            <select ref={this.insert_assetType}>
              <option value="" disabled hidden>Select asset type</option>
              <option selected>Heavy Tanker</option>
              <option>Light Unit</option>
            </select>
          </div>
          <div className="con">
            <label>Start Time Date</label>
            <DatePicker
              selected={this.state.startDateTime}
              onChange={(i: Date): void => { this.setDateTime(i, "start"); }}
              showTimeSelect
              timeIntervals={30}
              timeCaption="Time"
              dateFormat="d MMMM yyyy h:mm aa" />
          </div>
          <div className="con">
            <label>End Time Date</label>
            <DatePicker
              selected={this.state.endDateTime}
              onChange={(i: Date): void => { this.setDateTime(i, "end"); }}
              showTimeSelect
              timeIntervals={30}
              timeCaption="Time"
              dateFormat="d MMMM yyyy h:mm aa" />
          </div>
          <insert onClick={()=>this.insertAsset()}></insert>
        </div>
        <hr/>
        <div className="output">
          {this.state.requestList.map((t: any) => (
            <request-body id={t.id}>
                <svg type="close" viewBox="0 0 282 282" onClick={() => { this.removeAsset(t.id); }}> <g> <circle cx="141" cy="141" r="141"/> <ellipse cx="114" cy="114.5" rx="114" ry="114.5"/> <path d="M1536.374,2960.632,1582.005,2915l20.742,20.742-45.632,45.632,45.632,45.632-20.742,20.742-45.632-45.632-45.632,45.632L1470,3027.005l45.632-45.632L1470,2935.742,1490.742,2915Z"/> </g> </svg>
                <h2>{t.assetType}</h2>
                <div className="cont-1">
                    <div className="cont-2">
                        <label>Start</label>
                        <br/>
                        <div className="cont-3">{t.startDateTime.toLocaleDateString("en-GB",{day:"numeric",month:"long",year:"numeric"})}</div>
                        <div className="cont-3">{t.startDateTime.toLocaleTimeString("en-US",{hour:"numeric",minute:"numeric",hour12:true})}</div>
                    </div>
                    <div className="cont-2">
                        <label>End</label>
                        <br/>
                        <div className="cont-3">{t.endDateTime.toLocaleDateString("en-GB",{day:"numeric",month:"long",year:"numeric"})}</div>
                        <div className="cont-3">{t.endDateTime.toLocaleTimeString("en-US",{hour:"numeric",minute:"numeric",hour12:true})}</div>
                    </div>
                </div>
            </request-body>
          ))}
        </div>
        <hr/>
        {/* className="btn-med" */}
        <Button
          className="type-1"
          onClick={() => this.processAssetRequest()}
        >
          Submit Request
        </Button>
      </React.Fragment>
    );
  }
}