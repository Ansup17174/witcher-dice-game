import {useParams} from 'react-router-dom';
import {useState, useEffect, useRef} from 'react';
import jwt_decode from 'jwt-decode';


const GameRoom = () => {
    const patterns = ["Brak", "Para", "Dwie pary", "Trojka", "Maly St", "Duzy St", "Full", "Kareta", "Poker"]
    const {room_id, access_token} = useParams();
    const {sub} = jwt_decode(access_token);
    const [dicesToRoll, setDicesToRoll] = useState("");
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
        winner: null,
        ready: [false, false],
        deal_result: ""
    });
    const roomWs = useRef(null);

    useEffect(() => {
        roomWs.current = new WebSocket(`ws://localhost:8000/ws/room/${room_id}/${access_token}`);
        roomWs.current.onmessage = e => {
            setGameState(JSON.parse(e.data));
        };
        return () => {
            roomWs.current.close();
        };
    }, []);

    const rollDices = e => {
        e.preventDefault();
        if (!dicesToRoll.length) {
            return;
        }
        const data = {
            action: "roll",
            dices: dicesToRoll.split(" ").map(string => Number.parseInt(string))
        };
        setDicesToRoll("");
        roomWs.current.send(JSON.stringify(data));
    };

    const pass = () => {
        roomWs.current.send(JSON.stringify({action: 'pass'}));
    };

    const ready = () => {
        const data = {
            action: 'ready'
        };
        roomWs.current.send(JSON.stringify(data));
    };

    return (
        <div>
            <h3>Logged as {sub}</h3>
            <h3>Players: {gameState.players[0]}, {gameState.players[1]}</h3>
            {gameState.ready[0] && gameState.ready[1] && <h3>Current player: {gameState.players[gameState.current_player]}</h3>}
            <h4>Score: {gameState.score[0]}-{gameState.score[1]}</h4>
            <div>
                <h5>{gameState.players[0]} dices: {JSON.stringify(gameState.dices[0])}</h5>
                <h5>Pattern: {patterns[gameState.dices_value[0]]}</h5>
            </div>
            <div>
                <h5>{gameState.players[1]} dices: {JSON.stringify(gameState.dices[1])}</h5>
                <h5>Pattern: {patterns[gameState.dices_value[1]]}</h5>
            </div>
            {!gameState.is_finished && gameState.players[gameState.current_player] === sub && gameState.ready[0] && gameState.ready[1] && 
                <div>
                <form onSubmit={rollDices}>
                <input type="text" value={dicesToRoll} onChange={e => setDicesToRoll(e.target.value)}/>
                <input type="submit" value="Roll"/>
                </form>
                <input type="submit" value="Pass" onClick={pass}/>
            </div>}
            {!gameState.is_finished && !gameState.ready[gameState.players.indexOf(sub)] && <input type="submit" value="Ready" onClick={ready}/>}
            {(!gameState.ready[0] || !gameState.ready[1]) && <div>
                    {gameState.ready[0] && <h4>Player 1 ready</h4>}
                    {gameState.ready[1] && <h4>Player 2 ready</h4>}
                </div>}
            <div>
                <h3>Turn: {gameState.turn}</h3>
                <h3>Deal: {gameState.deal}</h3>
            </div>
            <div>
                {gameState.deal_result && <h1>{gameState.deal_result}</h1>}
                {gameState.score[0] === 2 && <h1>Player 1 wins</h1>}
                {gameState.score[1] === 2 && <h1>Player 2 wins</h1>}
            </div>
        </div>
    );
}; 

export default GameRoom;
