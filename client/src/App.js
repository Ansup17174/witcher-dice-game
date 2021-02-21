import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import MainPage from './components/MainPage';
import NotFound from './components/NotFound';


const App = () => {

	return (
		<Router>
			<div>
				<Switch>
					<Route path="/" component={MainPage} exact />
					<Route path="*" component={NotFound} exact />
				</Switch>
			</div>
		</Router>
	);
};

export default App;
