import React from 'react';
import './Availability.scss';
import axios, {AxiosError, AxiosResponse} from 'axios';
import {backendPath} from '../../../config';
import DayPicker from "react-day-picker";
// @ts-ignore
import TimeRange from 'react-timeline-range-slider';
import {endOfToday, getDay, getHours, getMinutes, set} from 'date-fns';
import {contains} from "../../../common/functions";

type Day =
    | 'Sunday'
    | 'Monday'
    | 'Tuesday'
    | 'Wednesday'
    | 'Thursday'
    | 'Friday'
    | 'Saturday';
type Schedule = { [key in Day]: number[][] };


// States for TimeRange
const now = new Date()
const getTodayAtSpecificHour = (hour = 12, minutes = 0) =>
    set(now, {hours: hour, minutes: minutes, seconds: 0, milliseconds: 0})
const getSelectedAtSpecificHour = (date: Date, hour = 12, minutes = 0) =>
    set(date, {hours: hour, minutes: minutes, seconds: 0, milliseconds: 0})

const selectedStart = getTodayAtSpecificHour()
const selectedEnd = getTodayAtSpecificHour(12, 30)

const startTime = getTodayAtSpecificHour(0)
const endTime = endOfToday()

const modifierStyles = {
    previous: {
        color: '#000000',
        backgroundColor: '#ffb3b3',
    },
}

interface State {
    // Calendar state
    modifiedDays: [];
    selectedDay?: Date;
    modifiers: {},

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
    previousIntervals: { start: Date, end: Date }[];
}

export default class Availability extends React.Component<any, State> {
    constructor(props: any) {
        super(props);
        this.handleDayClick = this.handleDayClick.bind(this);
        this.state = {
            modifiedDays: [],
            selectedDay: undefined,
            allow_getPrefHours: true,
            allow_patchPrefHours: true,
            allow_getSchedule: true,
            allow_patchSchedule: true,
            error: false,
            selectedInterval: [selectedStart, selectedEnd],
            previousIntervals: [],
            modifiers: { previous: new Date(),}
        }
    }

    componentDidMount(): void {
        this.getPrefHours();
        this.getSchedule();
    }

    // Calendar Methods

    // @ts-ignore
    handleDayClick(day, {selected}) {
        this.setState({
            selectedDay: selected ? undefined : day,
        }, () => {
            this.displaySchedule();
        });
    }

    // TimeRange Methods

    displaySchedule() {
        if (this.state.schedule && contains(this.state.schedule) && this.state.selectedDay && contains(this.state.selectedDay)) {
            let selected = this.state.selectedDay;
            let k: Day = this.convertNumToDay(getDay(selected));
            let s: Schedule = this.state.schedule;
            let prevIntervals: { start: Date, end: Date }[] = [];
            for (let l of s[k]) {
                let startTime: [number, number] = this.convertNumToTime(l[0]);
                let startInterval = getSelectedAtSpecificHour(now, startTime[0], startTime[1]);
                let endTime: [number, number] = this.convertNumToTime(l[1]);
                let endInterval = getSelectedAtSpecificHour(now, endTime[0], endTime[1]);
                let interval = {start: startInterval, end: endInterval};
                prevIntervals = prevIntervals.concat(interval);
                this.addModifiedDay(k);
            }
            this.setState({selectedInterval: [selectedStart, selectedEnd]})
            this.setState({previousIntervals: prevIntervals});
        }
    }

    displayModifiedDays() {
        let modified = this.state.modifiedDays;
        let numberDay: number;
        let arrDays: number[] = [];
        for (let i: number = 0; i < modified.length; i++) {
            if (JSON.stringify(modified[i]) === JSON.stringify("Sunday")) {
                numberDay = 0;
            } if (JSON.stringify(modified[i]) === JSON.stringify("Monday")) {
                numberDay = 1;
            } if (JSON.stringify(modified[i]) === JSON.stringify("Tuesday")) {
                numberDay = 2;
            } if (JSON.stringify(modified[i]) === JSON.stringify("Wednesday")) {
                numberDay = 3;
            } if (JSON.stringify(modified[i]) === JSON.stringify("Thursday")) {
                numberDay = 4;
            } if (JSON.stringify(modified[i]) === JSON.stringify("Friday")) {
                numberDay = 5;
            } if (JSON.stringify(modified[i]) === JSON.stringify("Saturday")) {
                numberDay = 6
            }
            // @ts-ignore
            arrDays = arrDays.concat(numberDay);
        }
        let mod = {
        previous: {daysOfWeek: arrDays},
        };
        console.log(arrDays);
        this.setState({modifiers: mod});
    }

    // Converts float value to the nearest half hour interval (6.5 becomes [6, 30])
    convertNumToTime(n: number): [number, number] {
        let hour = Math.floor(n);
        let minutes = n - hour;
        if (minutes > 0.1) {
            minutes = 30;
        }
        return [hour, minutes];
    }

    // Converts number representation of weekday to the day
    convertNumToDay(n: number): Day {
        if (n === 0) return 'Sunday';
        if (n === 1) return 'Monday';
        if (n === 2) return 'Tuesday';
        if (n === 3) return 'Wednesday';
        if (n === 4) return 'Thursday';
        if (n === 5) return 'Friday';
        return 'Saturday';
    }

    getModifiedDays = (): void => {
        if (this.state.schedule && contains(this.state.schedule)) {
            let s: Schedule = this.state.schedule;
            let modified: Day[] = [];
            for (let key in s) {
                // @ts-ignore
                let val = s[key];
                if (val.length > 0) {
                    // @ts-ignore
                    modified = modified.concat(key)
                }
            }
            // @ts-ignore
            this.setState({modifiedDays: modified}, (): void => {
                this.displaySchedule();
                this.displayModifiedDays();
            })
        }
    }

    addModifiedDay(day: Day) {
        let modified = this.state.modifiedDays;
        // @ts-ignore
        if (modified.includes(day)) {
            return;
        }
        // @ts-ignore
        modified = modified.concat(day);
        console.log(modified);
        this.setState({modifiedDays: modified}, (): void => {
            this.displaySchedule();
            this.displayModifiedDays();
        })
    }

    removeModifiedDay(day: Day) {
        let modified = this.state.modifiedDays;
        // @ts-ignore
        let index = modified.indexOf(day);
        if (index > -1) {
            // @ts-ignore
            modified.splice(index, 1);
        }
        this.setState({modifiedDays: modified}, (): void => {
            this.displaySchedule();
            this.displayModifiedDays();
        });
    }

    // @ts-ignore
    errorHandler = ({error}) => this.setState({error});

    onChangeCallback = (selectedInterval: any) => {
        this.setState({selectedInterval});
    };

    addAvailability = (): void => {
        if (this.state.schedule && contains(this.state.schedule) && this.state.selectedDay && contains(this.state.selectedDay)) {
            let interval = this.state.selectedInterval;
            let startAvailability: number = this.convertDateToNum(interval[0]);
            let endAvailability: number = this.convertDateToNum(interval[1]);
            let availability: number[] = [startAvailability, endAvailability];
            let k: Day = this.convertNumToDay(getDay(this.state.selectedDay));
            let s: Schedule = this.state.schedule;
            let i: number = s[k].length;
            s[k][i] = availability;
            this.setState({schedule: s}, (): void => {
                this.displaySchedule();
            });
        }
    }

    deleteAvailability = (): void => {
        if (this.state.schedule && contains(this.state.schedule) && this.state.selectedDay && contains(this.state.selectedDay)) {
            let k: Day = this.convertNumToDay(getDay(this.state.selectedDay));
            let s: Schedule = this.state.schedule;
            s[k] = [];
            this.setState({schedule: s}, (): void => {
                this.displaySchedule();
            });
            this.removeModifiedDay(k);
        }
    }

    convertDateToNum(d: Date): number {
        let hour = getHours(d);
        let minutes = getMinutes(d);
        if (minutes > 0) {
            minutes = 0.5;
        }
        return hour + minutes;
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
                    this.getModifiedDays();
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
        const {selectedInterval, previousIntervals, error} = this.state;
        return (
            <availability>
                <div className="exterior">
                    <div className="calendar">
                        <DayPicker
                            showWeekNumbers
                            selectedDays={this.state.selectedDay}
                            // @ts-ignore
                            onDayClick={this.handleDayClick}
                            fromMonth={new Date()}
                            todayButton="Return to today"
                            modifiers={this.state.modifiers}
                            modifiersStyles={modifierStyles}
                        />
                    </div>
                    <div className="time-range">
                        <TimeRange
                            error={error}
                            selectedInterval={selectedInterval}
                            timelineInterval={[startTime, endTime]}
                            onUpdateCallback={this.errorHandler}
                            onChangeCallback={this.onChangeCallback}
                            disabledIntervals={previousIntervals}
                        />
                    </div>
                    <div className="hours">
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
                        <button className="type-3" onClick={this.addAvailability}>
                            Add Availability
                        </button>
                        <button className="type-3" onClick={this.deleteAvailability}>
                            Delete Availabilities For This Day
                        </button>
                        <div className="con-2">
                            <button className="type-1" onClick={(): void => {
                                this.patchPrefHours();
                                this.patchSchedule();
                            }}>
                                {this.state.allow_patchSchedule ? 'Save All' : 'Loading'}
                            </button>
                            <button className="type-2" onClick={this.exit}>
                                Return
                            </button>
                        </div>
                    </div>
                </div>
            </availability>
        )
    };
}
