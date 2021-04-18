import axios from 'axios';
import React, { useEffect, useState } from 'react';

import { backendPath } from '../../config';

function Roles() {
  const [roles, setRoles] = useState([]);
  const [refresh, setRefresh] = useState(0);
  const [newRoleName, setNewRoleName] = useState('');
  const [newRoleCode, setNewRoleCode] = useState('');
  const [error, setError] = useState(undefined);

  useEffect(() => {
    axios
      .get(backendPath + 'reference/roles', {
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((resp) => {
        setRoles(resp.data);
      });
  }, [refresh]);

  function addNew(e) {
    // Validate the new role name
    e.preventDefault();
    setError(undefined);
    if (newRoleCode === '') {
      setError('Role code is required.');
      return;
    }
    const existing = roles.filter((x) => x.code === newRoleCode);
    if (existing.length > 0) {
      setError('Role code must be unique.');
      return;
    }

    // Post the new role name and refresh the table
    axios
      .post(
        backendPath + 'reference/roles',
        { name: newRoleName, code: newRoleCode },
        {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        }
      )
      .then(() => {
        setNewRoleName('');
        setNewRoleCode('');
        setRefresh((x) => x + 1);
      });
  }

  function toggle(id) {
    axios
      .patch(
        backendPath + 'reference/roles',
        { id: id },
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
      <h2 className={'mb2'}>Volunteer Roles</h2>
      <hr />
      <h5>New volunteer role</h5>
      <form onSubmit={addNew}>
        <div className="form-group">
          <label htmlFor={'roleCode'}>Role code:</label>
          <input
            id={'roleCode'}
            className={'form-control w-third'}
            value={newRoleCode}
            type="text"
            name="code"
            onChange={(e) => {
              setNewRoleCode(e.target.value);
            }}
          />
        </div>
        <div className="form-group">
          <label htmlFor={'roleName'}>Role name:</label>
          <input
            id={'roleName'}
            className={'form-control w-third'}
            value={newRoleName}
            type="text"
            name="name"
            onChange={(e) => {
              setNewRoleName(e.target.value);
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
      <h5>Existing roles</h5>
      <table className="table">
        <thead>
          <tr>
            <th scope="col">Code</th>
            <th scope="col">Name</th>
            <th scope="col">Last Updated</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          {roles !== [] &&
            roles.map((x) => {
              return (
                <tr key={x['id']}>
                  <th scope="row">{x['code']}</th>
                  <td>{x['name']}</td>
                  <td>{x['updated']}</td>
                  <td>
                    <button
                      className={'btn btn-danger'}
                      onClick={() => {
                        toggle(x['id']);
                      }}>
                      {x['deleted'] === 'False' ? 'Disable' : 'Enable'}
                    </button>
                  </td>
                </tr>
              );
            })}
          {roles.length === 0 && (
            <tr key={'error'}>
              <th colSpan={2}>No roles currently defined.</th>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Roles;
