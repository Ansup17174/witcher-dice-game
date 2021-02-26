import {useState, useEffect, useContext, useRef} from 'react';
import GlobalContext from '../GlobalContext';
import BlueButton from '../components/BlueButton';
import WhiteLink from '../components/WhiteLink';
import {SubmitButton} from '../components/form';
import {Container, ColumnContainer, Row} from '../components/containers';
import Header from '../components/Header';
import {ChatArea, ChatInput, ChatSubmit} from '../components/game';
import apiClient from '../apiclient';

const MainPage = () => {

    const chatWs = useRef(null);
    const roomListWs = useRef(null);
    const [chatState, setChatState] = useState([]);
    const [chatInput, setChatInput] = useState("");
    const [roomList, setRoomList] = useState([]);
    const {webSocketBase, NotificationManager, onlineUsers} = useContext(GlobalContext);

    useEffect(() => {
        chatWs.current = new WebSocket(webSocketBase + "/chat");
        roomListWs.current = new WebSocket(webSocketBase + "/room-list");

        const authorize = async () => {
            await chatWs.current.send(JSON.stringify({
                action: "authorize",
                access_token: localStorage.getItem("dice-token")
            }));
        };
        
        chatWs.current.onmessage = message => setChatState(JSON.parse(message.data));
        chatWs.current.onopen = () => authorize();
        chatWs.current.onerror = error => NotificationManager.error("Error while sending message", null, 2000);

        roomListWs.current.onmessage = message => setRoomList(JSON.parse(message.data));


        return () => {
            chatWs.current.close();
        };
    }, []);

    const sendText = async () => {
        if (!chatInput) return
        if (chatWs.current.readyState === 1) {
            await chatWs.current.send(JSON.stringify({
                action: "message",
                text: chatInput
            }));
            setChatInput("");
        } else {
            NotificationManager.error("Error while sending message", null, 2000);
        }
    };

    const createRoom = async () => {
        const token = localStorage.getItem("dice-token");
        await apiClient.post("/game/create-room", {}, {withCredentials: true, headers: {"Authorization": `Bearer ${token}`}})
        .then(response => {
            NotificationManager.success("Room created!", null, 2000);
        })
        .catch(error => {
            NotificationManager.error("Error occured while creating room", null, 2000);
        });
    };

    return (
        <ColumnContainer>
            <Container>
                <Header>Users online</Header>
                <div>
                    {onlineUsers.join(", ")}
                </div>
            </Container>
            <Container>
                <Header>Chat</Header>
                <ChatArea>
                    {chatState.map((line, index) => <div key={index}>{line}</div>)}
                </ChatArea>
                <Row>
                    <ChatInput type="text"
                    placeholder="Type..."
                    value={chatInput}
                    onChange={e => setChatInput(e.target.value)}
                    onKeyUp={e => e.key === "Enter" ? sendText() : null}
                    />
                    <ChatSubmit onClick={sendText}>Send</ChatSubmit>
                </Row>
            </Container>
            <Container>
                <Header>Room list</Header>
                <SubmitButton type="submit" value="Create room " onClick={() => createRoom()}/>
                {roomList.map((roomId, index) => (
                <Row key={index}><span>Room #{roomId}</span><WhiteLink to={`/room/${roomId}`}><BlueButton>Join</BlueButton></WhiteLink></Row>
                ))}
            </Container>
        </ColumnContainer>
    );
};

export default MainPage;