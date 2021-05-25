import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faVirus } from '@fortawesome/free-solid-svg-icons';
import { faShieldVirus } from '@fortawesome/free-solid-svg-icons';
import { faUserShield } from '@fortawesome/free-solid-svg-icons';
import KeyboardArrowRightIcon from '@material-ui/icons/KeyboardArrowRight';
import couchdb from "../../Assets/couchdb.svg";
import ansible from "../../Assets/ansible.svg";
import twitter from "../../Assets/twitter.svg";
import flask from "../../Assets/flask.png";
import react from "../../Assets/react.svg";

const useStyles = makeStyles((theme) => ({
    banner: {
        position: "relative",
        height: 300,
        backgroundImage: "linear-gradient(#ff9d2f, #ff6126)",
        borderBottomLeftRadius: "50% 20%",
        borderBottomRightRadius: "50% 20%",
        "& h1": {
            margin: 0,
            padding: "30px 0",
            font: "44px Arial",
            textAlign: "center",
            color: "white"
        },
        "& h4": {
            color: "white",
            fontFamily: "Roboto, sans-serif"
        }
    },
    cards: {
        width: "80%",
        margin: "0 auto",
        textAlign: "center"
    },
    btn: {
        margin: "0 auto",
        textAlign: "center",
        color: "white",
        "& .MuiButton-outlined": {
            border: "1px solid white"
        },
        "& .MuiButton-root": {
            color: "white"
        }
    },
    covidIcon: {
        color: "red"
    },
    vaccineIcon: {
        color: "Blue"
    },
    jobKeeperIcon: {
        color: "Green"
    }
}));

function Cover({
    handleGetStarted
}) {

    const classes = useStyles();

    return (
        <div>
            <header className={classes.banner}>
                <h1>Twitter Data Analysis</h1>
                <Grid
                    container
                    direction="row"
                    justify="space-evenly"
                    alignItems="center"
                    spacing={3}
                    className={classes.cards}
                >
                    <Grid item xs>
                        <img src={ansible} alt="React Logo" width="50" height="50" />
                        <h4>Ansible</h4>
                    </Grid>
                    <Grid item xs>
                        <img src={couchdb} alt="React Logo" width="50" height="50" />
                        <h4>Couch DB</h4>
                    </Grid>
                    <Grid item xs>
                        <img src={twitter} alt="React Logo" width="50" height="50" />
                        <h4>Twitter</h4>
                    </Grid>
                    <Grid item xs>
                        <img src={flask} alt="React Logo" width="50" height="50" />
                        <h4>Flask</h4>
                    </Grid>
                    <Grid item xs>
                        <img src={react} alt="React Logo" width="50" height="50" />
                        <h4>React</h4>
                    </Grid>
                </Grid>
                <div className={classes.btn}>
                    <Button variant="outlined" onClick={handleGetStarted}>Get Started <KeyboardArrowRightIcon /></Button>
                </div>
            </header>

            <Grid
                container
                direction="row"
                justify="space-evenly"
                alignItems="center"
                spacing={3}
                className={classes.cards}
            >
                <Grid item xs>
                    <Card>
                        <CardContent>

                            <h3>COVID</h3>
                            <FontAwesomeIcon icon={faVirus} size="6x" className={classes.covidIcon} />
                        </CardContent>
                    </Card>
                </Grid> ``
                <Grid item xs>
                    <Card>
                        <CardContent>

                            <h3>Vaccine</h3>

                            <FontAwesomeIcon icon={faShieldVirus} size="6x" className={classes.vaccineIcon} />

                        </CardContent>
                    </Card>

                </Grid>
                <Grid item xs>
                    <Card>
                        <CardContent>

                            <h3>Job Keeper</h3>

                            <FontAwesomeIcon icon={faUserShield} size="6x" className={classes.jobKeeperIcon} />

                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </div>
    );
}

export default Cover;
