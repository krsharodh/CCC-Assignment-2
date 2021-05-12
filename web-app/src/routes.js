import { Router, Route } from 'react-router'

// Components
import App from './Components/App/index';
import NotFound from './Components/NotFound/index';

const Routes = (props) => (
    <Router {...props}>
        <Route path="/index" component={App} />
        <Route path="*" component={NotFound} />s
    </Router>
);

export default Routes;