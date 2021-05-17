import './style.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import Covid from "../Covid/covid";
import Vaccine from "../Vaccine/vaccine";
import JobKeeper from "../Job-Keeper/job-keeper";
import NotFound from "../NotFound";
import React from 'react';
import Navigation from "../Navigation/navigation";
import Header from "../Header/header"

// Material UI imports

function App() {

  return (
    <Router >
      <Header />
      <Navigation />
      <Switch>
        <Route exact path="/covid">
          <Covid />
        </Route>
        <Route exact path="/vaccine">
          <Vaccine />
        </Route>
        <Route exact path="/job-keeper">
          <JobKeeper />
        </Route>
        <Route path="*">
          <NotFound />
        </Route>
      </Switch>
      <Redirect from="/" to="covid" />
    </Router>
  );
}

export default App;
