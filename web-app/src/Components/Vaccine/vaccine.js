import './style.css';
import Filters from '../Filters/filters';
import React, { useState, useEffect } from 'react';

// Material UI imports
import Card from '@material-ui/core/Card';
import Grid from '@material-ui/core/Grid';
import CardContent from '@material-ui/core/CardContent';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
    // Styles for component
});

function Vaccine() {

    const classes = useStyles();

    const [areasList, setAreasList] = useState([]);

    useEffect(() => {
        getAreas()
    }, [])

    useEffect(() => {
        getSample()
    }, [])

    let baseURL = "http://127.0.0.1:5000/"
    if (process.env.NODE_ENV === 'production') {
        baseURL = `${process.env.REACT_APP_PROD_URL}:${process.env.REACT_APP_PORT_NUMBER}`
    };

    const getAreas = async () => {
        const response = await fetch(baseURL);
        const responseJson = await response.json();
        setAreasList(responseJson);
    }

    const getSample = async () => {
        const response = await fetch(baseURL + "getSample");
        const responseJson = await response.json();
        console.log(responseJson);
    }

    return (
        <div >
            {/* <header className="App-header">
                <span>Cluster and Cloud Computing Assignment 2</span>
            </header> */}

            <Grid
                container
                direction="row"
                justify="center"
                alignItems="center"
            >
                <Grid item xs={12} spacing={2}>

                    <Card className={classes.root}>
                        <CardContent>
                            <Filters autoCompleteList={areasList} label={"Search Area"} />
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} >

                    <Card className={classes.root}>
                        <CardContent>
                            <h2>Attitude towards vaccine</h2>
                        </CardContent>
                    </Card>
                </Grid>

            </Grid>
        </div>
    );
}

export default Vaccine;
