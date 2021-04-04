import './AssetRequestVehicle.scss';
import React, { useEffect, useState } from 'react';
import { useHistory, useParams } from 'react-router';
import DatePicker from 'react-datepicker';
import { toSentenceCase } from '../../common/functions';
import { Button } from 'react-bootstrap';
import { backendPath } from '../../config';
import axios from 'axios';

function AssetRequestVehicle() {
  const [startDate, setStartDate] = useState(new Date());
  const [assetTypes, setAssetTypes] = useState([]);
  const [endDate, setEndDate] = useState(new Date());
  const [assetType, setAssetType] = useState('heavyTanker');
  const [vehicles, setVehicles] = useState([]);
  const { id } = useParams();
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
    // Submit Request
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
        params: { requestId: id },
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((resp) => {
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
        let lcl = vehicles;
        lcl = lcl.filter((x) => x.id !== vehicleId);
        setVehicles(lcl);
      });
  }

  function cancelRequest() {
    const params = {
      requestID: id,
    };
    const headers = {
      Authorization: 'Bearer ' + localStorage.getItem('access_token'),
    };
    axios
      .delete(backendPath + 'new_request', { params: params, headers: headers })
      .then((resp) => {
        window.open(window.location.origin + '/captain', 'self_', '', false);
      });
  }

  return (
    <asset-request-vehicle>
      <h4>New Asset Request</h4>
      <hr />
      <div className="entry">
        <div className="con">
          <label>Asset Type</label>
          <select
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
          <label>Start Time Date</label>
          <DatePicker
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
          <label>End Time Date</label>
          <DatePicker
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
      <hr className="thick" />
      <div className="output">
        {vehicles.map((x) => {
          return (
            <request-body key={x.id}>
              <svg
                type="close"
                viewBox="0 0 282 282"
                onClick={() => removeAsset(x.id)}>
                <g>
                  <circle cx="141" cy="141" r="141" />
                  <ellipse cx="114" cy="114.5" rx="114" ry="114.5" />
                  <path d="M1536.374,2960.632,1582.005,2915l20.742,20.742-45.632,45.632,45.632,45.632-20.742,20.742-45.632-45.632-45.632,45.632L1470,3027.005l45.632-45.632L1470,2935.742,1490.742,2915Z" />
                </g>
              </svg>
              <h2>{toSentenceCase(x.assetType)}</h2>
              <div className="cont-1">
                <div className="cont-2">
                  <label>Start</label>
                  <br />
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
                  <label>End</label>
                  <br />
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
      <hr className="thick" />
      <Button className="type-1" onClick={submit}>
        Submit
      </Button>
      <Button className="type-2" onClick={cancelRequest}>
        Cancel
      </Button>
    </asset-request-vehicle>
  );
}

export default AssetRequestVehicle;
