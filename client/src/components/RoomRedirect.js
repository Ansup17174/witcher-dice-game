import {useParams} from 'react-router-dom';
import WitcherRoomPage from '../pages/WitcherRoomPage';
import NotFound from '../pages/NotFound';

const RoomRedirect = () => {
    const {roomId, game} = useParams();

    switch (game) {
        case "Witcher-dice":
            return <WitcherRoomPage roomId={roomId}/>
        default:
            return <NotFound />
    }
};

export default RoomRedirect;