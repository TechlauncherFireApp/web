import React from 'react';
import './Availability.scss';
import axios, {AxiosResponse} from 'axios';
import {backendPath} from '../../../config';
import DayPicker, {DateUtils} from "react-day-picker";
import "react-day-picker/lib/style.css";

interface State {
  // Preferred Date and Time
  selectedDays: Date[];

  allow_getPrefHours: boolean;
}

export default class Availability extends React.Component<any, State> {
  constructor(props: any) {
    super(props);
    this.handleDayClick = this.handleDayClick.bind(this);
    this.state = {
      selectedDays: [],
      allow_getPrefHours: true,
    }
  }

  // Component Methods
  // @ts-ignore
  handleDayClick(day, { selected }) {
    const selectedDays = this.state.selectedDays.concat();
    if (selected) {
      const selectedIndex = selectedDays.findIndex((selectedDay: Date) =>
        DateUtils.isSameDay(selectedDay, day)
      );
      selectedDays.splice(selectedIndex, 1);
    } else {
      selectedDays.push(day);
    }
    this.setState({ selectedDays });
  }


  // Backend Requests
    getPrefDates(): void {
    if (!this.state.allow_getPrefHours) return;
    this.setState({ allow_getPrefHours: false });

      axios
      .request({
        url: backendPath + '/volunteer/prefhours',
        method: 'GET',
        params: { volunteerID: this.props.match.params.id },
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
      .then((res: AxiosResponse): void => {

      })

  };

    exit(): void {
      window.open(
        `${window.location.origin}/volunteer/${this.props.match.params.id}`,
      '_self',
      '',
      false)
    }

  render() {
    return (
        <div>
          <div>
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

          <div>
            <button className={"type-1"} onClick={(): void => this.exit()}>
              Return
            </button>
          </div>
        </div>
  )};
}
