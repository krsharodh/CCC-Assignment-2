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

import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';

// Material UI imports

const drawerWidth = 150;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  // necessary for content to be below app bar
  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
  container: {
    backgroundColor: "rgb(0 0 0 / 6 %)"
  }
}));

function App() {

  const classes = useStyles();

  return (
    <Router >
      <div className={classes.root}>
        <CssBaseline />
        <Header />
        <Navigation />

        <main className={classes.content}>
          <div className={classes.toolbar} />
          <div className="container">
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
          </div>
        </main>
      </div>


      <Redirect from="/" to="covid" />
    </Router>
  );
}

export default App;
