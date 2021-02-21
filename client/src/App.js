import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import MainPage from './components/MainPage';
import NotFound from './components/NotFound';
import Invitations from './components/Invitations';


const App = () => {

	return (
		<Router>
			<div>
				<Switch>
					<Route path="/" component={MainPage} exact />
					<Route path="/invitations" component={Invitations} exact />
					<Route path="*" component={NotFound} exact />
				</Switch>
			</div>
		</Router>
	);
};

export default App;
