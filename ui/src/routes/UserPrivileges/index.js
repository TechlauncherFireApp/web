import axios from 'axios';
import React, {useEffect, useState} from 'react';
import {useHistory} from "react-router-dom";

import {backendPath} from "../../config";

function UserPrivileges() {
    const [users, setUsers] = useState([]);
    const [rootAdmins, setRootAdmins] = useState(0);
    const [loading, setLoading] = useState(1);
    const [user] = useState(localStorage.getItem('id'));
    const [user_role] = useState(localStorage.getItem('role'));
    const history = useHistory();

    const [refresh, setRefresh] = useState(0);

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
            .finally(() => {
                users.forEach((u) => {
                    if (u['role'] === 2) {
                        setRootAdmins(x => x + 1);
                    }
                })
                setLoading(x => x - 1)
            });
    }, [config, refresh])

    function promote(user_id) {
        axios
            .request({
                    url: backendPath + 'user-type',
                    method: 'PATCH',
                    params: {userId: user_id, typeChange: 'promote'},
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                    },
                }
            ).then(() => {
            setRefresh((x) => x + 1)
        });
    }

    function demote(user_id) {
        axios
            .request({
                    url: backendPath + 'user-type',
                    method: 'PATCH',
                    params: {userId: user_id, typeChange: 'demote'},
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                    },
                }
            ).then(() => {
            setRefresh((x) => x + 1)
        });
    }

    function selfDemote(user_id) {
        axios
            .request({
                    url: backendPath + 'user-type',
                    method: 'PATCH',
                    params: {userId: user_id, typeChange: 'self-demote'},
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                    },
                }
            ).then(() => {
            setRefresh((x) => x + 1)
            history.push('/logout')
        });
    }

    return (
        <div className={'w-100 mt4 ba br b--black-10 pa3'}>
            <h2 className={'mb2'}>User Privileges</h2>
            <hr/>
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
                                <td>{
                                    x['role'] === 0 ? 'Volunteer' :
                                        x['role'] === 1 ? 'Administrator' :
                                            x['role'] === 2 ? 'Root Administrator' :
                                                'null'
                                }</td>
                                <td>
                                    {user_role === 'ROOT_ADMIN' && (x['role'] === 0 || x['role'] === 1) ?
                                        <button
                                            className={'btn btn-danger'}
                                            onClick={() => {
                                                promote(x['ID']);
                                            }}>
                                            Promote
                                        </button>
                                        : user_role === 'ADMIN' && (x['role'] === 0) ?
                                            <button
                                                className={'btn btn-danger'}
                                                onClick={() => {
                                                    promote(x['ID']);
                                                }}>
                                                Promote
                                            </button>
                                            : ''}
                                </td>
                                <td>
                                    {user_role === 'ROOT_ADMIN' && x['role'] === 1 ?
                                        <button
                                            className={'btn btn-danger'}
                                            onClick={() => {
                                                demote(x['ID'])
                                            }}>
                                            Demote
                                        </button>
                                        :
                                        x['ID'] === user && user_role === 'ROOT_ADMIN' && rootAdmins > 1 ?
                                            <button
                                                className={'btn btn-danger'}
                                                onClick={() => {
                                                    if (window.confirm('Are you sure you want to demote ' +
                                                        'yourself from Root Admin to Admin?'))
                                                        selfDemote(x['ID'])
                                                }}>
                                                Self Demote
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
