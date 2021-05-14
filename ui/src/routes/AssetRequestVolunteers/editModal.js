import './editModal.scss';

import axios from 'axios';
import moment from 'moment';
import React, { useEffect, useState } from 'react';
import { Button, Modal, Table } from 'react-bootstrap';

import { backendPath } from '../../config';

function EditModal(props) {
  const { position, asset, assigned, volunteers, onUpdate, onHide } = props;
  const [loading, setLoading] = useState(false);
  const [positionFilter, setPositionFilter] = useState(false);
  const [selectedVolunteer, setSelectedVolunteer] = useState(undefined);
  const [searchText, setSearchText] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  function saveChange() {
    setLoading(true);
    axios
      .patch(
        backendPath + 'shift/request',
        {},
        {
          params: {
            shift_id: asset.shiftID,
            position_id: position.positionId,
            volunteer_id: selectedVolunteer,
          },
        }
      )
      .then(() => {
        setLoading(false);
        onHide();
        onUpdate();
      });
  }

  function removeVolunteer() {
    setLoading(true);
    axios
      .delete(backendPath + 'shift/request', {
        params: {
          shift_id: asset.shiftID,
          position_id: position.positionId,
        },
      })
      .then(() => {
        setLoading(false);
        onHide();
        onUpdate();
      });
  }

  useEffect(() => {
    let lcl = [...volunteers];
    lcl = lcl.filter((v) => {
      const name = `${v.firstName} ${v.lastName}`;
      return name.indexOf(searchText) > -1;
    });
    if (positionFilter) {
      lcl = lcl.filter((v) => {
        return v.possibleRoles.includes(position.role);
      });
    }

    setSearchResults(lcl);
  }, [position.role, volunteers, searchText, positionFilter]);

  return (
    <Modal
      show={props.show}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
      backdrop="static">
      <Modal.Header closeButton closeLabel="cancel" onHide={props.onHide}>
        <Modal.Title id="contained-modal-title-vcenter">
          {asset.assetClass} - {position.role}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p>
          {moment(asset.startTime).format('LLL')} -{' '}
          {moment(asset.endTime).format('LLL')}
        </p>
        {assigned === true ? (
          <p>
            Assigned to:{' '}
            <b>
              {position.volunteerGivenName} {position.volunteerSurname}
            </b>
          </p>
        ) : (
          <p>
            <i>This position is currently unassigned</i>
          </p>
        )}
        <form>
          <input
            id="searchBar"
            type="text"
            placeholder="Search Volunteer via Name"
            value={searchText}
            onChange={(e) => {
              setSearchText(e.target.value);
            }}
          />
          &nbsp;
          <input
            className="positionFilter"
            type="checkbox"
            id="positionFilter"
            value={positionFilter}
            onClick={(e) => {
              setPositionFilter(e.target.checked);
            }}
          />{' '}
          Only show &apos;{position.role}&apos;s
          <hr />
          <div className="con-vols">
            {searchResults.length > 0 && (
              <Table striped bordered hover size="sm">
                <thead>
                  <tr>
                    <th width={'33%'}>Name</th>
                    <th width={'33%'}>Roles</th>
                    <th width={'33%'}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {searchResults.map((t) => (
                    <tr
                      key={t.ID}
                      className="view"
                      onClick={() => {
                        setSelectedVolunteer(t.ID);
                      }}>
                      <td>
                        {t.firstName} {t.lastName}
                      </td>
                      <td>
                        {t.possibleRoles.map((q) => (
                          <div key={q}>- {q}</div>
                        ))}
                      </td>
                      <td>
                        {`${position.volunteerId}` === t.ID && <b>Assigned</b>}
                        {`${selectedVolunteer}` === t.ID &&
                          `${position.volunteerId}` !== t.ID && (
                            <i>Assign Volunteer</i>
                          )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            )}
            {searchResults.length === 0 && <p>Nothing found</p>}
          </div>
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button
          className="btn btn-primary"
          onClick={saveChange}
          disabled={loading}>
          {assigned === true ? 'Replace' : 'Assign Volunteer'}
        </Button>
        {assigned === true && (
          <Button
            className="btn btn-danger"
            onClick={removeVolunteer}
            disabled={loading}>
            Remove
          </Button>
        )}
        <Button
          className="btn btn-danger"
          onClick={props.onHide}
          disabled={loading}>
          Cancel
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default EditModal;
