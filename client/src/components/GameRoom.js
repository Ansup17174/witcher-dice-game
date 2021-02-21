import {useParams} from 'react-router-dom';
import {useState, useEffect, useRef} from 'react';


const GameRoom = () => {
    const {roomId} = useParams();
    const [gameState, setGameState] = useState({});
    const roomWs = useRef(null);

    useEffect(() => {
        roomWs.current = new WebSocket(`ws://localhost:8000/ws/${roomId}`);
        roomWs.current.onmessage = e => {
            setGameState(JSON.parse(e.data));
        };

        return () => {
            roomWs.current.close();
        };
    });
};

export default GameRoom;