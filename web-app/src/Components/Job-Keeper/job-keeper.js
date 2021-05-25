import './style.css';
import React, { useState, useEffect } from 'react';

import { JobGraph } from "../Graphs/graphs";

import { GetJobGraph1Data, GetJobGraph2Data, GetJobGraph3Data } from "../agent";

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

function JobKeeper() {

    const classes = useStyles();

    const [jobGraph1Data, setJobGraph1Data] = useState([]);
    const [jobGraph2Data, setJobGraph2Data] = useState([]);
    const [jobGraph3Data, setJobGraph3Data] = useState([]);

    useEffect(() => {
        getJobGraph1Data();
        getJobGraph2Data();
        getJobGraph3Data();
    }, [])

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
                                <Grid item xs={8}>
                                    <JobGraph data={jobGraph1Data} lineDataKey={"median_weekly_personal_income"} yAxisLabel={"Median Weekly Personal Income"} />
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Proportion of tweets mentioning Job Keeper and Median Weekly Personal Income
                                    </Typography>
                                    <p>
                                        The graph describes the percentage of Job Keeper keyword in tweets and Median Weekly Personal Income across various major in cities in Australia.
                                        <p></p>
                                        <strong>Highest Percentage:</strong>  Adelaide<br></br>
                                        <strong>Lowest Percentage:</strong>  Darwin
                                    </p>
                                </Grid>
                            </Grid>

                        </CardContent>
                    </Card>
                </Grid>

                {/* Graph 2 */}
                <Grid item xs={12} >
                    <Card>
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={8}>
                                    <JobGraph data={jobGraph2Data} lineDataKey={"jobseeker_payment"} yAxisLabel={"Jobseeker Payment"} />
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Proportion of tweets mentioning Job Keeper and Jobseeker Payment
                                    </Typography>
                                    <p>
                                        The graph describes the percentage of Job Keeper keyword in tweets and Jobseeker Payment across various major in cities in Australia.
                                        <p></p>
                                        <strong>Highest Percentage:</strong>  Adelaide<br></br>
                                        <strong>Lowest Percentage:</strong>  Hobart
                                    </p>
                                </Grid>
                            </Grid>

                        </CardContent>
                    </Card>
                </Grid>

                {/* Graph 3 */}
                <Grid item xs={12} >
                    <Card>
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={8}>
                                    <JobGraph data={jobGraph3Data} lineDataKey={"Aged_15_64_percentage"} yAxisLabel={"Aged 15 to 64 %"} />
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Proportion of tweets mentioning Vaccine and Aged 15 to 64 %
                                    </Typography>
                                    <p>
                                        The graph describes the percentage of Job Keeper keyword in tweets and Aged 15 to 64 % across various major in cities in Australia.
                                        <p></p>
                                        <strong>Highest Percentage:</strong>  Adelaide<br></br>
                                        <strong>Lowest Percentage:</strong>  Hobart
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

export default JobKeeper;
