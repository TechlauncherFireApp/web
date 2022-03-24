import axios from 'axios';
import React, { useState } from 'react';
import { NavLink, useHistory } from 'react-router-dom';

import { backendPath } from '../../config';

function Verify() {
  const [values, setValues] = useState({});
  const [error, setError] = useState(undefined);
  const history = useHistory();

  function submit(e) {
    e.preventDefault();
    axios.post(backendPath + 'authentication/verify', values).then((resp) => {
      switch (resp.data['result']) {
        case 'SUCCESS':
          history.push('/verify?success=true');
          break;
        case 'INCORRECT':
          setError('Code was not correct');
          break;
        default:
          setError('Unknown error');
          break;
      }
    });
  }

  {/*backend -> authentication/verifyCode function needs to be written*/}

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
        <h2>Enter Code</h2>
        <div className="form-group">
          <label htmlFor={'email'}>Verification Code:</label>
          <input
            className={'form-control'}
            type="text"
            name="code"
            onChange={(e) => {
              handleChange('code', e.target.value);
            }}
          />
        </div>

        <input
          type="submit"
          value="Submit"
          className={'btn bg-light-red pv2 ph3 br2 b near-white dim'}
        />
        {/* PLACEHOLDER
          TODO: Below NavLink is a placeholder, can be removed once backend for submit button is done
        */}
        <NavLink to="/reset">Submit</NavLink>

        <div className={'mt2'}>
          <NavLink to={'/forgot'}>Back</NavLink>
        </div>
        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}
      </form>

      <div id="register-btn" className={'submit-btn mt2 mb4'}>
            <a href="/register" className="btn w-80 bg-light-silver dim" role="button"><strong>Resend Code</strong></a>
      </div>

      {/*
      TODO: Need to add procedure here that has this button resend the verification code to the correct email
      Currently using link to register as placeholder
      */}

    </div>


  );
}

export default Verify;
