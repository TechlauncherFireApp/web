import axios from 'axios';
import FontPicker from "font-picker-react";
import React, {useEffect, useState} from 'react';
import { SketchPicker } from "react-color";

import {backendPath} from '../../config';

function Configuration() {
    const [refresh, setRefresh] = useState(0);
    const [deletions, setDeletions] = useState(0);
    const [error, setError] = useState(undefined);

    const [configs, setConfigs] = useState([]);
    const [newConfigName, setNewConfigName] = useState('');
    const [newConfigTitle, setNewConfigTitle] = useState('');
    const [newConfigFont, setNewConfigFont] = useState('Anton');
    const [newConfigNavColour, setNewConfigNavColour] = useState('#fff');
    const [newConfigBackColour, setNewConfigBackColour] = useState('');

    useEffect(() => {
        axios
            .get(backendPath + 'tenancy_config', {
                headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')},
                params: {getAll: Boolean(true)}
            })
            .then((resp) => {
                setConfigs(resp.data.results);
                console.log(resp.data.results);
            });
    }, [refresh, deletions])

    function addNew(e) {
        e.preventDefault();
        setError(undefined);
        if (newConfigName === '') {
            setError('Configuration name required.');
            return;
        }
        // Post the new configuration and refresh the table
        axios
            .post(
                backendPath + 'tenancy_config',
                {
                    name: newConfigName,
                    title: newConfigTitle,
                    font: newConfigFont,
                    navColour: newConfigNavColour,
                    backColour: newConfigBackColour
                },
                {
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                    },
                }
            )
            .then(() => {
                setNewConfigName('');
                setNewConfigTitle('');
                setNewConfigFont('Anton');
                setNewConfigNavColour('#fff');
                setNewConfigBackColour('');
                setRefresh((x) => x + 1);
            });
    }

    function toggle(id) {
        axios
            .patch(
                backendPath + 'tenancy_config',
                {id: id},
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

    function deleteConfig(id) {
        axios
            .delete(
                backendPath + 'tenancy_config',
                {
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                    },
                    params: {
                        id: id,
                    }
                })
            .then(() => {
                setDeletions((x) => x + 1);
            });
    }


    return (
        <div className={'w-100 mt4 ba br b--black-10 pa3'}>
            <h2 className={'mb2'}>Tenant Customisation</h2>
            <hr/>
            <h5>New branding configuration</h5>
            <form onSubmit={addNew}>
                <div className="form-group">
                    <label htmlFor={'configName'}>Configuration name:</label>
                    <input
                        id={'roleCode'}
                        className={'form-control w-third'}
                        value={newConfigName}
                        type="text"
                        name="code"
                        onChange={(e) => {
                            setNewConfigName(e.target.value);
                        }}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor={'configTitle'}>Website title:</label>
                    <input
                        id={'roleName'}
                        className={'form-control w-third'}
                        value={newConfigTitle}
                        type="text"
                        name="name"
                        onChange={(e) => {
                            setNewConfigTitle(e.target.value);
                        }} />
                    <br />
                    <h7>Title font: </h7>
                    <FontPicker apiKey="AIzaSyCkXby-0LMacdrycDNmwoII8Lm-vfi_WC0"
                                activeFontFamily={newConfigFont}
                                onChange={(nextFont) => setNewConfigFont(nextFont.family)}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor={'configNavColour'}>Navbar Colour:</label><br/>
                    <SketchPicker
                        color={newConfigNavColour}
                        onChange={(nextColour) => setNewConfigNavColour(nextColour.hex)}/>
                </div>
                {error && <div className={'alert alert-danger'}>{error}</div>}
                <button
                    type="submit"
                    value="Submit"
                    className={'btn bg-light-red pv1 ph2 br2 b near-white dim mv2'}>
                    Submit
                </button>
            </form>
            <hr/>
            <h5>Existing configurations</h5>
            <table className="table">
                <thead>
                <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Page Title</th>
                    <th scope="col">Title Font</th>
                    <th scope="col">Navbar Colour</th>
                    <th scope="col">Background Colour</th>
                    <th scope="col">Action</th>
                    <th scope="col">Deletion</th>
                </tr>
                </thead>
                <tbody>
                {configs !== [] &&
                configs.map((x) => {
                    return (
                        <tr key={x['id']}>
                            <th scope="row">{x['name']}</th>
                            <td>{x['title']}</td>
                            <td>{x['font']}</td>
                            <td>{x['nav_colour']}</td>
                            <td>{x['back_colour']}</td>
                            <td>
                                <button
                                    className={'btn btn-danger'}
                                    onClick={() => {
                                        toggle(x['id']);
                                    }}>
                                    {x['deleted'] === 'False' ? 'Disable' : 'Enable'}
                                </button>
                            </td>
                            <td>
                                <button
                                    className={'btn btn-danger'}
                                    onClick={() => {
                                        deleteConfig(x['id']);
                                    }}>
                                    Remove
                                </button>
                            </td>
                        </tr>
                    );
                })}
                {configs.length === 0 && (
                    <tr key={'error'}>
                        <th colSpan={2}>No configurations currently defined.</th>
                    </tr>
                )}
                </tbody>
            </table>
        </div>
    );
}

export default Configuration;
