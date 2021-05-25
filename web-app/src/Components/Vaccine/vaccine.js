import React from 'react';

import { CovidGraph1, SentimentAnalysis, VaccineBarGraph } from "../Graphs/graphs";

// Material UI imports
import Card from '@material-ui/core/Card';
import Grid from '@material-ui/core/Grid';
import CardContent from '@material-ui/core/CardContent';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import WordCloudVaccine from './WordcloudVaccine'
import WordCloudVaccineHashTag from './WordCloudVaccineHashTag'
import LinearProgress from '@material-ui/core/LinearProgress';
import Skeleton from '@material-ui/lab/Skeleton';

const useStyles = makeStyles({
    container: {
        width: "95%",
        margin: "0 auto",
        marginTop: 10,
    },
    chartHeader: {
        marginBottom: 10,
        display: "inline-block"
    }
});

function Vaccine({ vaccineGraph1Data, vaccineGraph2Data, vaccineGraph3Data, vaccineGraph4Data, vaccineGraph5Data }) {
    const classes = useStyles();

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
                    {vaccineGraph1Data.length === 0 &&
                        <LinearProgress color="secondary" />}
                    <Card>
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={8}>
                                    {vaccineGraph1Data.length === 0
                                        ? <Skeleton animation="pulse" height={350} width="100%" />
                                        : <CovidGraph1 data={vaccineGraph1Data} />
                                    }
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
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


                {/* Graph 2 */}
                <Grid item xs={12} >
                    {vaccineGraph2Data.length === 0 &&
                        <LinearProgress color="secondary" />}
                    <Card>
                        <CardContent>
                            {vaccineGraph2Data.length === 0
                                ? <Skeleton animation="pulse" height={350} width="100%" />
                                : <SentimentAnalysis data={vaccineGraph2Data} />
                            }
                        </CardContent>
                    </Card>
                </Grid>

                {/* Graph 3 */}
                <Grid item xs={12} >
                    {vaccineGraph3Data.length === 0 &&
                        <LinearProgress color="secondary" />}
                    <Card >
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={8}>
                                    {vaccineGraph3Data.length === 0
                                        ? <Skeleton animation="pulse" height={350} width="100%" />
                                        : <VaccineBarGraph data={vaccineGraph3Data} lineDataKey={"median_weekly_personal_income"} yAxisLabel={"Median Weekly Personal Income"} />
                                    }
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Average Sentiment Score of Vaccine-related Tweets and Median Weekly Personal Income
                                     </Typography>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Graph 4 */}
                <Grid item xs={12} >
                    {vaccineGraph4Data.length === 0 &&
                        <LinearProgress color="secondary" />}
                    <Card >
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={8}>
                                    {vaccineGraph4Data.length === 0
                                        ? <Skeleton animation="pulse" height={350} width="100%" />
                                        : <WordCloudVaccine data={vaccineGraph4Data} />
                                    }
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Main Topics of Vaccine
                                     </Typography>
                                    <p>
                                        The wordcloud describes the main topics used in Vaccine related tweets.
                                        <p></p>
                                        <strong>Top 3 Topics</strong>
                                        {
                                            vaccineGraph4Data &&
                                            <ul>
                                                {vaccineGraph4Data
                                                    .sort((a, b) => parseFloat(b.value) - parseFloat(a.value)).slice(0, 3)
                                                    .map(el => <li>{el.text}</li>)}
                                            </ul>
                                        }
                                    </p>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Graph 5 */}
                <Grid item xs={12} >
                    {vaccineGraph5Data.length === 0 &&
                        <LinearProgress color="secondary" />}
                    <Card >
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={8}>
                                    {vaccineGraph5Data.length === 0
                                        ? <Skeleton animation="pulse" height={350} width="100%" />
                                        : <WordCloudVaccineHashTag data={vaccineGraph5Data} />
                                    }
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Main Hashtags
                                     </Typography>
                                    <p>
                                        The wordcloud describes the main hashtags used in Vaccine related tweets.
                                        <p></p>
                                        <strong>Top 3 Hashtags</strong>
                                        {
                                            vaccineGraph5Data &&

                                            <ul>
                                                {vaccineGraph5Data
                                                    .sort((a, b) => parseFloat(b.value) - parseFloat(a.value)).slice(0, 3)
                                                    .map(el => <li>{el.text}</li>)}
                                            </ul>
                                        }
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
