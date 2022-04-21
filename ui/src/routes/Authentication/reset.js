import axios from 'axios';
import React, { useState } from 'react';
import {NavLink, useHistory} from 'react-router-dom';

import { backendPath } from '../../config';

function Reset() {
  const [values, setValues] = useState(() => {
    /*Add email pulled from previous page to the values dict*/
    const email = localStorage.getItem("email");
    const firstValue = {
      'email': email
    }
    return firstValue || {};
  });
  const [error, setError] = useState(undefined);
  const history = useHistory();

  function submit(e) {
    e.preventDefault();
    axios.post(backendPath + 'authentication/reset', values).then((resp) => {
      switch (resp.data['result']) {
        case 'SUCCESS':
          history.push('/login/');
          break;
        case 'NO_MATCH':
          setError('Passwords did not match');
          break;
        case 'NO_CRITERIA':
          setError('Passwords does not meet requirements.');
          break;
        default:
          setError('Unknown error');
          break;
      }
    });
  }

  function handleChange(field, value) {
    const lcl = { ...values };
    lcl[field] = value;
    setValues(lcl);
    console.log(values);
  }

  return (
    <div className="padding">
      <form
        onSubmit={submit}
        className={'mt6 w-50 ml-auto mr-auto ba br2 b--black-10 pa3'}>

        {/* Heading */}
        <h2>Reset your password</h2>

        {/* New Password Input */}
        <div className="form-group">
          <label htmlFor={'password'}>New Password:</label>
          <input
            className={'form-control'}
            type="password"
            name="new_password"
            onChange={(e) => {
              handleChange('new_password', e.target.value);
            }}
          />
        </div>

        {/* Second Password Input */}
        <div className="form-group">
          <label htmlFor={'password'}>Repeat New Password:</label>
          <input
            className={'form-control'}
            type="password"
            name="repeat_password"
            onChange={(e) => {
              handleChange('repeat_password', e.target.value);
            }}
          />
          {/* Fine print - password criteria */}
          <small>
            Must be at least 8 characters long and contain an uppercase and
            lowercase character.
          </small>
        </div>

        {/* Submit Button */}
        <input
          type="submit"
          value="Submit"
          className={'btn bg-light-red pv2 ph3 br2 b near-white dim'}
        />

        {/*Back Button*/}
        <div className={'mt2'}>
          <NavLink to={'/login'}>Back</NavLink>
        </div>

        {/*Error Code*/}
        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}
      </form>
    </div>
  );
}

export default Reset;

