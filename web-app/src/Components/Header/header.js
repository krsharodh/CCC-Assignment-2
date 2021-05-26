// Material UI imports
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import AppBar from '@material-ui/core/AppBar';
import { makeStyles } from '@material-ui/core/styles';

const drawerWidth = 150;

const useStyles = makeStyles((theme) => ({
    appBar: {
        width: `calc(100% - ${drawerWidth}px)`,
        backgroundImage: "linear-gradient(#ff9d2f, #ff6126)",
        marginLeft: drawerWidth,
    }
}));

function Header() {

    const classes = useStyles();

    return (
        <AppBar position="fixed" className={classes.appBar}>
            <Toolbar>
                <Typography variant="h6" noWrap>
                    COVID analysis among major Australian cities
            </Typography>
            </Toolbar>
        </AppBar>
    );
}

export default Header;
