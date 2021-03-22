import {useState, useRef, useEffect} from 'react';
import {useHistory} from 'react-router-dom';
import {Container} from '../components/containers';
import {GameButtons} from '../components/games';
import SmallButton from '../components/SmallButton';
import useGlobalContext from '../GlobalContext';

// NOT FINISHED

const BlackQueenRoomPage = ({roomId}) => {
    
    const history = useHistory();
    const [gameState, setGameState] = useState({
        players: [],
        score: [],
        ready: [false, false, false],
        deck: {
            s: [],
            c: [],
            d: [],
            h: []
        },
        table: [],
        is_finished: true,
        turn: 1,
        deal: 0,
    });

    const {userData, NotificationManager, webSocketBase} = useGlobalContext();
    const spectatorMode = !gameState.players.includes(userData.username);
    const yourIndex = gameState.players.indexOf(userData.username) > -1 ? gameState.players.indexOf(userData.username) : 0;
    const roomWs = useRef(null);

    useEffect(() => {
        roomWs.current = new WebSocket(webSocketBase + `/room/${roomId}`);
        roomWs.current.onopen = () => roomWs.current.send(JSON.stringify({
            action: "authorize",
            access_token: localStorage.getItem("dice-token")
        }));
        roomWs.current.onmessage = message => setGameState(JSON.parse(message.data));
        roomWs.current.onerror = e => history.push("/");
        roomWs.current.onclose = e => NotificationManager.info("Game finished", null, 2000);

        return () => roomWs.current.close();
    }, []);

    const sendReady = async () => {
        const data = {
            action: 'ready'
        };
        await roomWs.current.send(JSON.stringify(data));
    };
    
    return (
        <Container>
            {!spectatorMode && gameState.players.length === 3 && <GameButtons>
                {!gameState.is_finished && !gameState.ready[yourIndex] &&
                <SmallButton type="submit" value="Ready" color="rgb(20, 149, 168)" hoverColor="rgb(31, 211, 237)"
                onClick={() => sendReady()}/>}
            </GameButtons>}
        </Container>
    );

};

export default BlackQueenRoomPage;