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
import Cover from "../Cover/cover"

import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';

import { useState, useEffect } from 'react';

import { GetCities, GetCovidGraph1Data, GetCovidGraph2Data, GetCovidTopicsData, GetCovidHashtagsData, GetCovidMapData } from "../agent";
import { GetVaccineGraph1Data, GetVaccineGraph2Data, GetVaccineGraph3Data, GetVaccineGraph4Data, GetVaccineGraph5Data } from "../agent";
import { GetJobGraph1Data, GetJobGraph2Data, GetJobGraph3Data } from "../agent";


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
    backgroundColor: "rgba(0, 0, 0, 0.08)"
  }
}));

function App() {

  const classes = useStyles();

  const [showGetStarted, setShowGetStarted] = useState(true);

  const [areasList, setAreasList] = useState([]);
  const [selectedArea, setSelectedArea] = useState(0);
  const [covidGraph1Data, setCovidGraph1Data] = useState([]);
  const [covidGraph2Data, setCovidGraph2Data] = useState([]);
  const [covidTopicsData, setCovidTopicsData] = useState([]);
  const [covidHashtagsData, setCovidHashtagsData] = useState([]);
  const [covidMapData, setCovidMapData] = useState([]);

  const [vaccineGraph1Data, setVaccineGraph1Data] = useState([]);
  const [vaccineGraph2Data, setVaccineGraph2Data] = useState([]);
  const [vaccineGraph3Data, setVaccineGraph3Data] = useState([]);
  const [vaccineGraph4Data, setVaccineGraph4Data] = useState([]);
  const [vaccineGraph5Data, setVaccineGraph5Data] = useState([]);

  const [jobGraph1Data, setJobGraph1Data] = useState([]);
  const [jobGraph2Data, setJobGraph2Data] = useState([]);
  const [jobGraph3Data, setJobGraph3Data] = useState([]);


  const handleGetStarted = () => {
    setShowGetStarted(false);

    getCities()

    // Covid
    getCovidGraph1Data();
    getCovidTopicsData();
    getCovidHashtagsData();
    getCovidMapData();

    //Vaccine
    getVaccineGraph1Data();
    getVaccineGraph2Data();
    getVaccineGraph3Data();
    getVaccineGraph4Data();
    getVaccineGraph5Data();

    // Job Keeper
    getJobGraph1Data();
    getJobGraph2Data();
    getJobGraph3Data();
  }

  const getCities = async () => {
    console.log(areasList);
    let responseJson = await GetCities();
    setAreasList(responseJson);
    setSelectedArea(responseJson[0]["value"]);
    getCovidGraph2Data(responseJson[0]["value"]);
  }

  const getCovidGraph1Data = async () => {
    let responseJson = await GetCovidGraph1Data();
    responseJson = responseJson.map(el => ({
      ...el,
      percentage: ((el.metioned_covid / el.total_tweets) * 100).toFixed(2)
    }))
    setCovidGraph1Data(responseJson);
  }

  const getCovidGraph2Data = async (city) => {
    const responseJson = await GetCovidGraph2Data(city);
    setCovidGraph2Data(responseJson);
  }

  const getCovidTopicsData = async () => {
    const responseJson = await GetCovidTopicsData();
    setCovidTopicsData(responseJson);
  }

  const getCovidHashtagsData = async () => {
    const responseJson = await GetCovidHashtagsData();
    setCovidHashtagsData(responseJson);
  }

  const getCovidMapData = async () => {
    const responseJson = await GetCovidMapData();
    setCovidMapData(responseJson);
  }

  const handleAreaChange = (event) => {
    setSelectedArea(event.target.value);
    getCovidGraph2Data(event.target.value);
  };

  const getVaccineGraph1Data = async () => {
    let responseJson = await GetVaccineGraph1Data();
    responseJson = responseJson.map(el => ({
      ...el,
      percentage: ((el.metioned_vaccine / el.total_tweets) * 100).toFixed(2)
    }))
    setVaccineGraph1Data(responseJson);
  }

  const getVaccineGraph2Data = async () => {
    let responseJson = await GetVaccineGraph2Data();
    responseJson = responseJson.map(el => ({
      ...el,
      percentage: ((el.metioned_vaccine / el.total_tweets) * 100).toFixed(2)
    }))
    setVaccineGraph2Data(responseJson);
  }

  const getVaccineGraph3Data = async () => {
    let responseJson = await GetVaccineGraph3Data();
    setVaccineGraph3Data(responseJson);
  }

  const getVaccineGraph4Data = async () => {
    let responseJson = await GetVaccineGraph4Data();
    setVaccineGraph4Data(responseJson);
  }

  const getVaccineGraph5Data = async () => {
    let responseJson = await GetVaccineGraph5Data();
    setVaccineGraph5Data(responseJson);
  }

  const getJobGraph1Data = async () => {
    let responseJson = await GetJobGraph1Data();
    responseJson = responseJson.map(el => ({
      ...el,
      percentage: ((el.metioned_jobkeeper / el.total_tweets) * 100).toFixed(2)
    }))
    setJobGraph1Data(responseJson);
  }

  const getJobGraph2Data = async () => {
    let responseJson = await GetJobGraph2Data();
    responseJson = responseJson.map(el => ({
      ...el,
      percentage: ((el.metioned_jobkeeper / el.total_tweets) * 100).toFixed(2)
    }))
    setJobGraph2Data(responseJson);
  }

  const getJobGraph3Data = async () => {
    let responseJson = await GetJobGraph3Data();
    responseJson = responseJson.map(el => ({
      ...el,
      percentage: ((el.metioned_jobkeeper / el.total_tweets) * 100).toFixed(2)
    }))
    setJobGraph3Data(responseJson);
  }


  return (
    showGetStarted
      ? <Cover handleGetStarted={handleGetStarted} />
      :
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
                  <Covid
                    areasList={areasList}
                    selectedArea={selectedArea}
                    covidGraph1Data={covidGraph1Data}
                    covidGraph2Data={covidGraph2Data}
                    covidTopicsData={covidTopicsData}
                    covidHashtagsData={covidHashtagsData}
                    covidMapData={covidMapData}
                    handleAreaChange={handleAreaChange}
                  />
                </Route>
                <Route exact path="/vaccine">
                  <Vaccine
                    vaccineGraph1Data={vaccineGraph1Data}
                    vaccineGraph2Data={vaccineGraph2Data}
                    vaccineGraph3Data={vaccineGraph3Data}
                    vaccineGraph4Data={vaccineGraph4Data}
                    vaccineGraph5Data={vaccineGraph5Data}
                  />
                </Route>
                <Route exact path="/job-keeper">
                  <JobKeeper
                    jobGraph1Data={jobGraph1Data}
                    jobGraph2Data={jobGraph2Data}
                    jobGraph3Data={jobGraph3Data}
                  />
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
