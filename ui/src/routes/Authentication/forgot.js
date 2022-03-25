import axios from 'axios';
import React, { useState } from 'react';
import { NavLink, useHistory } from 'react-router-dom';

import { backendPath } from '../../config';

function Forgot() {
  const [values, setValues] = useState({});
  const [error, setError] = useState(undefined);
  const history = useHistory();


  function submit(e) {
    /* TODO: Below function is the hook for the incomplete backend */
    e.preventDefault();
    axios.post(backendPath + 'authentication/emailCode', values).then((resp) => {
      switch (resp.data['result']) {
        case 'SUCCESS':
          history.push('/emailCode?success=true');
          /* Maybe change this above line, essentially will link to the next page and bring over any necessary account data*/
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
          <label htmlFor={'email'}>Email:</label>
          <input
            className={'form-control'}
            type="text"
            name="email"
            onChange={(e) => {
              handleChange('email', e.target.value);
            }}
          />
        </div>

        {/* UNCOMMENT THIS WHEN BACKEND HOOKS WORK
          <input
              type="submit"
              value="Submit"
              className={'btn bg-light-red pv2 ph3 br2 b near-white dim'}
          />
        */}

        {/* PLACEHOLDER
          TODO: Below NavLink is a placeholder, can be removed once backend for submit button is done
        */}
        <NavLink to="/verify">Submit</NavLink>

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
