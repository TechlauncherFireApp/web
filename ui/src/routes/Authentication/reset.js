import axios from 'axios';
import React, { useState } from 'react';
import { NavLink, useHistory } from 'react-router-dom';

import { backendPath } from '../../config';

function Reset() {
  const [values, setValues] = useState({});
  const [error, setError] = useState(undefined);
  const history = useHistory();

  /*Todo: Look at the changepassword backend process as it will probably be very similar to our needs for the reset password process*/
  function submit(e) {
    e.preventDefault();
    axios.post(backendPath + 'authentication/reset', values).then((resp) => {
      switch (resp.data['result']) {
        case 'SUCCESS':
          history.push('/login?success=true');
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
  /* Function from the 2021 team to connect submit button with backend, will need to be modified when backend is complete */


  function handleChange(field, value) {
    const lcl = { ...values };
    lcl[field] = value;
    setValues(lcl);
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
            name="password"
            onChange={(e) => {
              handleChange('password', e.target.value);
            }}
          />
        </div>

        {/* Second Password Input */}
        <div className="form-group">
          <label htmlFor={'password'}>Repeat New Password:</label>
          <input
            className={'form-control'}
            type="password"
            name="password"
            onChange={(e) => {
              handleChange('password', e.target.value);
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

        <div className={'mt2'}>
          <NavLink to={'/login'}>Back</NavLink>
        </div>
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

