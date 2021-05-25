import './style.css';
import Filters from '../Filters/filters';
import React from 'react';

// ReChars
import { CovidGraph1, CovidGraph2 } from "../Graphs/graphs";
import WordCloudCovid from "./WordCloudCovid"
import Map from "./Map"
import WordCloudCovidHashTag from "./WordCloudCovidHashTag"

// Material UI imports
import Card from '@material-ui/core/Card';
import Grid from '@material-ui/core/Grid';
import CardContent from '@material-ui/core/CardContent';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
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
    },
    chartHeaderCenter: {
        marginBottom: 10,
        textAlign: "center"
    },
    descContainer: {
        // border: "0.5px solid black",
        // height: 250
    }
});

function Covid({ areasList, covidGraph1Data, covidGraph2Data, covidTopicsData, covidHashtagsData, handleAreaChange, selectedArea }) {

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
                    {covidGraph1Data.length === 0 &&
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
                                    {covidGraph1Data.length === 0
                                        ? <Skeleton animation="rect" height={350} width="100%" />
                                        : <CovidGraph1 data={covidGraph1Data} />
                                    }
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
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
                    {covidGraph2Data.length === 0 &&
                        <LinearProgress color="secondary" />}
                    <Card >
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                            >
                                <Grid item xs={12}>
                                    <Typography variant="h6" className={classes.chartHeaderCenter}>
                                        Proportion of tweets mentioning COVID vs Cases
                                    </Typography>
                                    <div className={classes.chartHeaderCenter}>
                                        <Filters data={areasList} value={selectedArea} handleChange={handleAreaChange} />
                                    </div>
                                    {covidGraph2Data.length === 0
                                        ? <Skeleton animation="rect" height={350} width="100%" />
                                        : <CovidGraph2 data={covidGraph2Data} />
                                    }

                                </Grid>
                                {/* <Grid item xs={5} className={classes.descContainer}>
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
                                </Grid> */}
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
                    {covidTopicsData.length === 0 &&
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
                                    {covidTopicsData.length === 0
                                        ? <Skeleton animation="rect" height={350} width="100%" />
                                        : <WordCloudCovid data={covidTopicsData} />
                                    }
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>

                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Main Topics
                                     </Typography>
                                    <p>
                                        The wordcloud describes the main topics used in COVID related tweets.
                                        <p></p>
                                        <strong>Top 3 topics</strong>
                                        {
                                            covidTopicsData &&
                                            <ul>
                                                {covidTopicsData
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

                {/* Graph 4 */}
                <Grid item xs={12} >
                    {covidHashtagsData.length === 0 &&
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
                                    {covidHashtagsData.length === 0
                                        ? <Skeleton animation="rect" height={350} width="100%" />
                                        : <WordCloudCovidHashTag data={covidHashtagsData} />
                                    }
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Main Hashtags
                                     </Typography>
                                    <p>
                                        The wordcloud describes the main topics used in COVID related tweets.
                                        <p></p>
                                        <strong>Top 3 Hashtags</strong>
                                        {
                                            covidHashtagsData &&
                                            <ul>
                                                {covidHashtagsData
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

            </Grid>
        </div>
    );
}

export default Covid;
