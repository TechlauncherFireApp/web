import axios from 'axios';
import React, { useState } from 'react';
import { NavLink, useHistory } from 'react-router-dom';

import { backendPath } from '../../config';

function Availability() {
  const [values, setValues] = useState({});
  const [error, setError] = useState(undefined);
  const history = useHistory();

  function submit(e) {
    e.preventDefault();
    axios.post(backendPath + 'authentication', values).then((resp) => {
      history.push('/login?success=true');
      let x = resp.data['result'];
      if(x) {
        setError('placeholder');
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

        <h2>Enter your unavailability</h2>

        <div className="form-group">
          <label htmlFor={'Name'}>Title:</label>
          <input
            className={'form-control'}
            type="text"
            name="name"
            onChange={(e) => {
              handleChange('name', e.target.value);
            }}
          />
        </div>

        <div className="form-group">
          <label htmlFor={'givenName'}>Reoccuring:</label>
          <input
            type="checkbox"
            name="reoccur"
            onChange={(e) => {
              handleChange('reoccur', e.target.value);
            }}
          />
        </div>

        <div className="form-group">
          <label htmlFor="startTime">Choose a Start Time:</label>
          <select id="startTime" name="startTime">
            <option value="test">1am</option>
            <option value="test">2am</option>
            <option value="testtest">3am</option>
            <option value="test">4am</option>
            <option value="test">5am</option>
            <option value="testv">6am</option>
            <option value="test">7am</option>
            <option value="testtest">8am</option>
            <option value="test">9am</option>
            <option value="test">10am</option>
            <option value="test">11am</option>
            <option value="testv">12am</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="endTime">Choose a End Time:</label>
          <select id="endTime" name="endTime">
            <option value="test">1am</option>
            <option value="test">2am</option>
            <option value="testtest">3am</option>
            <option value="test">4am</option>
            <option value="test">5am</option>
            <option value="testv">6am</option>
            <option value="test">7am</option>
            <option value="testtest">8am</option>
            <option value="test">9am</option>
            <option value="test">10am</option>
            <option value="test">11am</option>
            <option value="testv">12am</option>
          </select>
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

/* Need to find a react library for time and date pickers
* https://www.npmjs.com/package/react-datepicker
* https://mui.com/x/react-date-pickers/time-picker - (also has some excellent datepickers)
*
*
* */

export default Availability;
