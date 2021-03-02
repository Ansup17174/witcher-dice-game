import {useState, useEffect, useReducer, useContext, useRef} from 'react';
import GlobalContext from '../GlobalContext';
import {GameContainer, GameButtons, GameDices, GameSpace, DiceImage, GameText} from '../components/game';
import {useParams, useHistory} from 'react-router-dom';
import {Container} from '../components/containers';
import SmallButton from '../components/SmallButton';
import Header from '../components/Header';

const RoomPage = () => {

    const patterns = [
        "Nothing", "Para", "Dwie pary", "Trojka", "Maly St", "Duzy St", "Full", "Kareta", "Poker"
    ];
    const history = useHistory();
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
        ready: [false, false],
        winner: null
    });

    const {userData, NotificationManager, webSocketBase} = useContext(GlobalContext);
    const spectatorMode = !gameState.players.includes(userData.username);
    const yourIndex = gameState.players.indexOf(userData.username) > -1 ? gameState.players.indexOf(userData.username) : 0;
    const opponentIndex = yourIndex ? 0 : 1;
    const roomWs = useRef(null);

    const reducer = (state, action) => {
        if (!gameState.ready[0] || !gameState.ready[1] || gameState.current_player !== yourIndex || spectatorMode) {
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
            case "reset":
                return {
                0: false,
                1: false,
                2: false,
                3: false,
                4: false
            };
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

    const sendReady = async () => {
        const data = {
            action: 'ready'
        };
        roomWs.current.send(JSON.stringify(data));
    };

    const sendPass = async () => {
        const data = {
            action: 'pass'
        };
        roomWs.current.send(JSON.stringify(data));
    };

    const sendDices = async () => {
        const dices = Object.entries(selectedDices).filter(([key, value]) => value).map(([key, value]) => Number.parseInt(key));
        if (!dices.length) return
        const data = {
            action: 'roll',
            dices: dices
        };
        roomWs.current.send(JSON.stringify(data));
        dispatch({type: "reset"});
    };

    useEffect(() => {
        roomWs.current = new WebSocket(webSocketBase + `/room/${roomId}`);
        roomWs.current.onopen = () => roomWs.current.send(JSON.stringify({
            action: "authorize",
            access_token: localStorage.getItem("dice-token")
        }));
        roomWs.current.onmessage = message => setGameState(JSON.parse(message.data));
        roomWs.current.onerror = e => history.push("/");
        roomWs.current.onclose = e => NotificationManager.info("Game finished", null, 2000);
    }, []);

    return (
        <Container>
            <GameText>Room {roomId}</GameText>
                <GameText>Score: {`${gameState.score[0]}-${gameState.score[1]}`}</GameText>
                <Header>
                    {gameState.players.length === 2 ? 
                    (gameState.ready[0] && gameState.ready[1] ? 
                    (spectatorMode ? `${gameState.players[gameState.current_player]}'s turn` :
                        (gameState.players[gameState.current_player] === userData.username ? "Your turn" : "Opponent's turn")) : null)
                     : "Waiting for an opponent"}
                </Header>
            <GameContainer>
                {gameState.players.length === 2 && <GameText>{gameState.players[0] === userData.username ? 
                gameState.players[1] : gameState.players[0]}</GameText>}
                <GameText>Pattern: {patterns[gameState.dices_value[opponentIndex]]}</GameText>
                <GameDices>
                    <DiceImage src={`/images/dice${gameState.dices[opponentIndex][0]}.png`} alt={`dice${gameState.dices[opponentIndex][0]}`}/>
                    <DiceImage src={`/images/dice${gameState.dices[opponentIndex][1]}.png`} alt={`dice${gameState.dices[opponentIndex][1]}`}/>
                    <DiceImage src={`/images/dice${gameState.dices[opponentIndex][2]}.png`} alt={`dice${gameState.dices[opponentIndex][2]}`}/>
                    <DiceImage src={`/images/dice${gameState.dices[opponentIndex][3]}.png`} alt={`dice${gameState.dices[opponentIndex][3]}`}/>
                    <DiceImage src={`/images/dice${gameState.dices[opponentIndex][4]}.png`} alt={`dice${gameState.dices[opponentIndex][4]}`}/>
                </GameDices>
            </GameContainer>
            <GameSpace>
                {!gameState.is_finished && gameState.deal_result !== "" && 
                <Header>{gameState.players[gameState.deal_result]} gets the point</Header>}
                {gameState.winner && <GameText>{gameState.winner} wins</GameText>}
            </GameSpace>
            <GameContainer>
                <GameDices>
                    <DiceImage src={`/images/dice${gameState.dices[yourIndex][0]}.png`} alt={`dice${gameState.dices[0][0]}`}
                    selected={selectedDices[0]} onClick={() => dispatch({type: 0})}/>
                    <DiceImage src={`/images/dice${gameState.dices[yourIndex][1]}.png`} alt={`dice${gameState.dices[0][1]}`}
                    selected={selectedDices[1]} onClick={() => dispatch({type: 1})}/>
                    <DiceImage src={`/images/dice${gameState.dices[yourIndex][2]}.png`} alt={`dice${gameState.dices[0][2]}`}
                    selected={selectedDices[2]} onClick={() => dispatch({type: 2})}/>
                    <DiceImage src={`/images/dice${gameState.dices[yourIndex][3]}.png`} alt={`dice${gameState.dices[0][3]}`}
                    selected={selectedDices[3]} onClick={() => dispatch({type: 3})}/>
                    <DiceImage src={`/images/dice${gameState.dices[yourIndex][4]}.png`} alt={`dice${gameState.dices[0][4]}`}
                    selected={selectedDices[4]} onClick={() => dispatch({type: 4})}/>
                </GameDices>
                <GameText>{spectatorMode ? gameState.players[0] : "You"}</GameText>
                <GameText>Pattern: {patterns[gameState.dices_value[yourIndex]]}</GameText>
            </GameContainer>
            {!spectatorMode && <GameButtons>
                {!gameState.ready[yourIndex] && gameState.score[0] !== 2 && gameState.score[1] !== 2 &&
                <SmallButton type="submit" value="Ready" color="rgb(20, 149, 168)" hoverColor="rgb(31, 211, 237)"
                onClick={() => sendReady()}/>}
                {gameState.ready[0]
                && gameState.ready[1]
                && gameState.current_player === yourIndex
                && <SmallButton type="submit" value="Pass" color="rgb(214, 166, 21)" hoverColor="rgb(255, 199, 28)"
                onClick={() => sendPass()}/>}
                {gameState.ready[0]
                && gameState.ready[1]
                && gameState.current_player === yourIndex
                && <SmallButton type="submit" value="Roll" color="green" hoverColor="rgb(75, 245, 66)"
                onClick={() => sendDices()}/>}
                {gameState.is_finished && <GameText>Game finished</GameText>}
            </GameButtons>}
        </Container>
    );
};

export default RoomPage;
