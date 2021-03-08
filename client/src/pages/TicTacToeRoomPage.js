import {useState, useEffect, useReducer, useRef} from 'react';
import useGlobalContext from '../GlobalContext';
import {GameContainer, GameButtons, GameSpace, GameText, TicTacToeImage, TicTacToeTable, TicTacToeRow,
    SmallTicTacToeImage} from '../components/games';
import {useHistory} from 'react-router-dom';
import {Container, ImagesRow} from '../components/containers';
import SmallButton from '../components/SmallButton';
import Header from '../components/Header';

const TicTacToeRoomPage = ({roomId}) => {

    const history = useHistory();
    const [gameState, setGameState] = useState({
        players: [],
        score: [0, 0],
        board: [
            0, 0, 0,
            1, 1, 1,
            0, 0, 0
        ],
        current_player: 0,
        round: 1,
        is_finished: false,
        ready: [false, false],
        winner: null,
        round_result: null
    });

    const {userData, NotificationManager, webSocketBase} = useGlobalContext();
    const spectatorMode = !gameState.players.includes(userData.username);
    const yourIndex = gameState.players.indexOf(userData.username) > -1 ? gameState.players.indexOf(userData.username) : 0;
    const opponentIndex = yourIndex ? 0 : 1;
    const roomWs = useRef(null);

    const makeMove = async index => {
        if (!gameState.ready[0] || !gameState.ready[1] || gameState.current_player !== yourIndex || spectatorMode) {
            return;
        }
        await roomWs.current.send(JSON.stringify({action: "move", index: index}));
    };

    const sendReady = async () => {
        const data = {
            action: 'ready'
        };
        await roomWs.current.send(JSON.stringify(data));
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
                <ImagesRow>
                    <GameText><SmallTicTacToeImage src={`/images/${yourIndex}.png`} />You</GameText>
                    <GameText><SmallTicTacToeImage src={`/images/${opponentIndex}.png`} />{gameState.players[opponentIndex]}</GameText>
                </ImagesRow>
            </GameContainer>
            <GameSpace>
                {!gameState.is_finished && gameState.round_result !== -1 && gameState.round_result !== null &&
                    (!gameState.ready[0] || !gameState.ready[1]) &&
                    <Header>{gameState.players[gameState.round_result]} gets the point</Header>}
                {gameState.winner && <GameText>{gameState.winner} wins</GameText>}
                {!gameState.is_finished && gameState.round_result === -1 && <Header>It's a tie!</Header>}
                {gameState.players[0] && (!gameState.ready[0] || !gameState.ready[1]) && !gameState.is_finished &&
                    <GameText>{gameState.ready[0] ? `${gameState.players[0]} ready` : `${gameState.players[0]} not ready`}</GameText>
                }
                {gameState.players[1] && (!gameState.ready[0] || !gameState.ready[1]) && !gameState.is_finished &&
                    <GameText>{gameState.ready[1] ? `${gameState.players[1]} ready` : `${gameState.players[1]} not ready`}</GameText>
                }
            </GameSpace>
            <TicTacToeTable>
                <TicTacToeRow>
                    <TicTacToeImage src={gameState.board[0] ? `/images/${gameState.board[0]}.png` : "/images/blank.png"}
                     onClick={() => makeMove(0)}/>
                    <TicTacToeImage src={gameState.board[1] ? `/images/${gameState.board[1]}.png` : "/images/blank.png"}
                     onClick={() => makeMove(1)}/>
                    <TicTacToeImage src={gameState.board[2] ? `/images/${gameState.board[2]}.png` : "/images/blank.png"}
                     onClick={() => makeMove(2)}/>
                </TicTacToeRow>
                <TicTacToeRow>
                <TicTacToeImage src={gameState.board[3] ? `/images/${gameState.board[3]}.png` : "/images/blank.png"}
                     onClick={() => makeMove(3)}/>
                    <TicTacToeImage src={gameState.board[4] ? `/images/${gameState.board[4]}.png` : "/images/blank.png"}
                     onClick={() => makeMove(4)}/>
                    <TicTacToeImage src={gameState.board[4] ? `/images/${gameState.board[4]}.png` : "/images/blank.png"}
                     onClick={() => makeMove(4)}/>
                </TicTacToeRow>
                <TicTacToeRow>
                <TicTacToeImage src={gameState.board[5] ? `/images/${gameState.board[5]}.png` : "/images/blank.png"}
                     onClick={() => makeMove(5)}/>
                    <TicTacToeImage src={gameState.board[6] ? `/images/${gameState.board[6]}.png` : "/images/blank.png"}
                     onClick={() => makeMove(6)}/>
                    <TicTacToeImage src={gameState.board[7] ? `/images/${gameState.board[7]}.png` : "/images/blank.png"}
                     onClick={() => makeMove(7)}/>
                </TicTacToeRow> 
            </TicTacToeTable>
            {!spectatorMode && <GameButtons>
                {!gameState.ready[yourIndex] && gameState.score[0] !== 2 && gameState.score[1] !== 2 &&
                <SmallButton type="submit" value="Ready" color="rgb(20, 149, 168)" hoverColor="rgb(31, 211, 237)"
                onClick={() => sendReady()}/>}
            </GameButtons>}
        </Container>
    );
};

export default TicTacToeRoomPage;
