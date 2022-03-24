import axios from 'axios';
import React, { useState } from 'react';
import { NavLink, useHistory } from 'react-router-dom';

import { backendPath } from '../../config';

function forgot() {
  const [values, setValues] = useState({});
  const [error, setError] = useState(undefined);
  const history = useHistory();

  function submit(e) {
    e.preventDefault();
    axios.post(backendPath + 'authentication/emailcode', values).then((resp) => {
      switch (resp.data['result']) {
        case 'SUCCESS':
          history.push('/emailcode?success=true');
          break;
        case 'EMAIL_NOT_FOUND':
          setError('Email cannot be found');
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
  }

  return (
    <div className="padding">
      <form
        onSubmit={submit}
        className={'mt6 w-50 ml-auto mr-auto ba br2 b--black-10 pa3'}>
        <h2>Reset Password</h2>
        <div className="form-group">
          <label htmlFor={'email'}>Email*:</label>
          <input
            className={'form-control'}
            type="text"
            name="email"
            onChange={(e) => {
              handleChange('email', e.target.value);
            }}
          />
        </div>

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

export default Forgot;
