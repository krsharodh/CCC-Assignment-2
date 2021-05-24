import {
    useHistory,
    useLocation
} from "react-router-dom";
import React from 'react';

// Material UI imports
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

const drawerWidth = 150;

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
    },
    drawer: {
        width: drawerWidth,
        flexShrink: 0,
        "& .Mui-selected": {
            borderRight: "1px solid blue"
        }
    },
    drawerPaper: {
        width: drawerWidth,
    },
    toolbar: theme.mixins.toolbar,

}));

function Navigation() {

    const history = useHistory();

    const classes = useStyles();

    const location = useLocation();

    return (
        <div className={classes.root}>
            <Drawer
                className={classes.drawer}
                variant="permanent"
                classes={{
                    paper: classes.drawerPaper,
                }}
                anchor="left"
            >
                <div className={classes.toolbar} />
                <Divider />
                <List>
                    {[{ text: 'Covid', value: '/covid' }, { text: 'Vaccine', value: '/vaccine' }, { text: 'Job Keeper', value: '/job-keeper' }].map((el, index) => (
                        <ListItem button key={el.text} onClick={() => history.push(el.value)} selected={location.pathname === el.value}>
                            <ListItemText primary={el.text} />
                        </ListItem>
                    ))}
                </List>
            </Drawer>
        </div>

    );
}

export default Navigation;
