import axios from 'axios';
import queryString from 'query-string';
import React, { useState } from 'react';
import { useLocation } from 'react-router';
import { useHistory } from 'react-router-dom';

// import { NavLink, useHistory } from 'react-router-dom';       //uncomment this line when  using any NavLink property.
import { backendPath } from '../../config';
import ff_image from './images/fire-fighters-1080.png';
import fa_logo from './images/fireapp-logo.png';

function Login() {
  const [values, setValues] = useState({});
  const query = queryString.parse(useLocation().search);
  const [error, setError] = useState(undefined);
  const showRegistrationSuccess = query['success'] === 'true';
  const history = useHistory();

  function submit(e) {
    e.preventDefault();
    axios.post(backendPath + 'authentication/login', values).then((resp) => {
      switch (resp.data['result']) {
        case 'SUCCESS':
          localStorage.setItem('access_token', resp.data['access_token']);
          localStorage.setItem('role', resp.data['role']);
          localStorage.setItem('id', resp.data['id']);
          switch (resp.data['role']) {
            case 'VOLUNTEER':
              history.push('/volunteer/' + resp.data['id']);
              break;
            default:
              history.push('/captain');
          }
          break;
        default:
          setError('Unknown username or bad password');
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
    <div className="login-page">
      <div className="padding1">
        {showRegistrationSuccess && error === undefined && (
          <div className="w-50 ml-auto mr-auto alert alert-success" role="alert">
            Registration successful, you may now login.
          </div>
        )}
        <form
          onSubmit={submit}
          className={'mt1 mb1 ml1 mr1 bn br2 pa3'}>   {/*FIXME -- change1 - jasmeen*/}
          {/*className={'mt6 w-50 ml-auto mr-auto ba br2 b--black-10 pa3'}>*/}
          {/*top-margin bottom-margin left-margin right-margin border-style border-radius border-color padding*/}
          <div className="Fireapp-logo br3">
            <img src={fa_logo} id="fireapp-logo-img" alt="FireApp Logo"/>
            <h2>FIREAPP</h2>
          </div>

          <div className="form-group-auth">
            <label htmlFor={'email'}>Email or Username*:</label>
            <input
              className={'form-control'}
              type="text"
              name="email"
              onChange={(e) => {
                handleChange('email', e.target.value);
              }}
            />
          </div>
          <div className="form-group-auth">
            <label htmlFor={'password'}>Password*:</label>
            <input
              className={'form-control'}
              type="password"
              name="password"
              onChange={(e) => {
                handleChange('password', e.target.value);
              }}
            />
          </div>
          <div className="submit-btn">
            <input
              type="submit"
              value="Sign In"
              className={'btn submit-btn-2 w-80 pv2 ph3 br2 white-90 b dim'}      // IMP!! width should be w-80. button color padd-top-bott padd-left-right border-radius font-weight text-color dim-upon-hover
            />
          </div>
          {/*<div className={'change-pass-option'}>*/}
          {/*  <NavLink to={'changepass'}>Change Password?</NavLink>*/}
          {/*</div>*/}
          <div className="new-to-fireapp silver">----------New to FireApp?----------</div>
          <div id="register-btn" className={'submit-btn mt2 mb4'}>
            <a href="/register" className="btn w-80 bg-light-silver dim" role="button">Create an account</a>
          </div>
          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}
        </form>
      </div>
      <div id="login-ff-image" className="img-fluid" align="top">
        <img src={ff_image} id="firefighters-img" alt="Fire fighters" align={"right"}/>
      </div>
   </div>
  );
}

export default Login;
