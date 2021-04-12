import React from 'react';
import './Availability.scss';
import axios, {AxiosError, AxiosResponse} from 'axios';
import {backendPath} from '../../../config';
import DayPicker, {DateUtils} from "react-day-picker";
// @ts-ignore
import TimeRange from 'react-timeline-range-slider';
import {endOfToday, set} from 'date-fns';
import {contains} from "../../../common/functions";

type Day =
    | 'Monday'
    | 'Tuesday'
    | 'Wednesday'
    | 'Thursday'
    | 'Friday'
    | 'Saturday'
    | 'Sunday';
type Schedule = { [key in Day]: number[][] };

const now = new Date()
const getTodayAtSpecificHour = (hour = 12) =>
    set(now, {hours: hour, minutes: 0, seconds: 0, milliseconds: 0})

const selectedStart = getTodayAtSpecificHour()
const selectedEnd = getTodayAtSpecificHour()

const startTime = getTodayAtSpecificHour(0)
const endTime = endOfToday()

interface State {
  // Calendar state
  selectedDays: Date[];

  // Preferred Date and Time
  prefHours?: number;
  allow_getPrefHours: boolean;
  allow_patchPrefHours: boolean;

  // Availability
  schedule?: Schedule;
  allow_getSchedule: boolean;
  allow_patchSchedule: boolean;
  // State referring to TimeRange
  error: boolean;
  selectedInterval: any;
}

export default class Availability extends React.Component<any, State> {
  constructor(props: any) {
    super(props);
    this.handleDayClick = this.handleDayClick.bind(this);
    this.state = {
      selectedDays: [],
      allow_getPrefHours: true,
      allow_patchPrefHours: true,
      allow_getSchedule: true,
      allow_patchSchedule: true,
      error: false,
      selectedInterval: [selectedStart, selectedEnd],
    }
  }

  componentDidMount(): void {
    this.getPrefHours();
    this.getSchedule();
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
  getPrefHours(): void {
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
          console.log(res.data);
          if (typeof res.data === 'object' && res.data['success']) {
            this.setState({prefHours: res.data['prefHours'] as number})
          } else alert('Request Failed');
          this.setState({allow_getPrefHours: true});
        })
        .catch((err: AxiosError): void => {
          // @ts-ignore
          if (err.response.status === 401) {
            this.props.history.push('/login');
          } else {
            alert(err.message);
            this.setState({allow_getPrefHours: true});
          }
        });
  };

  getSchedule(): void {
    if (!this.state.allow_getSchedule) return;
    this.setState({allow_getSchedule: false});

    axios
        .request({
          url: backendPath + '/volunteer/availability',
          method: 'GET',
          params: {volunteerID: this.props.match.params.id},
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        })
        .then((res: AxiosResponse): void => {
          if (typeof res.data === 'object' && res.data['success']) {
            let n: Schedule = res.data['availability'] as Schedule;
            this.setState({schedule: n});
          } else alert('Request Failed');
          this.setState({allow_getSchedule: true});
        })
        .catch((err: AxiosError): void => {
          // @ts-ignore
          if (err.response.status === 401) {
            this.props.history.push('/login');
          } else {
            alert(err.message);
            this.setState({allow_getSchedule: true});
          }
        });
  }

  patchPrefHours = (): void => {
    if (
        !this.state.allow_patchPrefHours ||
        !contains(this.state.allow_patchPrefHours)
    ) return;
    this.setState({allow_patchPrefHours: false})

    axios
        .request({
          url: backendPath + '/volunteer/prefhours',
          method: 'PATCH',
          params: {
            volunteerID: this.props.match.params.id,
            prefHours: Number(this.state.prefHours),
          },
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        })
        .then((res: AxiosResponse): void => {
          // console.log(res.data);
          alert(res.data['success'] ? 'Updated - prefHours' : 'Request Failed');
          this.setState({allow_patchPrefHours: true});
        })
        .catch((err: AxiosError): void => {
          // @ts-ignore
          if (err.response.status === 401) {
            this.props.history.push('/login');
          } else {
            alert(err.message);
            this.setState({allow_patchPrefHours: true});
          }
        });
  }

  patchSchedule = (): void => {
    if (
        !this.state.allow_patchSchedule ||
        !contains(this.state.schedule)
    ) return;
    this.setState({allow_patchSchedule: false});
    axios
        .request({
          url: backendPath + '/volunteer/availability',
          method: 'PATCH',
          params: {volunteerID: this.props.match.params.id},
          data: {availability: this.state.schedule},
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        })
        .then((res: AxiosResponse): void => {
          alert(
              res.data['success'] ? 'Updated - Availability' : 'Request Failed'
          );
          this.setState({allow_patchSchedule: true});
        })
        .catch((err: AxiosError): void => {
          // @ts-ignore
          if (err.response.status === 401) {
            this.props.history.push('/login');
          } else {
            alert(err.message);
            this.setState({allow_patchSchedule: true});
          }
        });
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
            <div className="time-range">
              <p className="sen">Preferred number of hours per week:</p>
              <input
                  type="number"
                  placeholder="Select PrefHours"
                  title="Set PrefHours"
                  value={this.state.prefHours}
                  onChange={(e: any): void =>
                      this.setState({prefHours: Number(e.target.value)})
                  }
              />
            </div>
            <div className="con">
              <button className="type-1" onClick={(): void => {
                this.patchPrefHours();
                this.patchSchedule();
              }}>
                {this.state.allow_patchSchedule ? 'Save Availability & Preferred Hours' : 'Loading'}
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
