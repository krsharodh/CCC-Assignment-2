import './style.css';
import Filters from '../Filters/index';
import React, { useState, useEffect } from 'react';

// Material UI imports
import Card from '@material-ui/core/Card';
import Grid from '@material-ui/core/Grid';
import CardContent from '@material-ui/core/CardContent';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
    // Styles for component
});

function Home() {

    const classes = useStyles();

    const [areasList, setAreasList] = useState([]);

    useEffect(() => {
        getAreas()
    }, [])

    const baseURL = "http://127.0.0.1:5000/";

    const getAreas = async () => {
        const response = await fetch(baseURL);
        const responseJson = await response.json();
        setAreasList(responseJson);
    }

    return (
        <div >
            <header className="App-header">
                <span>Cluster and Cloud Computing Assignment 2</span>
            </header>

            <Grid
                container
                direction="row"
                justify="center"
                alignItems="center"
            >
                <Card className={classes.root}>
                    <CardContent>
                        <Filters autoCompleteList={areasList} label={"Search Area"} />
                    </CardContent>
                </Card>

                <Card className={classes.root}>
                    <CardContent>
                        <h2>Attitude towards vaccine</h2>
                    </CardContent>
                </Card>
            </Grid>
        </div>
    );
}

export default Home;
