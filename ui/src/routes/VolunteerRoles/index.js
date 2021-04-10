import React, { useEffect, useState } from 'react';
import { backendPath } from '../../config';
import axios from 'axios';

function VolunteerRoles() {
  const [roles, setRoles] = useState([]);
  const [volunteerRoles, setVolunteerRoles] = useState([]);
  const [volunteers, setVolunteers] = useState([]);
  const [loading, setLoading] = useState(1);

  const [refresh, setRefresh] = useState(0);

  const [config] = useState({
    headers: {
      Authorization: 'Bearer ' + localStorage.getItem('access_token'),
    },
  });

  // Fetch all required data in sequence
  useEffect(() => {
    // Get all the volunteers
    axios.get(backendPath + 'volunteer/all', config).then((volunteerResp) => {
      setVolunteers(volunteerResp.data.results);
      // Get all the roles available
      axios.get(backendPath + 'reference/roles', config).then((roleResp) => {
        const activeRoles = roleResp.data.filter(
          (x) => x['deleted'] === 'False'
        );
        setRoles(activeRoles);
        // Get the combination of users assigned to roles.
        axios
          .get(backendPath + 'user-role', config)
          .then((resp) => {
            // Build a usable data structure of the 3 results
            const rtn = {};
            volunteerResp.data.results.forEach((u) => {
              const user = {};
              // Put each role into the users map
              activeRoles.forEach((role) => {
                let enabled = false;
                if (
                  resp.data.find(
                    ({ roleId, userId }) =>
                      `${roleId}` === `${role['id']}` &&
                      `${u['ID']}` === `${userId}`
                  ) !== undefined
                ) {
                  enabled = true;
                }
                user[role['id']] = enabled;
              });
              // Store the user in the return list
              rtn[u['ID']] = user;
            });
            setVolunteerRoles(rtn);
          })
          .finally(() => {
            setLoading((x) => x - 1);
          });
      });
    });
  }, [config]);

  // Run when the data is changed on the form to only refresh the part that can change.
  useEffect(() => {
    if (roles.length === 0 || volunteers.length === 0) {
      return;
    }
    axios
      .get(backendPath + 'user-role', config)
      .then((resp) => {
        // Build a usable data structure of the 3 results
        const rtn = {};
        volunteers.forEach((u) => {
          const user = {};
          // Put each role into the users map
          roles.forEach((role) => {
            let enabled = false;
            if (
              resp.data.find(
                ({ roleId, userId }) =>
                  `${roleId}` === `${role['id']}` &&
                  `${u['ID']}` === `${userId}`
              ) !== undefined
            ) {
              enabled = true;
            }
            user[role['id']] = enabled;
          });
          // Store the user in the return list
          rtn[u['ID']] = user;
        });
        setVolunteerRoles(rtn);
      })
      .finally(() => {
        setLoading((x) => x - 1);
      });
    // eslint-disable-next-line
  }, [config, refresh]);

  function handleRole(userId, roleId, enabled) {
    if (enabled) {
      // Adding a role to the user
      axios
        .post(backendPath + 'user-role', { userId, roleId }, config)
        .then((x) => {
          setRefresh((x) => x + 1);
        });
    } else {
      // Removing a role from a user
      axios
        .patch(backendPath + 'user-role', { userId, roleId }, config)
        .then((x) => {
          setRefresh((x) => x + 1);
        });
    }
  }

  return (
    <div className={'w-100 mt4 ba br b--black-10 pa3'}>
      <h2 className={'mb2'}>Volunteer Roles</h2>
      <hr />
      <p>
        The table below shows volunteers and their currently available roles.
        Check or uncheck the checkbox to enable that volunteer to complete that
        role in future assignments.
      </p>
      {loading <= 0 && (
        <table className="table">
          <thead>
            <tr>
              <th scope="col">Volunteer Name</th>
              <th className={'tc'}>Roles</th>
            </tr>
          </thead>
          <tbody>
            {volunteers !== [] &&
              volunteers.map((x) => {
                return (
                  <tr key={x['ID']}>
                    <td>
                      {x['firstName']} {x['lastName']}
                    </td>
                    <td className={'flex justify-around'}>
                      {Object.keys(volunteerRoles[x['ID']]).map((key) => {
                        return (
                          <label key={key}>
                            {roles.find(({ id }) => `${id}` === key)['name']}{' '}
                            <input
                              type="checkbox"
                              checked={volunteerRoles[x['ID']][key]}
                              onChange={(e) => {
                                handleRole(x['ID'], key, e.target.checked);
                              }}
                            />
                          </label>
                        );
                      })}
                    </td>
                  </tr>
                );
              })}
            {volunteers.length === 0 && (
              <tr key={'error'}>
                <th colSpan={2}>No volunteers available.</th>
              </tr>
            )}
          </tbody>
        </table>
      )}
      {loading > 0 && <span>Loading...</span>}
    </div>
  );
}

export default VolunteerRoles;
