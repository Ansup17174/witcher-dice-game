import {useState, useEffect, useRef} from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import MainPage from './pages/MainPage';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import ChangePasswordPage from './pages/ChangePasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';
import NotFound from './pages/NotFound';
import ProfilePage from './pages/ProfilePage';
import {GlobalContext} from './GlobalContext';
import apiClient from './apiclient';
import ConfirmEmail from './pages/ConfirmEmail';
import ResendPage from './pages/ResendPage';
import RoomRedirect from './components/RoomRedirect';
import WitcherRoomPage from './pages/WitcherRoomPage';
import RankingPage from './pages/RankingPage';
import Navbar from './components/Navbar';
import 'react-notifications/lib/notifications.css';
import {NotificationManager, NotificationContainer} from 'react-notifications';
import LoadingPage from './pages/LoadingPage';


const App = () => {

	const [loading, setLoading] = useState(true);
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

	const sleep = ms => {
		return new Promise(resolve => setTimeout(resolve, ms));
	};

	const getUserData = async () => {
		const token = localStorage.getItem("dice-token");
		if (!token) {
			setUserData({});
		} else {
			await apiClient.get("/auth/user", {withCredentials: true, headers: {"Authorization": `Bearer ${token}`}})
			.then(response => {
				setUserData(response.data);
				if (onlineUsersWs.current.readyState === 1) {
					onlineUsersWs.current.send(token);
				}
			})
			.catch(error => {
				console.log(error);
				setUserData({});
				console.log(token);
				localStorage.removeItem("dice-token");
			});
		}
	};

	const init = async () => {
		getUserData();
		await sleep(250);
		setLoading(false);
	};

	useEffect(() => {
		onlineUsersWs.current = new WebSocket(webSocketBase + "/online");
		onlineUsersWs.current.onmessage = message => setOnlineUsers(JSON.parse(message.data));
		onlineUsersWs.current.onopen = () => onlineUsersWs.current.send(localStorage.getItem('dice-token'))
		init();
		return () => {
			onlineUsersWs.current.close();
		};
	}, []);

	return (
		<GlobalContext.Provider value={{userData, setUserData, getUserData, NotificationManager, webSocketBase, onlineUsers}}>
			<LoadingPage loading={loading}>Loading...</LoadingPage>
			<Router>
				<Navbar />
				<div className="main-page">
				<NotificationContainer />
				<Switch>
					<Route path="/" component={userData.id ? MainPage : LoginPage} exact />
					<Route path="/register" component={RegisterPage} exact />
					<Route path="/profile" component={ProfilePage} exact />
					<Route path="/ranking" component={RankingPage} exact />
					<Route path="/room/:game/:roomId" component={RoomRedirect} exact />
					<Route path="/change-password" component={ChangePasswordPage} exact />
					<Route path="/reset-password" component={ResetPasswordPage} exact />
					<Route path="/resend-verification-email" component={ResendPage} exact />
					<Route path="/confirm-email/:user_id/:token" component={ConfirmEmail} exact />
					<Route path="*" component={NotFound} exact />
				</Switch>
				</div>
			</Router>
		</GlobalContext.Provider>
	);
};

export default App;
