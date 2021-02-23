import {useState, useEffect} from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import Main from './pages/Main';
import NotFound from './components/NotFound';
import GlobalContext from './GlobalContext';
import apiClient from './apiclient';


const App = () => {

	const [userData, setUserData] = useState({
		id: "",
		username: "",
		email: {
			address: "",
			is_confirmed: true
		},
		profile: {
			matches_won: 0,
			matches_lost: 0,
			matches_played: 0
		}
	});

	const getUserData = () => {
		const token = localStorage.getItem("dice-token");
		if (!token) {
			setUserData({});
		} else {
			apiClient.get("/auth/user", {withCredentials: true, headers: {"Authorization": `Bearer ${token}`}})
			.then(response => {
				setUserData(response.data);
			})
			.catch(error => {
				setUserData({});
				localStorage.removeItem("dice-token");
			});
		}
	};

	useEffect(() => {
		getUserData();
	}, []);

	return (
		<GlobalContext.Provider value={{userData, setUserData}}>
			<Router>
					<Switch>
						<Route path="/" component={Main} exact />
						<Route path="*" component={NotFound} exact />
					</Switch>
			</Router>
		</GlobalContext.Provider>
	);
};

export default App;
