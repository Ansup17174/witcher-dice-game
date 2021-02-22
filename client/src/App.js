import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import MainPage from './components/MainPage';
import GameRoom from './components/GameRoom';
import NotFound from './components/NotFound';


const App = () => {

	return (
		<Router>
			<div>
				<Switch>
					<Route path="/" component={MainPage} exact />
					<Route path="/room/:room_id/:access_token" component={GameRoom} exact />
					<Route path="*" component={NotFound} exact />
				</Switch>
			</div>
		</Router>
	);
};

export default App;
