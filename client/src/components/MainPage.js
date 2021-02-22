import {useState, useRef, useEffect} from 'react';
import {Link} from 'react-router-dom';
import axios from 'axios';


const MainPage = () => {
    const [onlineUsers, setOnlineUsers] = useState([]);
	const [chatLines, setChatLines] = useState("");
	const [chatInput, setChatInput] = useState("");
	const [userData, setUserData] = useState({
		id: "",
		username: "",
		email: {
			address: "",
			is_confirmed: true
		},
		access_token: ""
	})
	const [formData, setFormData] = useState({
		username: "",
		password: ""
    });
    const [roomList, setRoomList] = useState([]);
    const onlineUsersWs = useRef(null);
    const chatWs = useRef(null);
    const roomListWs = useRef(null);

    useEffect(() => {
        onlineUsersWs.current = new WebSocket("ws://localhost:8000/ws/online");
        chatWs.current = new WebSocket("ws://localhost:8000/ws/chat");
        roomListWs.current = new WebSocket("ws://localhost:8000/ws/room-list");
        
        onlineUsersWs.current.onmessage = e => {
            setOnlineUsers(JSON.parse(e.data));
        };
    
        chatWs.current.onmessage = e => {
            setChatLines(e.data);
        };

        roomListWs.current.onmessage = e => {
            setRoomList(JSON.parse(e.data));
        };
        
        return () => {
            onlineUsersWs.current.close();
            chatWs.current.close();
            roomListWs.current.close();
        };
    }, []);

	const login = async e => {
		e.preventDefault();
		await axios.post("http://localhost:8000/auth/login", formData)
		.then(response => {
			setUserData(response.data);
			onlineUsersWs.current.send(response.data.access_token);
		})
		.catch(error => {
			console.log(error.response.data);
		});
	}

	const sendText = e => {
		e.preventDefault();
		if (!userData.id) {
			alert("Not logged in")
		} else {
			chatWs.current.send(`${userData.username}: ${chatInput}`);
			setChatInput("");
		}
    };

    const createRoom = () => {
        axios.post("http://localhost:8000/game/create-room", {}, {withCredentials: true, headers: {"Authorization": `Bearer ${userData.access_token}`}})
        .then(response => {
            console.log(response.data);
        })
        .catch(error => {
            console.log(error.response.data);
        });
    };

	return (
		<div>
			<h3>Logged as: {userData.username}</h3>
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
				<textarea value={chatLines} cols="30" rows="10" disabled></textarea>
				<form onSubmit={sendText}>
				<input type="text" value={chatInput} onChange={e => setChatInput(e.target.value)}/>
				<input type="submit" value="send"/>
				</form>
			</div>
            <div>
                <div onClick={() => createRoom()}>CREATE ROOM</div>
            </div>
            <div>
                <ul>
                    {roomList.map((room, index) => <Link to={`/room/${room}/${userData.access_token}`} key={index}><li>Room id: {room}</li></Link>)}
                </ul>
            </div>
		</div>
	);
};

export default MainPage;
