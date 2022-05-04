import './VolunteerCalendar.scss';
import 'react-big-calendar'
import 'react-big-calendar/lib/css/react-big-calendar.css';
import 'react-big-calendar/lib/addons/dragAndDrop/styles.css';

import moment from "moment";
import React, { useState } from 'react';
import { Calendar, momentLocalizer } from "react-big-calendar";
import withDragAndDrop from "react-big-calendar/lib/addons/dragAndDrop";

const DDCalendar = withDragAndDrop(Calendar);
const localizer = momentLocalizer(moment);

const eventsDB = [
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

/*
@desc - Create a calendar event, and TODO adds it to the backend DB
@param - title/name of event, date as a HTML date picker output, start time as a int, end time as an int
@return - new event object, & TODO side effect creates backend DB entry
 */
function createEvent(eventTitle, eventDate, eventStartTime, eventEndTime) {

    /* Split the date input yyyy-mm-dd into year, month, day so it can easily be used by the calendar */
    const splitDate = eventDate.split('-') ;
    const year = parseInt(splitDate[0]);
    const month = parseInt(splitDate[1]) - 1; /* JS Date constructor is indexed from zero (months 0-11) but HTML starts at 1 (months 1-12) so subtract 1 to account for this */
    const day = parseInt(splitDate[2]);

    /* creation of the new event object */
    let newEvent =  {
        title: eventTitle,
        start: new Date(year, month, day, Number(eventStartTime)),
        end:  new Date(year, month, day, Number(eventEndTime))
    }

    /* This updated the eventsDB array however, that is only used for initial state not updating the calendar. When we integrate with backend we may have to rethink implementation
    if(dateValid(newEvent.start) && newEvent.start< newEvent.end){
        eventsDB.push(newEvent)
    } Option : Rather than a side effect this could be its own function that gets called separately
    */

    return newEvent;
}

/*
@desc - TODO: When page loads or it refreshes it fills calendar from backend using the create event function - Integration!
function pullCalendar() {
   1. Request all events from backend DB
   2. eventsDB.push() each item...
}
*/

/*
@desc - Check if JS Date object is a valid date
@param - date, a js date object
@return - boolean
 */
function dateValid(date) {
    if (date instanceof Date && !isNaN(date.valueOf())) {
        return true;
    }
    return false;
}

/*
MAIN FUNCTION
 */
const VolunteerCalendar = () => {
    /* Init state for calendar */
    const [blocks, setBlocks] = useState(eventsDB);

    /* Drag and Drop functionality */
    const handleEventChange = ({event, start, end}) => {
        const idx = blocks.indexOf(event);
        const updatedBlock = { ...event, start, end };

        const blocksToChange = [...blocks];
        blocksToChange.splice(idx, 1, updatedBlock);

        setBlocks(blocksToChange);
    }

    /* Init the variables for the form (stateful) */
    const [state, setState] = useState({
        title: "",
        startTime: "",
        endTime: "",
        reoccur: false,
        date: "",
    });

    /* Function handles changes to the state of the form */
    const handleChange = e => {
        console.log(state);

        /* Sets the state based on changes */
        setState({
            ...state,
            [e.target.name]: e.target.type === "checkbox" ? e.target.checked : e.target.value, /* Check boxes require a different value than other values, this allows for that. Otherwise would just use "[e.target.name]: e.target.value" */
        });

        /* TODO: Update backend */
    };

    /* Form submission functionality */
    function submit(e) {
        e.preventDefault();

        /* create new event */
        let newBlock = createEvent(state.title, state.date, state.startTime, state.endTime);

        if (dateValid(newBlock.start) && (newBlock.start < newBlock.end)) { /* If date value is valid and start time is before end time*/
            setBlocks([...blocks, newBlock]); /* add new event to calendar */
        }
    }

    /* This is the event handler for clicking on a timeblock */
    const handleSelectedEvent = (event) => {
        let i = blocks.indexOf(event); /* Find index of event that has been clicked on in the array */
        if (confirm("Delete " + event.title)) { /* JS Confirmation window prompt, returns true if yes is clicked */
            let blocksToChange = [...blocks];
            blocksToChange.splice(i, 1); /* remove event from array */
            setBlocks(blocksToChange);
        }
        /* TODO: Delete from backend */
    }
    /* NOTE: Alternative to the JS confirmation window we could also do a React popup/modal, this is significantly more complicated but would allow for the implementation of editing name/recurring.
    For now we shall leave like this, but it is a possible future improvement for sure...
     */

    /* HTML OF PAGE */
    return (
        <div className='grid-container'>

            {/* Header */}
            <div className='calHeader'>
                <h1>Header</h1>
            </div>

            {/* Calendar */}
            <div className='calendar-body'>
                <DDCalendar
                    localizer={localizer}
                    startAccessor="start"
                    endAccessor="end"
                    style={{ height: '80vh' }}
                    events={blocks}
                    selectable={true}
                    onEventDrop={handleEventChange}
                    onEventResize={handleEventChange}
                    onSelectEvent={handleSelectedEvent} /* Event for when timeblock is clicked on */
                />
            </div>

            {/* SideBar / Form */}
            <div className='calForm'>

                {/* Border and styling of the form */}
                <form
                    className={'mt6 w-75 ml-auto mr-auto ba br2 b--black-10 pa2'}
                    onSubmit={submit}>
                    {/* Calls submit function when submit button at bottom of form is pressed */}


                    {/* Heading of form */}
                    <h2>Enter your unavailability</h2>

                    {/* Textbox for timeslot/block name/title */}
                    <div className="form-group">
                        <label htmlFor={'Name'}>Title: </label>
                        <input
                            className={'form-control'}
                            type="text"
                            name="title"
                            value={state.title}
                            onChange={handleChange}
                        />
                    </div>

                    {/* Checkbox for recurring events */}
                    <div className="form-group">
                        <label htmlFor={'givenName'}>Recurring:</label>
                        <input
                            type="checkbox"
                            name="reoccur"
                            checked={state.reoccur}
                            onChange={(handleChange)}
                        />
                   </div>

                    {/* Start Time*/}
                    <div className="form-group">
                      <label htmlFor="startTime">Start Time:</label>
                      <select id="startTime" name="startTime"
                        value={state.startTime}
                        onChange={handleChange}>
                        <option value="0">12:00 AM</option>
                        <option value="0.5">12:30 AM</option>
                        <option value="1">1:00 AM</option>
                        <option value="2">2:00 AM</option>
                        <option value="3">3:00 AM</option>
                        <option value="4">4:00 AM</option>
                        <option value="5">5:00 AM</option>
                        <option value="6">6:00 AM</option>
                        <option value="7">7:00 AM</option>
                        <option value="8">8:00 AM</option>
                        <option value="9">9:00 AM</option>
                        <option value="10">10:00 AM</option>
                        <option value="11">11:00 AM</option>
                        <option value="12">12:00 AM</option>
                        <option value="13">1:00 PM</option>
                        <option value="14">2:00 PM</option>
                        <option value="15">3:00 PM</option>
                        <option value="16">4:00 PM</option>
                        <option value="17">5:00 PM</option>
                        <option value="18">6:00 PM</option>
                        <option value="19">7:00 PM</option>
                        <option value="20">8:00 PM</option>
                        <option value="21">9:00 PM</option>
                        <option value="22">10:00 PM</option>
                        <option value="23">11:00 PM</option>
                        <option value="24">12:00 PM</option>
                      </select>
                    </div>

                    {/* End Time*/}
                    <div className="form-group">
                      <label htmlFor="endTime">Choose a End Time:</label>
                      <select id="endTime" name="endTime"
                        value={state.endTime}
                        onChange={handleChange}>
                        <option value="0">12:00 AM</option>
                        <option value="1">1:00 AM</option>
                        <option value="2">2:00 AM</option>
                        <option value="3">3:00 AM</option>
                        <option value="4">4:00 AM</option>
                        <option value="5">5:00 AM</option>
                        <option value="6">6:00 AM</option>
                        <option value="7">7:00 AM</option>
                        <option value="8">8:00 AM</option>
                        <option value="9">9:00 AM</option>
                        <option value="10">10:00 AM</option>
                        <option value="11">11:00 AM</option>
                        <option value="12">12:00 AM</option>
                        <option value="13">1:00 PM</option>
                        <option value="14">2:00 PM</option>
                        <option value="15">3:00 PM</option>
                        <option value="16">4:00 PM</option>
                        <option value="17">5:00 PM</option>
                        <option value="18">6:00 PM</option>
                        <option value="19">7:00 PM</option>
                        <option value="20">8:00 PM</option>
                        <option value="21">9:00 PM</option>
                        <option value="22">10:00 PM</option>
                        <option value="23">11:00 PM</option>
                        <option value="24">12:00 PM</option>
                      </select>
                    </div>
                    {/* HTML's time picker component has terrible browser compatibility and even worse react compatibility so we are using a select box but we could instead import a custom react component */}

                    {/* Date */}
                    <div className="form-group">
                      <label htmlFor="startTime">Choose a Date:</label>
                      <input type="date" id="date" name="date"
                        value={state.date}
                        onChange={handleChange}
                    />
                    </div>

                    {/* Submit Button */}
                    <input
                      type="submit"
                      value="Submit"
                      className={'btn bg-light-red pv2 ph3 br2 b near-white dim'}
                    />
                </form>
            </div>
        </div>
    );
};

export default VolunteerCalendar;