import React, { useEffect, useState } from 'react';
import './brigadeCaptainHome.scss';
import axios from 'axios';
import { NavLink, useHistory } from 'react-router-dom';

function BrigadeCaptainHome() {
  const [requests, setRequests] = useState([]);
  const [newRequestTitle, setRequestTitle] = useState(null);
  const history = useHistory();

  useEffect(() => {
    axios
      .get('/existing_requests', {
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((resp) => {
        setRequests(resp.data.results);
      });
  }, []);

  function addNew(e) {
    e.preventDefault();
    axios
      .post(
        '/new_request',
        { title: newRequestTitle },
        {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        }
      )
      .then((resp) => {
        history.push('/assetRequest/vehicles/' + resp.data.id);
      });
  }

  return (
    <div className={'w-100 mt4 ba br b--black-10 pa3'}>
      <h2 className={'mb2'}>Request Administration</h2>
      <hr />
      <h5>New request</h5>
      <form onSubmit={addNew}>
        <div className="form-group">
          <label>Request Name:</label>
          <input
            className={'form-control w-third'}
            type="text"
            name="name"
            onChange={(e) => {
              setRequestTitle(e.target.value);
            }}
          />
        </div>
        <button
          type="submit"
          value="Submit"
          className={'btn bg-light-red pv1 ph2 br2 b near-white dim mv2'}>
          Submit
        </button>
      </form>
      <hr />
      <h5>Existing requests</h5>
      <table className="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Title</th>
            <th scope="col">Status</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((x) => {
            return (
              <tr key={x.id}>
                <th scope="row">{x.id}</th>
                <td>{x.title}</td>
                <td>{x.status}</td>
                <td>
                  <NavLink to={'/assetRequest/volunteers/' + x.id}>
                    View
                  </NavLink>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default BrigadeCaptainHome;
