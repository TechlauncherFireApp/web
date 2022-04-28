import './VolunteerCalendar.scss';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import 'react-big-calendar/lib/addons/dragAndDrop/styles.css';

import moment from "moment";
import React from 'react';
import { Calendar, momentLocalizer } from "react-big-calendar";
import withDragAndDrop from "react-big-calendar/lib/addons/dragAndDrop";

const DDCalendar = withDragAndDrop(Calendar);
const localizer = momentLocalizer(moment);

const events = [
    {
        title: 'Take exam',
        start: new Date(2022, 3, 29, 1),
        end: new Date(2022, 3, 29, 12)
    },
    {
        title: 'Do audit 3',
        start: new Date(2022, 3, 29),
        end: new Date(2022, 3, 29)
    },
    {
        title: 'Study',
        start: new Date(2022, 3, 29, 13),
        end: new Date(2022, 3, 30, 12)
    }
];

const VolunteerCalendar = () => {
    return (
        <div className='calendar-body'>
            <DDCalendar
                localizer={localizer}
                startAccessor="start"
                endAccessor="end"
                style={{ height: '80vh' }}
                events={events}
                selectable={true}
            />
        </div>
    );
};

export default VolunteerCalendar;