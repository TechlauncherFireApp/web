import moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import { Table } from 'react-bootstrap';

import Position from './position';

function Asset(props) {
  const { asset, volunteerList, onUpdate } = props;

  return (
    <Table className="mt-4" striped bordered hover size="sm">
      <thead>
        <tr>
          <td width="15%">
            <b>{asset['assetClass']}</b>{' '}
          </td>
          <td colSpan={6}>
            <span>
              {moment(asset['startTime']).format('LLL')} -{' '}
              {moment(asset['endTime']).format('LLL')}
            </span>
          </td>
        </tr>
      </thead>
      <tbody>
        {asset['volunteers'].map((v) => {
          return (
            <Position
              key={v.positionId}
              asset={asset}
              position={v}
              volunteers={volunteerList}
              onUpdate={onUpdate}
            />
          );
        })}
      </tbody>
    </Table>
  );
}

Asset.propTypes = {
  asset: PropTypes.object,
  volunteerList: PropTypes.array,
  onUpdate: PropTypes.func,
};

export default Asset;
