import {useState, useEffect, useReducer, useRef} from 'react';
import useGlobalContext from '../GlobalContext';
import {GameContainer, GameButtons, GameDices, GameSpace, DiceImage, GameText} from '../components/games';
import {useHistory} from 'react-router-dom';
import {FormLink} from '../components/forms/form';
import {Container} from '../components/containers';
import SmallButton from '../components/SmallButton';
import Header from '../components/Header';

const WitcherRoomPage = ({roomId}) => {

    const patterns = [
        "Nothing", "Para", "Dwie pary", "Trojka", "Maly St", "Duzy St", "Full", "Kareta", "Poker"
    ];
    const history = useHistory();
    const [gameState, setGameState] = useState({
        players: [],
        score: [0, 0],
        dices: [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        dices_value: [0, 0],
        current_player: null,
        round_result: null,
        turn: 0,
        deal: 1,
        is_finished: false,
        ready: [false, false],
        winner: null,
        timeout: null
    });

    const {userData, NotificationManager, webSocketBase} = useGlobalContext();
    const spectatorMode = !gameState.players.includes(userData.username);
    const yourIndex = gameState.players.indexOf(userData.username) > -1 ? gameState.players.indexOf(userData.username) : 0;
    const opponentIndex = yourIndex ? 0 : 1;
    const roomWs = useRef(null);

    const reducer = (state, action) => {
        if (!gameState.ready[0] || !gameState.ready[1] || gameState.current_player !== yourIndex
             || spectatorMode || gameState.is_finished || gameState.turn < 2) {
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
        dispatch({type: "reset"});
    };

    const sendPass = async () => {
        const data = {
            action: 'pass'
        };
        roomWs.current.send(JSON.stringify(data));
        dispatch({type: "reset"});
    };

    const sendDices = async () => {
        const dices = Object.entries(selectedDices).filter(([key, value]) => value).map(([key, value]) => Number.parseInt(key));
        if (!dices.length && gameState.turn > 1) return
        const data = {
            action: 'roll',
            dices: dices
        };
        roomWs.current.send(JSON.stringify(data));
        dispatch({type: "reset"});
    };

    const getDiceImage = (number, index) => {
        const dice = gameState.dices[index][number];
        if (dice) return `/images/dice${dice}.png`;
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
                {gameState.turn !== 0 && <GameText>Pattern: {patterns[gameState.dices_value[opponentIndex]]}</GameText>}
                {gameState.dices[opponentIndex][0] !== 0 && <GameDices>
                    <DiceImage src={getDiceImage(0, opponentIndex)} alt={`dice${gameState.dices[opponentIndex][0]}`}/>
                    <DiceImage src={getDiceImage(1, opponentIndex)} alt={`dice${gameState.dices[opponentIndex][1]}`}/>
                    <DiceImage src={getDiceImage(2, opponentIndex)} alt={`dice${gameState.dices[opponentIndex][2]}`}/>
                    <DiceImage src={getDiceImage(3, opponentIndex)} alt={`dice${gameState.dices[opponentIndex][3]}`}/>
                    <DiceImage src={getDiceImage(4, opponentIndex)} alt={`dice${gameState.dices[opponentIndex][4]}`}/>
                </GameDices>}
            </GameContainer>
            <GameSpace>
                {!gameState.is_finished && gameState.round_result !== -1 && gameState.round_result !== null &&
                    (!gameState.ready[0] || !gameState.ready[1]) &&
                    <Header>{gameState.players[gameState.round_result]} gets the point</Header>}
                {gameState.winner && <GameText>{gameState.winner} wins</GameText>}
                {gameState.round_result === -1 && <Header>It's a tie!</Header>}
                {gameState.players[0] && (!gameState.ready[0] || !gameState.ready[1]) && !gameState.is_finished &&
                    gameState.players.length === 2 &&
                    <GameText>{gameState.ready[0] ? `${gameState.players[0]} ready` : `${gameState.players[0]} not ready`}</GameText>
                }
                {gameState.players[1] && (!gameState.ready[0] || !gameState.ready[1]) && !gameState.is_finished && 
                    gameState.players.length === 2 &&
                    <GameText>{gameState.ready[1] ? `${gameState.players[1]} ready` : `${gameState.players[1]} not ready`}</GameText>
                }
                {gameState.is_finished && <Header>Game finished</Header>}
            </GameSpace>
            <GameContainer>
                {gameState.dices[yourIndex][0] !== 0 && <GameDices>
                    <DiceImage src={getDiceImage(0, yourIndex)} alt={`dice${gameState.dices[0][0]}`}
                    selected={selectedDices[0]} onClick={() => dispatch({type: 0})}/>
                    <DiceImage src={getDiceImage(1, yourIndex)} alt={`dice${gameState.dices[0][1]}`}
                    selected={selectedDices[1]} onClick={() => dispatch({type: 1})}/>
                    <DiceImage src={getDiceImage(2, yourIndex)} alt={`dice${gameState.dices[0][2]}`}
                    selected={selectedDices[2]} onClick={() => dispatch({type: 2})}/>
                    <DiceImage src={getDiceImage(3, yourIndex)} alt={`dice${gameState.dices[0][3]}`}
                    selected={selectedDices[3]} onClick={() => dispatch({type: 3})}/>
                    <DiceImage src={getDiceImage(4, yourIndex)} alt={`dice${gameState.dices[0][4]}`}
                    selected={selectedDices[4]} onClick={() => dispatch({type: 4})}/>
                </GameDices>}
                <GameText>{spectatorMode ? gameState.players[0] : "You"}</GameText>
                {gameState.turn !== 0 && <GameText>Pattern: {patterns[gameState.dices_value[yourIndex]]}</GameText>}
            </GameContainer>
            {gameState.timeout !== null && <GameText>Time left: {gameState.timeout}s</GameText>}
            {!spectatorMode && !gameState.is_finished &&  <GameButtons>
                {!gameState.ready[yourIndex] && gameState.score[0] !== 2 && gameState.score[1] !== 2 &&
                gameState.players.length === 2 && 
                <SmallButton type="submit" value="Ready" color="rgb(20, 149, 168)" hoverColor="rgb(31, 211, 237)"
                onClick={() => sendReady()}/>}
                {gameState.ready[0]
                && gameState.ready[1]
                && gameState.current_player === yourIndex
                && gameState.turn > 1
                && <SmallButton type="submit" value="Pass" color="rgb(214, 166, 21)" hoverColor="rgb(255, 199, 28)"
                onClick={() => sendPass()}/>}
                {gameState.ready[0]
                && gameState.ready[1]
                && gameState.current_player === yourIndex
                && <SmallButton type="submit" value="Roll" color="green" hoverColor="rgb(75, 245, 66)"
                onClick={() => sendDices()}/>}
            </GameButtons>}
            {gameState.is_finished && <FormLink to="/">Go to main page</FormLink>}
        </Container>
    );
};

export default WitcherRoomPage;
