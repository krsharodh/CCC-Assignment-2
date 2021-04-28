import logo from './logo.svg';
import './App.css';
import Filters from './Components/Filters';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
  // Styles for component
});

function App() {
  const classes = useStyles();

  const areasList = [
    { title: 'Carlton', postCode: 3053 },
    { title: 'Brunswick', postCode: 3053 },
    { title: 'Clayton', postCode: 3053 }
  ];

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

export default App;
