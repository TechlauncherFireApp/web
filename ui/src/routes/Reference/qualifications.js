import React, { useEffect, useState } from 'react';
import { backendPath } from '../../config';
import axios from 'axios';

function Qualifications() {
  const [qualifications, setQualifications] = useState([]);
  const [refresh, setRefresh] = useState(0);
  const [newQualificationName, setNewQualificationName] = useState('');
  const [error, setError] = useState(undefined);

  useEffect(() => {
    axios
      .get(backendPath + 'reference/qualifications', {
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((resp) => {
        setQualifications(resp.data);
      });
  }, [refresh]);

  function addNew(e) {
    // Validate the new role name
    e.preventDefault();
    setError(undefined);
    if (newQualificationName === '') {
      setError('Qualification name is required.');
      return;
    }
    const existing = qualifications.filter(
      (x) => x.name === newQualificationName
    );
    if (existing.length > 0) {
      setError('Qualification name must be unique.');
      return;
    }

    // Post the new role name and refresh the table
    axios
      .post(
        backendPath + 'reference/qualifications',
        { name: newQualificationName },
        {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        }
      )
      .then(() => {
        setNewQualificationName('');
        setRefresh((x) => x + 1);
      });
  }

  function toggle(roleName) {
    axios
      .patch(
        backendPath + 'reference/qualifications',
        { name: roleName },
        {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        }
      )
      .then((resp) => {
        setRefresh((x) => x + 1);
      });
  }

  return (
    <div className={'w-100 mt4 ba br b--black-10 pa3'}>
      <h2 className={'mb2'}>Volunteer Qualifications</h2>
      <hr />
      <h5>New volunteer qualification</h5>
      <form onSubmit={addNew}>
        <div className="form-group">
          <label>Qualification name:</label>
          <input
            className={'form-control w-third'}
            type="text"
            name="name"
            value={newQualificationName}
            onChange={(e) => {
              setNewQualificationName(e.target.value);
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
      <h5>Existing qualifications</h5>
      <table className="table">
        <thead>
          <tr>
            <th scope="col">Qualification Name</th>
            <th scope="col">Last Updated</th>
            <th scope="col">Enabled</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          {qualifications !== [] &&
            qualifications.map((x) => {
              return (
                <tr key={x['name']}>
                  <th scope="row">{x['name']}</th>
                  <td>{x['updated']}</td>
                  <td>{x['deleted'] === 'False' ? 'Yes' : 'No'}</td>
                  <td>
                    <button
                      className={'btn btn-danger'}
                      onClick={() => {
                        toggle(x['name']);
                      }}>
                      {x['deleted'] === 'False' ? 'Disable' : 'Enable'}
                    </button>
                  </td>
                </tr>
              );
            })}
          {qualifications.length === 0 && (
            <tr key={'error'}>
              <th colSpan={2}>No qualifications currently defined.</th>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Qualifications;
