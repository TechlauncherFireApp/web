import './position.scss';

import React, { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';

import EditModal from './editModal';

const GREY = '#ececec';
const CONFIRMED = '#abff95';
const WARNING = '#FFCCCC';

function Position(props) {
  const { position, asset, volunteers, onUpdate } = props;
  const [assigned, setAssigned] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [backgroundColour, setBackgroundColour] = useState(GREY);

  useEffect(() => {
    if (position['status'] === 'confirmed') {
      setBackgroundColour(CONFIRMED);
      setAssigned(true);
      return;
    }
    if (position['status'] === 'pending') {
      setBackgroundColour(GREY);
      setAssigned(true);
      return;
    }
    setBackgroundColour(WARNING);
    setAssigned(false);
  }, [position]);

  return (
    <>
      <EditModal
        asset={asset}
        assigned={assigned}
        show={showModal}
        position={position}
        onUpdate={onUpdate}
        volunteers={volunteers}
        onHide={() => {
          setShowModal(false);
        }}
      />

      <tr
        key={position.positionID}
        className={'body'}
        style={{
          backgroundColor: backgroundColour,
        }}>
        <td>{position.role}</td>
        {assigned ? (
          <>
            <td width="30%">
              {position.volunteerGivenName} {position.volunteerSurname}
            </td>
            <td width="20%">Qualifications coming soon!</td>
            <td width="10%">{position.mobileNo}</td>
            <td width="15%">{position.status}</td>
          </>
        ) : (
          <>
            <td width="30%">
              <i>Unassigned</i>
            </td>
            <td width="20%" />
            <td width="10%" />
            <td width="15%">Unassigned</td>
          </>
        )}
        <td>
          <Button
            className="btn-warning fill"
            onClick={() => {
              setShowModal(true);
            }}>
            {assigned ? 'Change' : 'Add'}
          </Button>
        </td>
      </tr>
    </>
  );
}

export default Position;
