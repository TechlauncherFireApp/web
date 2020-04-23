import React, { Component } from 'react';
import './NewAssetRequest.scss';
import { contains } from '../main.js';
import Request from './components/Request.jsx';

class NewAssetRequest extends Component {

    state = {
        request_list: []
    };

    constructor(props) {
        super(props);
        this.insert_assetType = React.createRef();
        this.insert_startTime = React.createRef();
        this.insert_startDate = React.createRef();
        this.insert_endTime = React.createRef();
        this.insert_endDate = React.createRef();
        this.output = React.createRef();
    }

    insert_onClick = () => {
        console.clear();
        let a = {
            assetType: this.insert_assetType.current.value,
            startTime: this.insert_startTime.current.value,
            startDate: this.insert_startDate.current.value,
            endTime: this.insert_endTime.current.value,
            endDate: this.insert_endDate.current.value
        };
        // Validate Data
        for (let x in a) if (!contains(a[x])) { alert(x + " not entered"); return; }

        // Validated Successfully
        const o = this.state.request_list;
        o.push(a);
        this.setState({ request_list: o });
    }

    submit_onClick = () => {
        // Code Here
    }

    render() {
        return (
            <main-body>
                <div class="header-block">
                    <h1>New Asset Request</h1>
                </div>
                <container>
                    <entry>
                        <div>
                            <label>Asset Type</label>
                            <select ref={this.insert_assetType}>
                                <option value="" disabled hidden>Select asset type</option>
                                <option selected>Heavy Tanker</option>
                                <option>Light Unit</option>
                            </select>
                        </div>
                        <div>
                            <label>Start Time</label>
                            <input type="time" value="02:40" ref={this.insert_startTime}/>
                            <input type="date" value="2020-05-01" ref={this.insert_startDate}/>
                        </div>
                        <div>
                            <label>End Time</label>
                            <input type="time" value="15:40" ref={this.insert_endTime}/>
                            <input type="date" value="2020-06-02" ref={this.insert_endDate}/>
                        </div>
                        <insert onClick={this.insert_onClick}></insert>
                    </entry>
                    <hr></hr>
                    <output ref={this.output}>
                        { this.state.request_list.map((t) =>
                            <Request
                                assetType={t.assetType}
                                startTime={t.startTime}
                                startDate={t.startDate}
                                endTime={t.endTime}
                                endDate={t.endDate} />)
                        }
                    </output>
                    <hr></hr>
                    <button onClick={this.submit_onClick}>Submit Request</button>
                </container>
            </main-body>
        );
    }
}
export default NewAssetRequest;