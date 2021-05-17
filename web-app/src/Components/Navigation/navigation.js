import {
    useHistory
} from "react-router-dom";
import React from 'react';

// Material UI imports
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    title: {
        flexGrow: 1,
        marginLeft: "1rem"
    },
}));

function Navigation() {

    const history = useHistory();

    const classes = useStyles();

    const [tabIndex, setTabIndex] = React.useState("/covid");

    const handleTabIndexChange = (event, newTabIndex) => {
        setTabIndex(newTabIndex);
        history.push(newTabIndex)
    };

    return (
        <div className={classes.root}>
            <AppBar position="static">
                {/* <Typography variant="h6" className={classes.title}>
                    Cluster and Cloud Computing Assignment 2
                </Typography> */}
                <Tabs value={tabIndex} onChange={handleTabIndexChange} aria-label="simple tabs example">
                    <Tab label="Covid" value="/covid" />
                    <Tab label="Vaccine" value="/vaccine" />
                    <Tab label="Job Keeper" value="/job-keeper" />
                </Tabs>
            </AppBar>
        </div>
    );
}

export default Navigation;
