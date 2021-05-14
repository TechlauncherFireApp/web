import axios from 'axios';
import React, { useEffect, useState } from 'react';

import { backendPath } from '../../config';
import Asset from './asset';

function AssetRequestVolunteers(props) {
  const [assetRequests, setAssetRequests] = useState([]);
  const [volunteers, setVolunteers] = useState([]);
  const [reload, setReload] = useState(0);

  useEffect(() => {
    axios
      .get(backendPath + 'shift/request?requestID=' + props.match.params.id)
      .then((resp) => {
        setAssetRequests(resp.data['results']);
      });
  }, [props.match.params.id, reload]);

  useEffect(() => {
    axios
      .get(backendPath + 'volunteer/all', {
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((resp) => {
        setVolunteers(resp.data['results']);
      });
  }, [reload]);

  return (
    <div className="padding">
      <h4>Asset Request</h4>
      <hr />
      {assetRequests.map((a) => (
        <Asset
          key={a.shiftID}
          asset={a}
          volunteerList={volunteers}
          onUpdate={() => {
            setReload((x) => x + 1);
          }}
        />
      ))}
    </div>
  );
}

export default AssetRequestVolunteers;
