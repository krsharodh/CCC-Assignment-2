import './style.css';
import React from 'react';

import { JobGraph } from "../Graphs/graphs";

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
    }
});

function JobKeeper({ jobGraph1Data, jobGraph2Data, jobGraph3Data }) {

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
                    {jobGraph1Data.length === 0 &&
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
                                    {jobGraph1Data.length === 0
                                        ? <Skeleton animation="pulse" height={350} width="100%" />
                                        : <JobGraph data={jobGraph1Data} lineDataKey={"median_weekly_personal_income"} yAxisLabel={"Median Weekly Personal Income"} />
                                    }
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Proportion of tweets mentioning Job Keeper and Median Weekly Personal Income
                                    </Typography>
                                    <p>
                                        The graph describes the percentage of tweets containing covid keyword in main cities of Australia.
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
                        {jobGraph2Data.length === 0 &&
                            <LinearProgress color="secondary" />}
                        <CardContent>
                            <Grid
                                container
                                direction="row"
                                justify="center"
                                alignItems="center"
                                spacing={2}>
                                <Grid item xs={8}>
                                    {jobGraph2Data.length === 0
                                        ? <Skeleton animation="pulse" height={350} width="100%" />
                                        : <JobGraph data={jobGraph2Data} lineDataKey={"jobseeker_payment"} yAxisLabel={"Jobseeker Payment"} />
                                    }
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Proportion  of tweets mentioning Jobseeker and counts  of Jobseeker payment in main cities
                                    </Typography>
                                    <p>
                                        The graph describes the percentage of Jobseeker/Jobkeeper keyword in tweets and the counts of jobseeker payment recepients across main cities in Australia.
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
                    {jobGraph3Data.length === 0 &&
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
                                    {jobGraph3Data.length === 0
                                        ? <Skeleton animation="pulse" height={350} width="100%" />
                                        : <JobGraph data={jobGraph3Data} lineDataKey={"Aged_15_64_percentage"} yAxisLabel={"Aged 15 to 64 %"} />
                                    }
                                </Grid>
                                <Grid item xs={4} className={classes.descContainer}>
                                    <Typography variant="h6" className={classes.chartHeader}>
                                        Proportion of tweets mentioning Jobkeeper and the percentage of population aged between 15 and 64
                                    </Typography>
                                    <p>
                                        The graph describes the percentage of tweets containing Jobkeeper/Jobseeker keyword and the percentage of population aged between 15 and 64 in the main cities of Australia.
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
