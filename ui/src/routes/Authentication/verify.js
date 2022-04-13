import axios from 'axios';
import React, { useState } from 'react';
import { NavLink, useHistory } from 'react-router-dom';

import { backendPath } from '../../config';

function Verify() {
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

  /*updates values based on input into the field*/
  function handleChange(field, value) {
    const lcl = { ...values };
    lcl[field] = value;
    setValues(lcl);
  }

  function submit(e) {
    e.preventDefault();
    axios.post(backendPath + 'authentication/verify', values).then((resp) => {
      switch (resp.data['result']) {
        case 'CODE_CORRECT':
          /* Email passed to next page */
          localStorage.setItem("email", values['email']);

          /*Proceed to next page*/
          history.push('/reset/');

          /* NOTE: May be a security issue with how the email is passed, if application progresses past PoC will need to be investigated and potentially method of sharing account to be reset changed" */
          break;
        case 'CODE_INCORRECT':
          setError('Code was not correct');
          break;
        case 'CODE_OVERDUE':
          setError('Code has expired');
          break;
        case 'FAIL':
          setError('Error: No code found in system');
          break;
        default:
          setError('Unknown Error');
          break;
      }
    });
  }

  return (
    <div className="padding">
      <form
        onSubmit={submit}
        className={'mt6 w-50 ml-auto mr-auto ba br2 b--black-10 pa3'}>

        {/* Heading */}
        <h2>Enter Code</h2>

        {/* Code input form*/}
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

        {/* Submit Button */}
        <input
          type="submit"
          value="Submit"
          className={'btn bg-light-red pv2 ph3 br2 b near-white dim'}
        />

        {/* Back Button */}
        <div className={'mt2'}>
          <NavLink to={'/forgot'}>Back</NavLink>
        </div>

        {/* Error Code */}
        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}
      </form>

      {/* Resend Code Button */}
      <div id="register-btn" className={'submit-btn mt2 mb4'}>
            <a href="/forgot" className="btn w-80 bg-light-silver dim" role="button"><strong>Resend Code</strong></a>
      </div>

      {/* TODO - Currently "resend code" redirects back to the forgot password page where you enter your email when the function could just be called again. Look to use OnClick Function*/}

    </div>

  );
}

export default Verify;
