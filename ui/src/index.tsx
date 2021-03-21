import React from 'react';
import ReactDOM from 'react-dom';
import './index.scss';
import App from './App';
import * as serviceWorker from './serviceWorker';
import axios from "axios";

axios.defaults.baseURL = "http://localhost:5000/";

declare global {
  namespace JSX {
    interface IntrinsicElements {
      // Main
      "main-body": React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
      home: React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;

      // Page :- Brigade Captain Home
      brigadeCaptainHome: React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;

      // Page :- AssetRequestVehicle
      "asset-request-vehicle": React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
      insert: React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
      "request-body": React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;

      // Page :- Volunteer Availability
      availability: React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
    }
  }
}

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.querySelector("app-root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
