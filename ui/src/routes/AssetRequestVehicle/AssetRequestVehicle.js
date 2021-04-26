import './AssetRequestVehicle.scss';

import axios from 'axios';
import React, {useEffect, useState} from 'react';
import {Button} from 'react-bootstrap';
import DatePicker from 'react-datepicker';
import {useHistory, useParams} from 'react-router';

import {toSentenceCase} from '../../common/functions';
import {backendPath} from '../../config';

function AssetRequestVehicle() {
    const [startDate, setStartDate] = useState(new Date());
    const [assetTypes, setAssetTypes] = useState([]);
    const [endDate, setEndDate] = useState(new Date());
    const [assetType, setAssetType] = useState('heavyTanker');
    const [vehicles, setVehicles] = useState([]);
    const {id} = useParams();
    const history = useHistory();

    useEffect(() => {
        axios
            .get(backendPath + 'reference/asset_types', {
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                },
            })
            .then((resp) => {
                setAssetTypes(resp.data);
            });
        axios
            .get(backendPath + 'vehicle/request', {
                params: {requestId: id},
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                },
            })
            .then((resp) => {
                let results = resp.data.results;
                let payloads = [];
                for (let asset of results) {
                    const payload = {
                        requestId: asset["ID"],
                        startDate: new Date(asset["From_Time"]),
                        endDate: new Date(asset["To_Time"]),
                        assetType: asset["Type"]
                    }
                    payloads.push(payload);
                }
                setVehicles([...vehicles, ...payloads]);
            })
    }, []);

    function insertAsset() {
        // Validate Data
        if (!startDate === undefined) {
            alert('Start DateTime has not been selected');
            return;
        } else if (endDate === undefined) {
            alert('End DateTime has not been selected');
            return;
        } else if (startDate < new Date()) {
            alert('Start DateTime has to be in the future');
            return;
        } else if (startDate >= endDate) {
            alert('Start DateTime has to be earlier than End DateTime');
            return;
        }
        const payload = {
            requestId: id,
            startDate: startDate,
            endDate: endDate,
            assetType: assetType,
        };
        axios
            .post(backendPath + 'vehicle/request', payload, {
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                },
            })
            .then((resp) => {
                payload['id'] = resp.data['id'];
                setVehicles([...vehicles, payload]);
            });
    }

    function submit() {
        if (vehicles.length === 0) {
            return;
        }
        axios
            .get(backendPath + 'recommendation', {
                params: {requestId: id},
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                },
            })
            .then(() => {
                history.push('/assetRequest/volunteers/' + id);
            });
    }

    function removeAsset(vehicleId) {
        const params = {
            requestId: id,
            vehicleId: vehicleId,
        };
        axios
            .delete(backendPath + 'vehicle/request', {
                params: params,
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                },
            })
            .then((resp) => {
                console.log(resp.data);
                let lcl = vehicles;
                lcl = lcl.filter((x) => x.id !== vehicleId);
                setVehicles(lcl);
            });
    }

    function saveRequest() {
        if (vehicles.length === 0) {
            deleteRequest();
            return;
        }
        window.open(window.location.origin + '/captain', 'self_', '', false)
    }

    function deleteRequest() {
        const params = {
            requestID: id,
        };
        const headers = {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        };
        axios
            .delete(backendPath + 'new_request', {params: params, headers: headers})
            .then(() => {
                window.open(window.location.origin + '/captain', 'self_', '', false);
            });
    }

    return (
        <asset-request-vehicle>
            <h4>New Asset Request</h4>
            <hr/>
            <div className="entry">
                <div className="con">
                    <label htmlFor={'assetType'}>Asset Type</label>
                    <select
                        id={'assetType'}
                        value={assetType}
                        onChange={(e) => {
                            setAssetType(e.target.value);
                        }}>
                        <option value="" disabled hidden>
                            Select asset type
                        </option>
                        {assetTypes.map((x) => {
                            return (
                                <option key={x.code} value={x.code}>
                                    {x.name}
                                </option>
                            );
                        })}
                    </select>
                </div>
                <div className="con">
                    <label htmlFor={'startDate'}>Start Time Date</label>
                    <DatePicker
                        id={'startDate'}
                        selected={startDate}
                        onChange={(i) => {
                            setStartDate(i);
                        }}
                        showTimeSelect
                        timeIntervals={30}
                        timeCaption="Time"
                        dateFormat="d MMMM yyyy h:mm aa"
                    />
                </div>
                <div className="con">
                    <label htmlFor={'endDate'}>End Time Date</label>
                    <DatePicker
                        id={'endDate'}
                        selected={endDate}
                        onChange={(e) => {
                            setEndDate(e);
                        }}
                        showTimeSelect
                        timeIntervals={30}
                        timeCaption="Time"
                        dateFormat="d MMMM yyyy h:mm aa"
                    />
                </div>
                <button className={'btn btn-success'} onClick={insertAsset}>
                    Add
                </button>
            </div>
            <hr className="thick"/>
            <div className="output">
                {vehicles.map((x) => {
                    return (
                        <request-body key={x.id}>
                            <svg
                                type="close"
                                viewBox="0 0 282 282"
                                onClick={() => removeAsset(x.id)}>
                                <g>
                                    <circle cx="141" cy="141" r="141"/>
                                    <ellipse cx="114" cy="114.5" rx="114" ry="114.5"/>
                                    <path
                                        d="M1536.374,2960.632,1582.005,2915l20.742,20.742-45.632,45.632,45.632,45.632-20.742,20.742-45.632-45.632-45.632,45.632L1470,3027.005l45.632-45.632L1470,2935.742,1490.742,2915Z"/>
                                </g>
                            </svg>
                            <h2>{toSentenceCase(x.assetType)}</h2>
                            <div className="cont-1">
                                <div className="cont-2">
                                    <span>Start</span>
                                    <br/>
                                    <div className="cont-3">
                                        {x.startDate.toLocaleDateString('en-GB', {
                                            day: 'numeric',
                                            month: 'long',
                                            year: 'numeric',
                                        })}
                                    </div>
                                    <div className="cont-3">
                                        {x.startDate.toLocaleTimeString('en-US', {
                                            hour: 'numeric',
                                            minute: 'numeric',
                                            hour12: true,
                                        })}
                                    </div>
                                </div>
                                <div className="cont-2">
                                    <span>End</span>
                                    <br/>
                                    <div className="cont-3">
                                        {x.endDate.toLocaleDateString('en-GB', {
                                            day: 'numeric',
                                            month: 'long',
                                            year: 'numeric',
                                        })}
                                    </div>
                                    <div className="cont-3">
                                        {x.endDate.toLocaleTimeString('en-US', {
                                            hour: 'numeric',
                                            minute: 'numeric',
                                            hour12: true,
                                        })}
                                    </div>
                                </div>
                            </div>
                        </request-body>
                    );
                })}
            </div>
            <hr className="thick"/>
            <Button className="type-1" onClick={submit}>
                Submit
            </Button>
            <Button className="type-3" onClick={saveRequest}>
                Save and Exit
            </Button>
            <Button className="type-2" onClick={deleteRequest}>
                Delete and Exit
            </Button>
        </asset-request-vehicle>
    );
}

export default AssetRequestVehicle;
