import './shift.scss';

import React from 'react';

import {
  parseDateTime,
  parseRolesAsString,
  toSentenceCase,
} from '../../common/functions';

export default class Shift extends React.Component {
  state = {
    status: '',
  };

  constructor(props) {
    super(props);
    this.state.status = props.shift.volunteerStatus;
  }

  updateStatus = (e) => {
    this.setState({ status: e.target.value });
    this.props.updateStatus(e.target.value, this.props.shift);
  };

  render() {
    const { shift } = this.props;
    const status = this.state.status;

    return (
      <tr>
        <td>{parseDateTime(shift.vehicleFrom, shift.vehicleTo)}</td>
        <td>{parseRolesAsString(shift.volunteerRoles)}</td>
        <td>{toSentenceCase(shift.vehicleType)}</td>
        <td>{shift.requestTitle}</td>
        <td>
          <select className={status} onChange={this.updateStatus}>
            <option value="pending" hidden selected={status === 'pending'}>
              Pending Confirmation
            </option>
            <option value="confirmed" selected={status === 'confirmed'}>
              Confirmed
            </option>
            <option value="rejected" selected={status === 'rejected'}>
              Rejected
            </option>
          </select>
        </td>
      </tr>
    );
  }
}
