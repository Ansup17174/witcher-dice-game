import {useState, useEffect} from 'react';
import RankingRow from '../components/ranking/RankingRow';
import RankingTable from '../components/ranking/RankingTable';
import RankingHeader from '../components/ranking/RankingHeader';
import useGlobalContext from '../GlobalContext';
import apiClient from '../apiclient';
import Header from '../components/Header';
import {Container} from '../components/containers';

const RankingPage = () => {
    const [rows, setRows] = useState([]);

    const getRows = async () => {
        await apiClient.get("/game/ranking")
        .then(response => {
            setRows(response.data);
        })
        .catch(error => {
            NotificationManager.error("Couldn't get ranking info", null, 2000);
        });
    };
    const {NotificationManager} = useGlobalContext();

    useEffect(() => getRows());

    return (
        <Container>
            <Header>Ranking</Header>
            <RankingTable>
                <RankingHeader>
                    <th>Username</th>
                    <th>Game</th>
                    <th>Matches won</th>
                    <th>Matches lost</th>
                    <th>Matches played</th>
                </RankingHeader>
                {rows.map((row, index) => <RankingRow key={index} stats={row}/>)}
            </RankingTable>
        </Container>
    );
};

export default RankingPage;