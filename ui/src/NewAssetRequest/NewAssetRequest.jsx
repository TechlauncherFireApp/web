import React, { Component } from 'react';
import './NewAssetRequest.scss';
import { contains } from '../main.js';
import Request from './components/Request';

// https://xd.adobe.com/view/2856aec3-f800-48bc-5922-bdfc629bf833-5e67/?fullscreen

class NewAssetRequest extends Component {

    state = {
        request_list: [
            // {assetType:"Heavy Tanker",startDateTime:new Date("2020-04-28T17:50"),endDateTime:new Date("2020-05-01T14:50")}
        ],
        dummyList: ["testing", "list", "of", "stuff"]
    };

    constructor(props) {
        super(props);
        this.insert_assetType = React.createRef();
        this.insert_startDateTime = React.createRef();
        this.insert_endDateTime = React.createRef();
        this.output = React.createRef();
    }

    Insert_Asset = () => {
        // Get Data
        console.clear();
        let a = {
            assetType : this.insert_assetType.current.value,
            startDateTime : new Date(this.insert_startDateTime.current.value),
            endDateTime : new Date(this.insert_endDateTime.current.value)
        };

        // Validate Data
        for (let x in a) if (!contains(a[x]) || (a[x] == "Invalid Date")) { alert(x + " not entered"); return; }
        const o = this.state.request_list;
        for (let x of o) if (JSON.stringify(a) === JSON.stringify(x)) { alert("Same Record already exists"); return; }

        // Validated Successfully
        o.push(a);
        this.setState({ request_list: o });
    }

    Remove_Asset = (e) => {
        console.clear();
        const o = this.state.request_list;
        
        // Find Element
        for (let x in o) {
            let s = JSON.stringify(o[x]);
            if (contains(s) && (s === e)) delete o[x];
        }

        // Update Data
        this.setState({ request_list: o });
    }

    submit_onClick = () => {
        // Get Data
        console.clear();
        const o = this.state.request_list;

        // Validate Data
        if (o.length === 0) { alert("At least one asset needs to be selected"); return; }

        // Validated Successfully
        console.log(o);
    }

    render() {
        return (
            <main-body>
                <h1>New Asset Request</h1>
                <hr/>
                <container>
                    <entry>
                        <div>
                            <label>Asset Type</label>
                            <select ref={this.insert_assetType}>
                                <option value="" selected disabled hidden>Select asset type</option>
                                <option >Heavy Tanker</option>
                                <option>Light Unit</option>
                            </select>
                        </div>
                        <div>
                            <label>Start Time Date</label>
                            <input type="datetime-local" ref={this.insert_startDateTime}/>
                        </div>
                        <div>
                            <label>End Time Date</label>
                            <input type="datetime-local" ref={this.insert_endDateTime}/>
                        </div>
                        <insert onClick={this.Insert_Asset}></insert>
                    </entry>
                    <hr></hr>
                    <output ref={this.output}>
                        { this.state.request_list.map((t) =>
                            <Request
                                assetType={t.assetType}
                                startDateTime={t.startDateTime}
                                endDateTime={t.endDateTime}
                                Remove_Asset={this.Remove_Asset} />)
                        }
                    </output>
                    <hr></hr>
                    {/* AMAN CHANGE : onClick={this.submit_onClick} */}
                    <button className="type-1" onClick={() => this.props.onDisplayRequest(this.state.dummyList)}>
                        {/* this button will need to call the backend function to generate
                          a recommendation, and then pass the list returned from the backend 
                          to the assetRequestContainer via the onDisplayRequest function (as
                          done above with a dummy list I insterted into the state)*/}
                        Submit Request
                    </button>
                </container>
            </main-body>
        );
    }
}
export default NewAssetRequest;