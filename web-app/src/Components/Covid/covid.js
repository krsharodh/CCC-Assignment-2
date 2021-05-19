import './style.css';
import Filters from '../Filters/filters';
import React, { useState, useEffect } from 'react';

// ReChars
import { CovidGraph1, CovidGraph2, Wordcloud } from "../Graphs/graphs";

// Material UI imports
import Card from '@material-ui/core/Card';
import Grid from '@material-ui/core/Grid';
import CardContent from '@material-ui/core/CardContent';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';


const useStyles = makeStyles({
    // Styles for component
    container: {
        width: "95%",
        margin: "0 auto",
        marginTop: 10
    },
    chartHeader: {
        marginBottom: 10
    }
});

function Covid() {

    const classes = useStyles();

    const [areasList, setAreasList] = useState([]);
    const [selectedArea, setSelectedArea] = useState(0);
    const [covidGraph1Data, setCovidGraph1Data] = useState([]);
    const [covidGraph2Data, setCovidGraph2Data] = useState([]);
    const [covidWordCloudData, setCovidWordCloudData] = useState([]);

    useEffect(() => {
        getCities();
        getCovidGraph1Data();
        getCovidWordCloudData();
        // getSample();
    }, [])

    let baseURL = "http://127.0.0.1:5000"
    if (process.env.NODE_ENV === 'production') {
        baseURL = `${process.env.REACT_APP_PROD_URL}`
    };

    const getCities = async () => {
        const response = await fetch(`${baseURL}/getCities`);
        const responseJson = await response.json();
        setAreasList(responseJson);
        setSelectedArea(responseJson[0]["value"])
        getCovidGraph2Data();
    }

    const getCovidGraph1Data = async () => {
        const response = await fetch(`${baseURL}/getCovidGraph1Data`);
        const responseJson = await response.json();
        setCovidGraph1Data(responseJson);
    }

    const getCovidGraph2Data = async () => {
        const url = new URL(`${baseURL}/getCovidGraph2Data`)
        const params = { city: selectedArea }
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
        const response = await fetch(url);
        const responseJson = await response.json();
        setCovidGraph2Data(responseJson);
    }

    const getCovidWordCloudData = async () => {
        const response = await fetch(`${baseURL}/getCovidWordCloudData`);
        const responseJson = await response.json();
        setCovidWordCloudData(responseJson);
    }

    const getSample = async () => {
        const response = await fetch(baseURL + "getSample");
        const responseJson = await response.json();
        console.log(responseJson);
    }

    const handleAreaChange = (event) => {
        setSelectedArea(event.target.value);
    };


    return (
        <div className={classes.container}>

            <Grid
                container
                direction="row"
                justify="center"
                alignItems="center"
                spacing={2}
            >
                <Grid item xs={6} >
                    <Card>
                        <CardContent>
                            <Typography variant="h6" className={classes.chartHeader}>
                                Proportion/count of tweets mentioning COVID
                            </Typography>
                            <CovidGraph1 data={covidGraph1Data} />
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={6} >
                    <Card >
                        <CardContent>
                            <Typography variant="h6" className={classes.chartHeader}>
                                <Grid
                                    container
                                    direction="row"
                                    justify="center"
                                    alignItems="center"
                                >
                                    <Grid item xs={7}>
                                        COVID tweets vs COVID cases -
                                    </Grid>
                                    <Grid item xs={5}>
                                        <Filters autoCompleteList={areasList} label={"Select City"} value={selectedArea} handleChange={handleAreaChange} />
                                    </Grid>
                                </Grid>
                            </Typography>

                            <CovidGraph2 data={covidGraph2Data} />
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} >
                    <Card >
                        <CardContent>

                            <Typography variant="h6" className={classes.chartHeader}>
                                Main Topics
                            </Typography>

                            <Wordcloud data={covidWordCloudData} />

                        </CardContent>
                    </Card>
                </Grid>

            </Grid>
        </div>
    );
}

export default Covid;
