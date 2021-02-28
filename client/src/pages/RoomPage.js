import {useState, useEffect, useReducer, useContext, useRef} from 'react';
import GlobalContext from '../GlobalContext';
import {GameContainer, GameButtons, GameDices, GameSpace, DiceImage, GameText} from '../components/game';
import {useParams} from 'react-router-dom';
import {Container} from '../components/containers';
import SmallButton from '../components/SmallButton';
import Header from '../components/Header';

const RoomPage = () => {

    const patterns = [
        "Nothing", "Para", "Dwie pary", "Trojka", "Maly St", "Duzy St", "Full", "Kareta", "Poker"
    ];
    const {roomId} = useParams();
    const [gameState, setGameState] = useState({
        players: [],
        score: [0, 0],
        dices: [
            [6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6]
        ],
        dices_value: [0, 0],
        current_player: 0,
        turn: 1,
        deal: 1,
        is_finished: false,
        ready: [false, false]
    });

    const reducer = (state, action) => {
        if (!gameState.ready[0] || !gameState.ready[1]) {
            return state;
        }
        switch (action.type) {
            case 0:
                return {...state, 0: !state[0]};
            case 1:
                return {...state, 1: !state[1]};
            case 2:
                return {...state, 2: !state[2]};
            case 3:
                return {...state, 3: !state[3]};
            case 4:
                return {...state, 4: !state[4]};
            default:
                return state;
        }
    };

    const [selectedDices, dispatch] = useReducer(reducer, {
        0: false,
        1: false,
        2: false,
        3: false,
        4: false
    });

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
                <GameText>Pattern: {patterns[gameState.dices_value[0]]}</GameText>
                <GameDices>
                    <DiceImage src={`/images/dice${gameState.dices[1][0]}.png`} alt={`dice${gameState.dices[1][0]}`}/>
                    <DiceImage src={`/images/dice${gameState.dices[1][1]}.png`} alt={`dice${gameState.dices[1][1]}`}/>
                    <DiceImage src={`/images/dice${gameState.dices[1][2]}.png`} alt={`dice${gameState.dices[1][2]}`}/>
                    <DiceImage src={`/images/dice${gameState.dices[1][3]}.png`} alt={`dice${gameState.dices[1][3]}`}/>
                    <DiceImage src={`/images/dice${gameState.dices[1][4]}.png`} alt={`dice${gameState.dices[1][4]}`}/>
                </GameDices>
            </GameContainer>
            <GameSpace />
            <GameContainer>
                <GameDices>
                    <DiceImage src={`/images/dice${gameState.dices[0][0]}.png`} alt={`dice${gameState.dices[0][0]}`}
                    selected={selectedDices[0]} onClick={() => dispatch({type: 0})}/>
                    <DiceImage src={`/images/dice${gameState.dices[0][1]}.png`} alt={`dice${gameState.dices[0][1]}`}
                    selected={selectedDices[1]} onClick={() => dispatch({type: 1})}/>
                    <DiceImage src={`/images/dice${gameState.dices[0][2]}.png`} alt={`dice${gameState.dices[0][2]}`}
                    selected={selectedDices[2]} onClick={() => dispatch({type: 2})}/>
                    <DiceImage src={`/images/dice${gameState.dices[0][3]}.png`} alt={`dice${gameState.dices[0][3]}`}
                    selected={selectedDices[3]} onClick={() => dispatch({type: 3})}/>
                    <DiceImage src={`/images/dice${gameState.dices[0][4]}.png`} alt={`dice${gameState.dices[0][4]}`}
                    selected={selectedDices[4]} onClick={() => dispatch({type: 4})}/>
                </GameDices>
                <GameText>You</GameText>
                <GameText>Pattern: {patterns[gameState.dices_value[1]]}</GameText>
            </GameContainer>
            <GameButtons>
                <SmallButton type="submit" value="Ready" color="rgb(20, 149, 168)" hoverColor="rgb(31, 211, 237)"/>
                {gameState.ready[0] && <SmallButton type="submit" value="Pass" color="rgb(214, 166, 21)" hoverColor="rgb(255, 199, 28)"/>}
                {gameState.ready[0] && <SmallButton type="submit" value="Roll" color="green" hoverColor="rgb(75, 245, 66)"/>}
            </GameButtons>
        </Container>
    );
};

export default RoomPage;

