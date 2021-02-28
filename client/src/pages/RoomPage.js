import {useState, useEffect, useContext, useRef} from 'react';
import GlobalContext from '../GlobalContext';
import {GameContainer, GameButtons, GameDices, GameSpace, DiceImage, GameText} from '../components/game';
import {useParams} from 'react-router-dom';
import {Container, Row} from '../components/containers';
import SmallButton from '../components/SmallButton';
import Header from '../components/Header';

const RoomPage = () => {

    const {roomId} = useParams();
    const [gameState, setGameState] = useState({
        players: [],
        score: [0, 0],
        dices: [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        dices_value: [0, 0],
        current_player: 0,
        turn: 1,
        deal: 1,
        is_finished: false,
        ready: [false, false]
    });
    const [selectedDices, setSelectedDices] = useState({
        0: false,
        1: false,
        2: false,
        3: false,
        4: false
    })
    const {NotificationManager, webSocketBase} = useContext(GlobalContext);
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
            <GameText>Room {roomId}</GameText>
                <GameText>Score: {`${gameState.score[0]}-${gameState.score[1]}`}</GameText>
                <Header>
                    {gameState.players.length === 2 ? 
                    (gameState.current_player === 0 ? "Your turn" : "Opponent's turn") : "Waiting for an opponent"}
                </Header>
            <GameContainer>
                <GameText>Player2</GameText>
                <GameDices>
                    <DiceImage src="/images/dice1.png" alt="dice1"/>
                    <DiceImage src="/images/dice2.png" alt="dice2"/>
                    <DiceImage src="/images/dice3.png" alt="dice3"/>
                    <DiceImage src="/images/dice4.png" alt="dice4"/>
                    <DiceImage src="/images/dice5.png" alt="dice5"/>
                </GameDices>
            </GameContainer>
            <GameSpace />
            <GameContainer>
                <GameDices>
                    <DiceImage src="/images/dice1.png" alt="dice1" selected={selectedDices[0]}
                    onClick={() => setSelectedDices({...selectedDices, 0: !selectedDices[0]})}/>
                    <DiceImage src="/images/dice2.png" alt="dice2" selected={selectedDices[1]}
                    onClick={() => setSelectedDices({...selectedDices, 1: !selectedDices[1]})}/>
                    <DiceImage src="/images/dice3.png" alt="dice3" selected={selectedDices[2]}
                    onClick={() => setSelectedDices({...selectedDices, 2: !selectedDices[2]})}/>
                    <DiceImage src="/images/dice4.png" alt="dice4" selected={selectedDices[3]}
                    onClick={() => setSelectedDices({...selectedDices, 3: !selectedDices[3]})}/>
                    <DiceImage src="/images/dice5.png" alt="dice5" selected={selectedDices[4]}
                    onClick={() => setSelectedDices({...selectedDices, 4: !selectedDices[4]})}/>
                </GameDices>
                <GameText>You</GameText>
            </GameContainer>
            <GameButtons>
                <SmallButton type="submit" value="Ready" color="rgb(20, 149, 168)" hoverColor="rgb(31, 211, 237)"/>
                <SmallButton type="submit" value="Pass" color="rgb(214, 166, 21)" hoverColor="rgb(255, 199, 28)"/>
                <SmallButton type="submit" value="Roll" color="green" hoverColor="rgb(75, 245, 66)"/>
            </GameButtons>
        </Container>
    );
};

export default RoomPage;

