import {useState} from 'react';
import axios from 'axios';
const onlineUsersWs = new WebSocket("ws://localhost:8000/ws/online");
onlineUsersWs.onmessage = e => {
	console.log(JSON.parse(e.data));
};


const App = () => {
	const [onlineUsers, setOnlineUsers] = useState([]);
	const [chatLines, setChatLines] = useState([]);
	const [chatInput, setChatInput] = useState("");
	const [userData, setUserData] = useState({})
	const [formData, setFormData] = useState({
		username: "",
		password: ""
	});

	onlineUsersWs.onmessage = e => {
		setOnlineUsers(JSON.parse(e.data));
	};

	const login = async e => {
		e.preventDefault();
		await axios.post("http://localhost:8000/auth/login", formData)
		.then(response => {
			setUserData(response.data);
			onlineUsersWs.send(response.data.access_token);
		})
		.catch(error => {
			console.log(error.response.data);
		});
	}

	return (
		<div>
			<form onSubmit={login}>
				<input type="text" placeholder="username" value={formData.username}
				onChange={e => setFormData({...formData, username: e.target.value})}/>
				<input type="password" placeholder="password" value={formData.password}
				onChange={e => setFormData({...formData, password: e.target.value})}/>
				<input type="submit" value="Login"/>
			</form>
			<div>
				{onlineUsers.length > 0 && onlineUsers.map((username, index) => <p key={index}>{username}</p>)}
			</div>
			<div>

			</div>
		</div>
	);
}

export default App;
