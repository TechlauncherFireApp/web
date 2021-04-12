import React from 'react';
import './Availability.scss';
import axios, {AxiosResponse} from 'axios';
import {backendPath} from '../../../config';
import DayPicker, {DateUtils} from "react-day-picker";
// @ts-ignore
import TimeRange from 'react-timeline-range-slider';
import {endOfToday, set} from 'date-fns';


const now = new Date()
const getTodayAtSpecificHour = (hour = 12) =>
    set(now, {hours: hour, minutes: 0, seconds: 0, milliseconds: 0})

const selectedStart = getTodayAtSpecificHour()
const selectedEnd = getTodayAtSpecificHour()

const startTime = getTodayAtSpecificHour(0)
const endTime = endOfToday()

interface State {
  // Preferred Date and Time
  selectedDays: Date[];

  allow_getPrefHours: boolean;

  // State referring to TimeRange
  error: boolean;
  selectedInterval: any;
}

export default class Availability extends React.Component<any, any> {
  constructor(props: any) {
    super(props);
    this.handleDayClick = this.handleDayClick.bind(this);
    this.state = {
      selectedDays: [],
      allow_getPrefHours: true,
      error: false,
      selectedInterval: [selectedStart, selectedEnd],
    }
  }

  // Calendar Methods

  // @ts-ignore
  handleDayClick(day, {selected}) {
    const selectedDays = this.state.selectedDays.concat();
    if (selected) {
      const selectedIndex = selectedDays.findIndex((selectedDay: Date) =>
          DateUtils.isSameDay(selectedDay, day)
      );
      selectedDays.splice(selectedIndex, 1);
    } else {
      selectedDays.push(day);
    }
    this.setState({selectedDays});
  }

  // TimeRange Methods

  // @ts-ignore
  errorHandler = ({error}) => this.setState({error});

  onChangeCallback = (selectedInterval: any) => {
    this.setState({selectedInterval});
  };

  deleteAvailability = (): void => {

  }

  // Backend Requests
  getPrefDates(): void {
    if (!this.state.allow_getPrefHours) return;
    this.setState({allow_getPrefHours: false});

    axios
        .request({
          url: backendPath + '/volunteer/prefhours',
          method: 'GET',
          params: {volunteerID: this.props.match.params.id},
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        })
        .then((res: AxiosResponse): void => {

        })
  };

  patchSchedule = (): void => {

  }

  exit = (): void => {
    window.open(
        `${window.location.origin}/volunteer/${this.props.match.params.id}`,
        '_self',
        '',
        false)
  }

  render() {
    const {selectedInterval, error} = this.state;
    return (
        <availability>
          <div className="exterior">
            <div className="calendar">
              <DayPicker
                  showOutsideDays
                  showWeekNumbers
                  selectedDays={this.state.selectedDays}
                  // @ts-ignore
                  onDayClick={this.handleDayClick}
                  fromMonth={new Date()}
                  todayButton="Return to today"
              />
            </div>
            <div className="time-range">
            <TimeRange
                error={error}
                selectedInterval={selectedInterval}
                timelineInterval={[startTime, endTime]}
                onUpdateCallback={this.errorHandler}
                onChangeCallback={this.onChangeCallback}
            />
            </div>
            <div className="con">
              <button className="type-1" onClick={this.patchSchedule}>
                Save Shifts
              </button>
              <button className="type-3" onClick={this.deleteAvailability}>
                Delete Shift
              </button>
              <button className="type-2" onClick={this.exit}>
                Return
              </button>
            </div>
          </div>
        </availability>
    )
  };
}
