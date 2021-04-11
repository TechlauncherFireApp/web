import React from 'react';
import './Availability.scss';
import axios, { AxiosResponse, AxiosError } from 'axios';
import { contains, att } from '../../../common/functions';
import { backendPath } from '../../../config';
import DayPicker, { DateUtils } from "react-day-picker";
import "react-day-picker/lib/style.css";
import moment from "moment";
import { Helmet } from "react-helmet";

export default class Availability extends React.Component {
  render() {
    return <DayPicker />
  };
}
