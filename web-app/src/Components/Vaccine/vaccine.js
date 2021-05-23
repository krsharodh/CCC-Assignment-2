import React, { useState, useEffect } from 'react';

import { CovidGraph1, Wordcloud, SentimentAnalysis } from "../Graphs/graphs";


import { GetVaccineGraph1Data, GetVaccineGraph2Data, GetVaccineGraph3Data, GetVaccineGraph4Data } from "../agent";

import { MapContainer, CircleMarker, TileLayer } from "react-leaflet";

// Material UI imports
import Card from '@material-ui/core/Card';
import Grid from '@material-ui/core/Grid';
import CardContent from '@material-ui/core/CardContent';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import WordCloudVaccine from './WordcloudVaccine'
import WordCloudVaccineHashTag from './WordCloudVaccineHashTag'

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

function Vaccine() {

    const classes = useStyles();

    const [vaccineGraph1Data, setVaccineGraph1Data] = useState([]);
    const [vaccineGraph2Data, setVaccineGraph2Data] = useState([]);
    const [vaccineGraph3Data, setVaccineGraph3Data] = useState([]);
    const [vaccineGraph4Data, setVaccineGraph4Data] = useState([]);

    useEffect(() => {
        getVaccineGraph1Data();
        getVaccineGraph2Data();
        getVaccineGraph3Data();
        getVaccineGraph4Data();
    }, [])

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
                                    <CovidGraph1 data={vaccineGraph1Data} />
                                </Grid>
                                <Grid item xs={5} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Proportion of tweets mentioning Vaccine
                                    </Typography>
                                    <p>
                                        The graph describes the percentage of Vaccine keyword in tweets across various major in cities in Australia.
                                        <p></p>
                                        <strong>Highest Percentage:</strong>  Adelaide<br></br>
                                        <strong>Lowest Percentage:</strong>  Hobart
                                    </p>
                                </Grid>
                            </Grid>

                        </CardContent>
                    </Card>
                </Grid>

                {/* <Grid
                    container
                    direction="row"
                    justify="center"
                    alignItems="center"
                    spacing={2}
                ></Grid> */}

                {/* Graph 2 */}
                <Grid item xs={12} >
                    <Card>
                        <CardContent>
                            <SentimentAnalysis data={vaccineGraph2Data} />
                            {/* <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={12}>
                                    <SentimentAnalysis data={vaccineGraph2Data} />
                                </Grid> */}
                            {/* <Grid item xs={5} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Sentiment Analysis
                                    </Typography>
                                    <p>
                                        The graph describes the sentiment score of tweets related to Vaccine keyword in Australia.
                                    </p>
                                </Grid> */}
                            {/* </Grid> */}

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
                                    <WordCloudVaccine data={vaccineGraph3Data} />

                                </Grid>
                                <Grid item xs={5} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Main Topics of Vaccine
                                     </Typography>
                                    <p>
                                        The wordcloud describes the main topics used in Vaccine related tweets.
                                        <p></p>
                                        <strong>Top 3 Topics</strong>
                                        <ul>
                                            {vaccineGraph3Data
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

                                    <WordCloudVaccineHashTag data={vaccineGraph4Data} />
                                </Grid>
                                <Grid item xs={5} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Main Hashtags
                                     </Typography>
                                    <p>
                                        The wordcloud describes the main hashtags used in Vaccine related tweets.
                                        <p></p>
                                        <strong>Top 3 Hashtags</strong>
                                        <ul>
                                            {vaccineGraph4Data
                                                .sort((a, b) => parseFloat(b.value) - parseFloat(a.value)).slice(0, 3)
                                                .map(el => <li>{el.text}</li>)}
                                        </ul>
                                    </p>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Map Container */}
                {/* <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <MapContainer
                                style={{ height: "480px", width: "100%" }}
                                zoom={1}
                                center={[-0.09, 51.505]}>
                                <TileLayer url="http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                            </MapContainer>
                        </CardContent>
                    </Card>
                </Grid> */}

            </Grid>
        </div>
    );
}

export default Vaccine;
