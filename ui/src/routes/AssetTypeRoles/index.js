import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Form } from 'react-bootstrap';

import { backendPath } from '../../config';

function AssetTypeRoles() {
  const [assetTypes, setAssetTypes] = useState([]);
  const [selectedAssetType, setSelectedAssetType] = useState('');
  const [roleMapping, setRoleMapping] = useState([]);
  const [refresh, setRefresh] = useState(0);
  const [roles, setRoles] = useState([]);
  const [newRole, setNewRole] = useState('');
  const [config] = useState({
    headers: {
      Authorization: 'Bearer ' + localStorage.getItem('access_token'),
    },
  });

  useEffect(() => {
    axios
      .get(backendPath + 'reference/asset_types', config)
      .then((roleResp) => {
        const activeRoles = roleResp.data.filter(
          (x) => x['deleted'] === 'False'
        );
        setAssetTypes(activeRoles);
      });

    axios.get(backendPath + 'reference/roles', config).then((roleResp) => {
      const activeRoles = roleResp.data.filter((x) => x['deleted'] === 'False');
      setRoles(activeRoles);
    });
  }, [config]);

  useEffect(() => {
    if (selectedAssetType !== '') {
      axios
        .get(backendPath + 'asset-type-role', {
          ...config,
          params: { assetTypeId: selectedAssetType },
        })
        .then((resp) => {
          setRoleMapping(resp.data);
        });
    } else {
      setRoleMapping([]);
    }
  }, [selectedAssetType, config, refresh]);

  function remove(assetTypeRoleId) {
    axios
      .delete(backendPath + 'asset-type-role', {
        ...config,
        params: { assetTypeRoleId: assetTypeRoleId },
      })
      .then(() => {
        setRefresh((x) => x + 1);
      });
  }

  function save() {
    axios
      .post(
        backendPath + 'asset-type-role',
        { roleId: newRole, assetTypeId: selectedAssetType },
        config
      )
      .then(() => {
        setRefresh((x) => x + 1);
        setNewRole('');
      });
  }

  return (
    <div className={'w-100 mt4 ba br b--black-10 pa3'}>
      <h2 className={'mb2'}>Asset Planning</h2>
      <hr />
      <p>
        Use the form below to describe the role requirements for different
        assets.
      </p>
      <p>
        This information is used in scheduling to match volunteers with role
        capabilities to asset roles in your organisation.
      </p>
      <p>
        Note: Any changes made to role requirements will only take effect for
        future scheduling events. Existing events will not be changed.
      </p>
      <hr />
      <Form.Row>
        <Form.Label className={'col-lg-4 pt-1'}>
          Select an asset type to define role requirements
        </Form.Label>
        <Form.Control
          className={'col-lg-4'}
          as="select"
          value={selectedAssetType}
          onChange={(e) => {
            setSelectedAssetType(e.target.value);
          }}>
          <option value={''} />
          {assetTypes.map((x) => (
            <option key={x['id']} value={x['id']}>
              {x['name']}
            </option>
          ))}
        </Form.Control>
      </Form.Row>
      <hr />
      {selectedAssetType !== '' && (
        <div>
          <p>
            Role mapping for assets of type{' '}
            <span className={'b'}>
              {
                assetTypes.find((x) => `${x['id']}` === selectedAssetType)[
                  'name'
                ]
              }
              :
            </span>
          </p>
          {roleMapping.map((roleMap) => {
            return (
              <div
                key={roleMap['assetTypeRoleId']}
                className={'w-100 flex flex-row pv2'}>
                <div className={'w-25 b'}>
                  <span>Seat #{roleMap['seatNumber']}</span>:
                </div>
                <div className={'w-25'}>
                  <span>{roleMap['roleName']}</span>
                </div>
                <div className={'w-25'}>
                  <button
                    className={'btn btn-danger ml-2'}
                    onClick={() => {
                      remove(roleMap['assetTypeRoleId']);
                    }}>
                    Remove
                  </button>
                </div>
              </div>
            );
          })}
          <div className={'w-100 flex flex-row pv2'}>
            <div className={'w-25 b'}>
              <span>New role</span>:
            </div>
            <div className={'w-25'}>
              <Form.Control
                as="select"
                value={newRole}
                onChange={(e) => {
                  setNewRole(e.target.value);
                }}>
                <option value={''} />
                {roles.map((x) => (
                  <option key={x['id']} value={x['id']}>
                    {x['name']}
                  </option>
                ))}
              </Form.Control>
            </div>
            <div className={'w-25'}>
              <button
                className={'btn btn-primary ml-2'}
                onClick={() => {
                  save();
                }}>
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AssetTypeRoles;
