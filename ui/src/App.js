// import 'bootstrap/dist/css/bootstrap.min.css';

import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import NavBar from "./components/Navbar/navbar";
import Sidebar from "./components/Sidebar/sidebar";
import AssetRequestVehicle from './routes/AssetRequestVehicle/AssetRequestVehicle';
import AssetRequestVolunteers from './routes/AssetRequestVolunteers/assetRequestVolunteers';
import AssetTypeRoles from './routes/AssetTypeRoles';
import Forgot from "./routes/Authentication/forgot";
import Login from './routes/Authentication/login';
import Logout from './routes/Authentication/logout';
import Register from './routes/Authentication/register';
import Reset from './routes/Authentication/reset';
import Verify from "./routes/Authentication/verify";
import BrigadeCaptainHome from './routes/BrigadeCaptainHome/brigadeCaptainHome';
import Configuration from "./routes/Configuration/configuration";
import Home from './routes/Home/Home';
import QuizMainPage from "./routes/QuizMainPage/QuizMainPage";
import QuizQuestions from "./routes/QuizQuestions/QuizQuestions";
import QuizResult from './routes/QuizResult/QuizResult';
import AssetTypes from './routes/Reference/assetTypes';
import Qualifications from './routes/Reference/qualifications';
import Roles from './routes/Reference/roles';
import UserPrivileges from './routes/UserPrivileges';
import VolunteerRoles from './routes/VolunteerRoles';
import Availability from './routes/Volunteers/Availability/Availability';
import Volunteer from './routes/Volunteers/volunteer';
import VolunteersContainer from './routes/Volunteers/volunteersContainer';


export default function App() {
  return (
      <div style={{display: 'flex', flexDirection: 'column'}}>
    <BrowserRouter>
      <NavBar />
      <div style={{display: 'flex', flexDirection: 'row'}}>
        <Sidebar/>
      <div className={'main-body'}>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/login" component={Login} />
          <Route exact path="/logout" component={Logout} />
          <Route exact path="/register" component={Register} />
          <Route exact path="/forgot" component={Forgot} />
          <Route exact path="/verify" component={Verify} />
          <Route exact path="/reset" component={Reset} />
          <Route exact path="/reference/roles" component={Roles} />
          <Route exact path="/reference/qualifications" component={Qualifications}/>
          <Route exact path="/reference/asset_types" component={AssetTypes} />
          <Route exact path="/captain" component={BrigadeCaptainHome} />
          <Route exact path="/assetRequest/vehicles/:id" component={AssetRequestVehicle} />
          <Route exact path="/assetRequest/volunteers/:id" component={AssetRequestVolunteers} />
          <Route exact path="/volunteer" component={VolunteersContainer} />
          <Route exact path="/volunteer-roles" component={VolunteerRoles} />
          <Route exact path="/asset-type-roles" component={AssetTypeRoles} />
          <Route exact path="/user-privileges" component={UserPrivileges} />
          <Route exact path="/volunteer/:id" component={Volunteer} />
          <Route exact path="/volunteer/:id/availability" component={Availability} />
          <Route exact path="/tenancy-configs" component={Configuration} />
          <Route exact path="/quiz" component={QuizMainPage} />
          <Route path={"/questions"} component={QuizQuestions} />
          <Route path={"/quiz-result"} component={QuizResult} />
        </Switch>
      </div>
      </div>
    </BrowserRouter>
        </div>
  );
}
