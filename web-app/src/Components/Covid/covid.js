import './style.css';
import Filters from '../Filters/filters';
import React, { useState, useEffect } from 'react';

// ReChars
import { CovidGraph1, CovidGraph2 } from "../Graphs/graphs";

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

    useEffect(() => {
        getAreas();
        getSample();
    }, [])

    let baseURL = "http://127.0.0.1:5000/"
    if (process.env.NODE_ENV === 'production') {
        baseURL = `${process.env.REACT_APP_PROD_URL}:${process.env.REACT_APP_PORT_NUMBER}`
    };

    const getAreas = async () => {
        // const response = await fetch(baseURL);
        // const responseJson = await response.json();
        const responseJson = [
            { "label": 'Melbourne', "value": 1 },
            { "label": 'Adelide', "value": 2 },
            { "label": 'Sydney', "value": 3 }
        ]
        setAreasList(responseJson);
        setSelectedArea(responseJson[0]["value"])
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
                            <CovidGraph1 />
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

                            <CovidGraph2 />
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} >
                    <Card >
                        <CardContent>

                            <Typography variant="h6" className={classes.chartHeader}>
                                Word Cloud
                            </Typography>

                        </CardContent>
                    </Card>
                </Grid>

            </Grid>
        </div>
    );
}

export default Covid;
