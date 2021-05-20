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
    container: {
        width: "95%",
        margin: "0 auto",
        marginTop: 10,
    },
    chartHeader: {
        marginBottom: 10,
        display: "inline-block"
    },
    descContainer: {
        // border: "0.5px solid black",
        // height: 250
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
    }, [])

    let baseURL = "http://127.0.0.1:5000"
    if (process.env.NODE_ENV === 'production') {
        baseURL = `${process.env.REACT_APP_PROD_URL}`
    };

    const getCities = async () => {
        const response = await fetch(`${baseURL}/getCities`);
        const responseJson = await response.json();
        setAreasList(responseJson);
        setSelectedArea(responseJson[0]["value"]);
        getCovidGraph2Data(responseJson[0]["value"]);
    }

    const getCovidGraph1Data = async () => {
        const response = await fetch(`${baseURL}/getCovidGraph1Data`);
        let responseJson = await response.json();

        responseJson = responseJson.map(el => ({
            ...el,
            percentage: ((el.metioned_covid / el.total_tweets) * 100).toFixed(2)
        }))
        setCovidGraph1Data(responseJson);
    }

    const getCovidGraph2Data = async (city) => {
        const url = new URL(`${baseURL}/getCovidGraph2Data`)
        const params = { city: city }
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

    const handleAreaChange = (event) => {
        setSelectedArea(event.target.value);
        getCovidGraph2Data(event.target.value);
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

                {/* Graph 1 */}
                <Grid item xs={12} >
                    <Card>
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={7}>
                                    <CovidGraph1 data={covidGraph1Data} />
                                </Grid>
                                <Grid item xs={5} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Proportion of tweets mentioning COVID
                                    </Typography>
                                    <p>
                                        The graph describes the percentage of COVID keyword in tweets across various major in cities in Australia.
                                        <p></p>
                                        <strong>Highest Percentage:</strong>  Canberra<br></br>
                                        <strong>Lowest Percentage:</strong>  Hobart
                                    </p>
                                </Grid>
                            </Grid>

                        </CardContent>
                    </Card>
                </Grid>


                {/* Graph 2 */}
                <Grid item xs={12} >
                    <Card >
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={7}>
                                    <CovidGraph2 data={covidGraph2Data} />
                                </Grid>
                                <Grid item xs={5} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Proportion of tweets mentioning COVID
                                    </Typography>
                                    <div className={classes.chartHeader}>
                                        <Filters autoCompleteList={areasList} label={"Select City"} value={selectedArea} handleChange={handleAreaChange} />
                                    </div>
                                    <p>
                                        The graph describes the correlation betweet COVID keyword in tweets and the actual number of cases in a specific city.
                                        <p></p>
                                    </p>
                                </Grid>
                            </Grid>

                        </CardContent>
                    </Card>
                </Grid>

                {/* Graph 3 */}
                <Grid item xs={12} >
                    <Card >
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={7}>
                                    <Wordcloud data={covidWordCloudData} />

                                </Grid>
                                <Grid item xs={5} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Main Topics
                                     </Typography>
                                    <p>
                                        The wordcloud describes the main topics used in COVID related tweets.
                                        <p></p>
                                        <strong>Top 3 topics</strong>
                                        <ul>
                                            {covidWordCloudData
                                                .sort((a, b) => parseFloat(b.value) - parseFloat(a.value)).slice(0, 3)
                                                .map(el => <li>{el.text}</li>)}
                                        </ul>
                                    </p>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>

            </Grid>
        </div>
    );
}

export default Covid;
