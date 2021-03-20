import {useParams} from 'react-router-dom';
import WitcherRoomPage from '../pages/WitcherRoomPage';
import TicTacToeRoomPage from '../pages/TicTacToeRoomPage';
import BlackQueenRoomPage from '../pages/BlackQueenRoomPage';
import NotFound from '../pages/NotFound';

const RoomRedirect = () => {
    const {roomId, game} = useParams();

    switch (game) {
        case "Witcher-dice":
            return <WitcherRoomPage roomId={roomId}/>
        case "Tic-tac-toe":
            return <TicTacToeRoomPage roomId={roomId}/>
        case "Black-queen":
            return <BlackQueenRoomPage roomId={roomId} />
        default:
            return <NotFound />
    }
};

export default RoomRedirect;