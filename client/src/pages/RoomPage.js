import {useState, useEffect, useContext, useRef} from 'react';
import GlobalContext from '../GlobalContext';
import {useParams} from 'react-router-dom';
import {FormField} from '../components/form';
import {Container, Row, GameContainer} from '../components/containers';
import Header from '../components/Header';

const RoomPage = () => {

    const {roomId} = useParams();
    const [gameState, setGameState] = useState({});
    const {userData, NotificationManager, webSocketBase} = useContext(GlobalContext);
    const roomWs = useRef(null);

    useEffect(() => {
        roomWs.current = new WebSocket(webSocketBase + `/room/${roomId}`);
        roomWs.current.onopen = () => roomWs.current.send(JSON.stringify({
            action: "authorize",
            access_token: localStorage.getItem("dice-token")
        }));
        roomWs.current.onmessage = message => setGameState(JSON.parse(message.data));
        roomWs.current.onclose = e => NotificationManager.info("Connection closed", null, 2000);
        
    }, []);

    return (
        <Container>
            <Header>Score: 2-1</Header>
            <Header>Opponent's turn</Header>
            <GameContainer>
                <Header>Player2</Header>
            </GameContainer>
            <GameContainer>
                <Header>You</Header>
            </GameContainer>
        </Container>
    );
};

export default RoomPage;