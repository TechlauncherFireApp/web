import axios from 'axios';
import React, {useEffect, useState} from 'react';

import {backendPath} from "../../config";

// import { backendPath } from '../../config';

function UserPrivileges() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(1);

    const [config] = useState({
        headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
    });

  // Fetch all users
  useEffect(() => {
    axios
        .get(backendPath + 'volunteer/all', config)
        .then((resp) => {
            console.log(resp.data.results)
            setUsers(resp.data.results)
        })
        .finally(() => {setLoading(x => x - 1)});
  }, [config])

    function promote(user_id) {
      console.log(user_id)
    }

    function demote(user_id) {
      console.log(user_id)
    }

  return (
    <div className={'w-100 mt4 ba br b--black-10 pa3'}>
      <h2 className={'mb2'}>User Privileges</h2>
      <hr />
      <p>
        The table below shows all users and their system privileges. This includes
        root administrators, administrators and volunteers. You can use the table to
        change the privileges of a user at any time.
      </p>
        {loading <= 0 && (
            <table className="table">
                <thead>
                <tr>
                    <th scope="col">Volunteer Name</th>
                    <th scope="col">User Type</th>
                    <th scope="col">Promote</th>
                    <th scope="col">Demote</th>
                </tr>
                </thead>
                <tbody>
                {users !== [] &&
                users.map((x) => {
                    return (
                    <tr key={x['ID']}>
                        <td>
                            {x['firstName']} {x['lastName']}
                        </td>
                        <td>{x['role']}</td>
                        <td>
                            {x['role'] === 0 ?
                                <button
                                    className={'btn btn-danger'}
                                    onClick={() => {
                                        promote(x['id']);
                                }}>
                                    Promote
                                </button>
                                : ''}
                        </td>
                        <td>
                            {x['role'] >= 1 ?
                                <button
                                    className={'btn btn-danger'}
                                    onClick={() => {
                                        demote(x['id']);
                                }}>
                                    Demote
                                </button>
                                : ''}
                        </td>
                    </tr>
                    );
                })}
                </tbody>
            </table>
        )}
    </div>
  );
}

export default UserPrivileges;
