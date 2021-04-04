import React, { useState } from 'react';
import axios from 'axios';
import { backendPath } from '../../config';
import { NavLink, useHistory } from 'react-router-dom';

function Register() {
  const [values, setValues] = useState({});
  const [error, setError] = useState(undefined);
  const history = useHistory();

  function submit(e) {
    e.preventDefault();
    axios.post(backendPath + 'authentication/register', values).then((resp) => {
      switch (resp.data['result']) {
        case 'SUCCESS':
          history.push('/login?success=true');
          break;
        case 'USERNAME_ALREADY_REGISTERED':
          setError('Username is already registered for another account');
          break;
        case 'BAD_USERNAME':
          setError('Username does not meet requirements.');
          break;
        case 'BAD_PASSWORD':
          setError('Password does not meet requirements. ');
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
        <h2>Register as a volunteer</h2>
        <div className="form-group">
          <label>Email*:</label>
          <input
            className={'form-control'}
            type="text"
            name="email"
            onChange={(e) => {
              handleChange('email', e.target.value);
            }}
          />
        </div>
        <div className="form-group">
          <label>Password*:</label>
          <input
            className={'form-control'}
            type="password"
            name="password"
            onChange={(e) => {
              handleChange('password', e.target.value);
            }}
          />
          <small>
            Must be at least 8 characters long and container an uppercase and
            lowercase character.
          </small>
        </div>
        <div className="form-group">
          <label>Given Name*:</label>
          <input
            className={'form-control'}
            type="text"
            name="giveNName"
            onChange={(e) => {
              handleChange('given_name', e.target.value);
            }}
          />
        </div>
        <div className="form-group">
          <label>Last Name*:</label>
          <input
            className={'form-control'}
            type="text"
            name="lastName"
            onChange={(e) => {
              handleChange('last_name', e.target.value);
            }}
          />
        </div>
        <div className="form-group">
          <label>Phone Number*:</label>
          <input
            className={'form-control'}
            type="text"
            name="phoneNumber"
            onChange={(e) => {
              handleChange('phone', e.target.value);
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

export default Register;
