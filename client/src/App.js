import {useState, useEffect, useRef} from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import MainPage from './pages/MainPage';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import NotFound from './pages/NotFound';
import GlobalContext from './GlobalContext';
import apiClient from './apiclient';
import ConfirmEmail from './pages/ConfirmEmail';
import Navbar from './components/navbar/Navbar';
import 'react-notifications/lib/notifications.css';
import {NotificationManager, NotificationContainer} from 'react-notifications';


const App = () => {

	const webSocketBase = "ws://localhost:8000/ws";
	const [onlineUsers, setOnlineUsers] = useState([]);
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
	const onlineUsersWs = useRef(null);

	const getUserData = async () => {
		const token = localStorage.getItem("dice-token");
		if (!token) {
			setUserData({});
		} else {
			await apiClient.get("/auth/user", {withCredentials: true, headers: {"Authorization": `Bearer ${token}`}})
			.then(response => {
				setUserData(response.data);
				onlineUsersWs.current.send(token);
			})
			.catch(error => {
				setUserData({});
				localStorage.removeItem("dice-token");
			});
		}
	};

	useEffect(() => {
		getUserData();
		onlineUsersWs.current = new WebSocket(webSocketBase + "/online");
		onlineUsersWs.current.onmessage = message => console.log(message.data);
		return () => {
			onlineUsersWs.current.close();
		};
	}, []);

	return (
		<GlobalContext.Provider value={{userData, setUserData, getUserData, NotificationManager, webSocketBase}}>
			<NotificationContainer />
			<Router>
				<Navbar />
				<div className="main-page">
				<Switch>
					<Route path="/" component={userData.id ? MainPage : LoginPage} exact />
					<Route path="/register" component={RegisterPage} exact />
					<Route path="/confirm-email/:user_id/:token" component={ConfirmEmail} exact />
					<Route path="*" component={NotFound} exact />
				</Switch>
				</div>
			</Router>
		</GlobalContext.Provider>
	);
};

export default App;
