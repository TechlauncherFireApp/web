import './VolunteerCalendar.scss';
import 'react-big-calendar'
import 'react-big-calendar/lib/css/react-big-calendar.css';
import 'react-big-calendar/lib/addons/dragAndDrop/styles.css';

import axios from 'axios';
import moment from "moment";
import React, { useState } from 'react';
import { Calendar, momentLocalizer } from "react-big-calendar";
import withDragAndDrop from "react-big-calendar/lib/addons/dragAndDrop";

import { backendPath } from '../../config';

const DDCalendar = withDragAndDrop(Calendar);
const localizer = momentLocalizer(moment);

const user = 49;

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

/* TODO: CSS Updates
/* TODO: Update Repeat Function
/* TODO: FIX ISSUES
BUG: WEEKLY VIEW CAUSES CRASH,
Had similar issue in past
was because of using Python date's instead of JS date objects...
Repeat events cause crashes not og events
 */

/*
-------------- MAIN FUNCTION ----------------------
 */
const VolunteerCalendar = () => {

    /*
    @desc - Create a calendar event, and adds it to the backend DB
    @param - title/name of event, date as HTML date picker output, start time as an int, end time as an int
    @return - new event object, & side effect creates backend DB entry
     */
    const [eventID, setEventID] = useState('');
    function createEvent(eventTitle, eventDate, eventStartTime, eventEndTime, eventRepeatStatus, allDayStatus) {

        /* Split the date input yyyy-mm-dd into year, month, day so it can easily be used by the calendar */
        const splitDate = eventDate.split('-');
        const year = parseInt(splitDate[0]);
        const month = parseInt(splitDate[1]) - 1; /* JS Date constructor is indexed from zero (months 0-11) but HTML starts at 1 (months 1-12) so subtract 1 to account for this */
        const day = parseInt(splitDate[2]);

        /* creation of the new event object */
        let newEvent = {};
        if (allDayStatus){
            newEvent = {
            userId: user,
            title: eventTitle,
            start: new Date(year, month, day),
            end: new Date(year, month, day),
            periodicity: eventRepeatStatus
            }
        }
        else {
            newEvent = {
                userId: user,
                title: eventTitle,
                start: new Date(year, month, day, Number(eventStartTime)),
                end: new Date(year, month, day, Number(eventEndTime)),
                periodicity: eventRepeatStatus
            }
        }

        if(dateValid(newEvent.start) && (allDayStatus || newEvent.start < newEvent.end)){ /* checks if time block is valid before adding it to DB */
            axios.post(backendPath + 'unavailability/createUnavailableEvent', newEvent).then((response) => {
                setEventID(response.data['eventId']);
            });
            newEvent.eventId = eventID; /* Adds eventId to event object */
        }

        return newEvent;
    }

    /*
    * @desc - creates all the events that are repeating items
    * @param - List of events... ie EventsDB
    * @return - An array of events
    * @Notes - Implementation within main function must be followed by being parsed into setBlocks. ie setBlocks[...blocks, repeatEventsOutput]
    * */
    function repeatEvents(listOfEvents) {
         let newEvents = [];
         listOfEvents.forEach(function(element) { /* Converting date format to JS Date objects which React-Big-Calendar requires */
                switch (element.periodicity) {
                    case 1:
                        for (let i = 1; i < 90; i++) {
                            let tempStart = new Date(element.start.valueOf());
                            let tempEnd = new Date(element.end.valueOf());
                            let tempEvent = {
                                title: element.title,
                                userId: element.userId,
                                eventId: element.eventId,
                                periodicity: element.periodicity,
                                start: tempStart.setDate(tempStart.getDate() + i),
                                end: tempEnd.setDate(tempEnd.getDate() + i)
                            }

                            console.log(1);
                            newEvents.push(tempEvent);
                        }
                        break;
                    case 2:
                        for (let i = 7; i < 90; i+=7) {
                            let tempStart = new Date(element.start.valueOf());
                            let tempEnd = new Date(element.end.valueOf());
                            let tempEvent = {
                                title: element.title,
                                userId: element.userId,
                                eventId: element.eventId,
                                periodicity: element.periodicity,
                                start: tempStart.setDate(tempStart.getDate() + i),
                                end: tempEnd.setDate(tempEnd.getDate() + i)
                            }
                            newEvents.push(tempEvent);
                            console.log(tempStart);
                        }
                        break;
                    case 3:
                        for (let i = 1; i < 4; i++) {
                            let tempStart = new Date(element.start.valueOf());
                            let tempEnd = new Date(element.end.valueOf());
                            let tempEvent = {
                                title: element.title,
                                userId: element.userId,
                                eventId: element.eventId,
                                periodicity: element.periodicity,
                                start: tempStart.setMonth(tempStart.getMonth() + i),
                                end: tempEnd.setMonth(tempEnd.getMonth() + i),
                            }
                            newEvents.push(tempEvent);
                            console.log(3);
                        }
                        break;
                    default:
                        break;
                }
         });
         console.log('done');
         return newEvents;
    }

    /*
    * @desc - Allows for the deletion or editing of repeating events
    * @param - an eventID
    * @return - An array of events
    * @Notes - Implementation within main function must be followed by being parsed into setBlocks. ie setBlocks[...blocks, repeatEventsOutput]
    * */
    /* TODO
    *   function changesToRepeatingEvents(eventID) {
    *       GET removeUnavailableEvent parse eventID
    *       GET createUnavailableEvent
    *       Delete in front-end calendar (eventsDB) all events with eventID
    *       Call repeatEvents but use a list with only this changed events
    *       return new result of that repeatEvents call
    *   }
    * */

    /* --- INITIALISE --- */
    /* Load Events from database on page initial render */

    const [blocks, setBlocks] = useState('');

    React.useEffect(() => {
        axios.get(backendPath + 'unavailability/showUnavailableEvent?userId='+user).then((response) => {
            let temp = response.data;
            temp.forEach(function(element) { /* Converting date format to JS Date objects which React-Big-Calendar requires */
                // element.start = moment(element.start).toDate();
                // element.end = moment(element.end).toDate();
                element.start = new Date(element.start);
                element.end = new Date(element.end);
            });

            // Could break everything lmao
            let repeatingEvents = repeatEvents(temp);
            let initialEvents = temp.concat(repeatingEvents);
            setBlocks(initialEvents);
            //setBlocks(temp);
        });
    }, []);

    /* --- HANDLERS --- */

    /* Drag and Drop functionality */
    const handleEventChange = ({event, start, end}) => {
        const idx = blocks.indexOf(event);
        const updatedBlock = { ...event, start, end };

        /* Delete from backend DB */
        axios.get(backendPath + 'unavailability/removeUnavailableEvent?eventId=' + event.eventId + '&userId=' + event.userId).then((response) => {
                console.log(response.data[0]);
        }).catch(function (error) {
            console.log(error);
        });

        /* replace with new event in backend DB */
        axios.post(backendPath + 'unavailability/createUnavailableEvent', updatedBlock).then((response) => {
            setEventID(response.data['eventId']);
        });
        updatedBlock.eventId = eventID;

        /* Update Frontend Calendar */
        const blocksToChange = [...blocks];
        blocksToChange.splice(idx, 1, updatedBlock);

        setBlocks(blocksToChange);
    }

    /* Init the variables for the form (stateful) */
    const [state, setState] = useState({
        title: "",
        startTime: "",
        endTime: "",
        repeat: "0",
        allDay: false,
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
    };

    const hidden = state.allDay ? 'hidden' : ''; /* for hiding the time inputs */

    /* Form submission functionality */
    function submit(e) {
        e.preventDefault();

        /* create new event */
        let newBlock = createEvent(state.title, state.date, state.startTime, state.endTime, state.repeat, state.allDay);

        if (dateValid(newBlock.start)) { /* If date value is valid and start time is before end time*/
            if (state.allDay || (newBlock.start < newBlock.end)) {
                setBlocks([...blocks, newBlock]); /* add new event to calendar (frontend)*/
            }
        }

        console.log(blocks);
    }

    /* This is the event handler for clicking on a time block */
    const handleSelectedEvent = (event) => {
        let i = blocks.indexOf(event); /* Find index of event that has been clicked on in the array */
        if (confirm("Delete " + event.title)) { /* JS Confirmation window prompt, returns true if yes is clicked */

            /* Delete from backend DB */
            axios.get(backendPath + 'unavailability/removeUnavailableEvent?eventId=' + event.eventId + '&userId=' + event.userId).then((response) => {
                console.log(response.data[0]);
            });

            /* Update frontend calendar */
            let blocksToChange = [...blocks];
            blocksToChange.splice(i, 1); /* remove event from array */
            setBlocks(blocksToChange);
        }
    }
    /* NOTE: Alternative to the JS confirmation window we could also do a React popup/modal, this is significantly more complicated but would allow for the implementation of editing name/recurring. For now we shall leave like this, but it is a possible future improvement for sure... */

    /* HTML OF PAGE */
    return (
        <div className='grid-container'>

            {/* Header */}
            <div className='calHeader'>
                <h1>Calendar</h1>
                {/* FUTURE: I  want to change this to "User X's Calendar" */}
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

                    {/* Checkbox for all day events */}
                    <div className="form-group">
                        <label htmlFor={'allday'}>Toggle All Day:</label>
                        <input
                            type="checkbox"
                            name="allDay"
                            checked={state.allDay}
                            onChange={(handleChange)}
                        />
                   </div>

                    {/* Repeating Options */}
                    <div className="form-group">
                      <label htmlFor="repeat">Repeats:</label>
                      <select id="repeats" name="repeat"
                        value={state.repeat}
                        onChange={handleChange}>
                        <option value="0">None</option>
                        <option value="1">Daily</option>
                        <option value="2">Weekly</option>
                        <option value="3">Monthly</option>v
                      </select>
                    </div>

                    <div className={hidden}> {/* For hiding this when all day is pressed */}
                        {/* Start Time*/}
                        <div className="form-group">
                          <label htmlFor="startTime">Choose a Start Time:</label>
                          <select id="startTime" name="startTime"
                            value={state.startTime}
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
                          </select>
                        </div>

                        {/* ISSUE: Could not get half hour options to work. */}

                        {/* End Time*/}
                        <div className="form-group">
                          <label htmlFor="endTime">Choose a End Time:</label>
                          <select id="endTime" name="endTime"
                            value={state.endTime}
                            onChange={handleChange}>
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
                    </div>

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