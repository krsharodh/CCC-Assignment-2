import './style.css';
import Filters from '../Filters/filters';
import React, { useState, useEffect } from 'react';

// ReChars
import { CovidGraph1, CovidGraph2, Wordcloud } from "../Graphs/graphs";
import WordCloudCovid from "./WordCloudCovid"
import Map from "./Map"
import WordCloudCovidHashTag from "./WordCloudCovidHashTag"
// Agent
import { GetCities, GetCovidGraph1Data, GetCovidGraph2Data, GetCovidTopicsData, GetCovidHashtagsData, GetCovidMapData } from "../agent";

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
    const [covidTopicsData, setCovidTopicsData] = useState([]);
    const [covidHashtagsData, setCovidHashtagsData] = useState([]);
    const [covidMapData, setCovidMapData] = useState([]);

    useEffect(() => {
        getCities();
        getCovidGraph1Data();
        getCovidTopicsData();
        getCovidHashtagsData();
        getCovidMapData();
    }, [])

    const getCities = async () => {
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
                                        <Filters data={areasList} value={selectedArea} handleChange={handleAreaChange} />
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
                {/* <Grid item xs={12} >
                    <Card >
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={7}>
                                    <Map data={covidMapData}/>

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
                                            {covidTopicsData
                                                .sort((a, b) => parseFloat(b.value) - parseFloat(a.value)).slice(0, 3)
                                                .map(el => <li>{el.text}</li>)}
                                        </ul>
                                    </p>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid> */}

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
                                    <WordCloudCovid data={covidTopicsData}/>

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
                                            {covidTopicsData
                                                .sort((a, b) => parseFloat(b.value) - parseFloat(a.value)).slice(0, 3)
                                                .map(el => <li>{el.text}</li>)}
                                        </ul>
                                    </p>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Graph 4 */}
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

                                    <WordCloudCovidHashTag data={covidHashtagsData}/>
                                </Grid>
                                <Grid item xs={5} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Main Hashtags
                                     </Typography>
                                    <p>
                                        The wordcloud describes the main topics used in COVID related tweets.
                                        <p></p>
                                        <strong>Top 3 Hashtags</strong>
                                        <ul>
                                            {covidHashtagsData
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
