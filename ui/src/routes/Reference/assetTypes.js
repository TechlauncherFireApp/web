import axios from 'axios';
import React, { useEffect, useState } from 'react';

import { backendPath } from '../../config';

function AssetTypes() {
  const [assetTypes, setAssetTypes] = useState([]);
  const [refresh, setRefresh] = useState(0);
  const [newAssetTypeName, setNewAssetTypeName] = useState('');
  const [newAssetCodeName, setNewAssetCodeName] = useState('');
  const [error, setError] = useState(undefined);

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
  }, [refresh]);

  function addNew(e) {
    // Validate the new role name
    e.preventDefault();
    setError(undefined);
    if (newAssetTypeName === '' || newAssetCodeName === '') {
      setError('Asset type code and name are required.');
      return;
    }
    const existing = assetTypes.filter(
      (x) => x.name === newAssetTypeName || x.code === newAssetCodeName
    );
    if (existing.length > 0) {
      setError('Qualification name must be unique.');
      return;
    }

    // Post the new role name and refresh the table
    axios
      .post(
        backendPath + 'reference/asset_types',
        { name: newAssetTypeName, code: newAssetCodeName },
        {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        }
      )
      .then(() => {
        setNewAssetTypeName('');
        setNewAssetCodeName('');
        setRefresh((x) => x + 1);
      });
  }

  function toggle(assetCode) {
    axios
      .patch(
        backendPath + 'reference/asset_types',
        { code: assetCode },
        {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        }
      )
      .then(() => {
        setRefresh((x) => x + 1);
      });
  }

  return (
    <div className={'w-100 mt4 ba br b--black-10 pa3'}>
      <h2 className={'mb2'}>Asset Types</h2>
      <hr />
      <h5>New Asset Type</h5>
      <form onSubmit={addNew}>
        <div className="form-group">
          <label htmlFor={'assetCode'}>Asset code:</label>
          <input
            id={'assetCode'}
            className={'form-control w-third'}
            value={newAssetCodeName}
            type="text"
            name="code"
            onChange={(e) => {
              setNewAssetCodeName(e.target.value);
            }}
          />
        </div>
        <div className="form-group">
          <label htmlFor={'assetName'}>Asset name:</label>
          <input
            id={'assetName'}
            value={newAssetTypeName}
            className={'form-control w-third'}
            type="text"
            name="name"
            onChange={(e) => {
              setNewAssetTypeName(e.target.value);
            }}
          />
        </div>
        {error && <div className={'alert alert-danger'}>{error}</div>}
        <button
          type="submit"
          value="Submit"
          className={'btn bg-light-red pv1 ph2 br2 b near-white dim mv2'}>
          Submit
        </button>
      </form>
      <hr />
      <h5>Existing Asset Types</h5>
      <table className="table">
        <thead>
          <tr>
            <th scope="col">Asset Type Name</th>
            <th scope="col">Last Updated</th>
            <th scope="col">Enabled</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          {assetTypes !== [] &&
            assetTypes.map((x) => {
              return (
                <tr key={x['name']}>
                  <th scope="row">{x['name']}</th>
                  <td>{x['updated']}</td>
                  <td>{x['deleted'] === 'False' ? 'Yes' : 'No'}</td>
                  <td>
                    <button
                      className={'btn btn-danger'}
                      onClick={() => {
                        toggle(x['code']);
                      }}>
                      {x['deleted'] === 'False' ? 'Disable' : 'Enable'}
                    </button>
                  </td>
                </tr>
              );
            })}
          {assetTypes.length === 0 && (
            <tr key={'error'}>
              <th colSpan={2}>No asset types are currently defined.</th>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default AssetTypes;
