import './style.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import Home from "../Home";
import NotFound from "../NotFound";

// Material UI imports

function App() {
  return (
    <Router >

      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
        <Route path="*">
          <NotFound />
        </Route>
      </Switch>

    </Router>
  );
}

export default App;
