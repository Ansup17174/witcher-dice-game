import {useState, useEffect} from 'react';
import RankingRow from '../components/ranking/RankingRow';
import RankingTable from '../components/ranking/RankingTable';
import RankingHeader from '../components/ranking/RankingHeader';
import RankingSelect from '../components/ranking/RankingSelect';
import RowHeader from '../components/ranking/RowHeader';
import useGlobalContext from '../GlobalContext';
import apiClient from '../apiclient';
import Header from '../components/Header';
import {Container} from '../components/containers';
import PageButton from '../components/page/PageButton';
import PageButtons from '../components/page/PageButtons';
import PageInput from '../components/page/PageInput';


const RankingPage = () => {
    const [rows, setRows] = useState([]);
    const [page, setPage] = useState(1);
    const [selectValue, setSelectValue] = useState("-");

    const getRows = async () => {
        await apiClient.get("/game/ranking",
            {params: {limit: 10, offset: (page-1)*10, game: selectValue !== "-" ? selectValue: null}}
        )
        .then(response => { 
            setRows(response.data);
        })
        .catch(error => {
            NotificationManager.error("Couldn't get ranking info", null, 2000);
        });
    };
    const {NotificationManager} = useGlobalContext();

    useEffect(() => getRows(), [page, selectValue]);

    const changePage = async number => {
        if (!Number.isInteger(Number.parseInt(number)) || number < 1) return;
        else setPage(Number.parseInt(number));
    };

    return (
        <Container>
            <Header>Ranking</Header>
            <RankingSelect value={selectValue} onChange={e => setSelectValue(e.target.value)}>
                <option disabled defaultValue>-</option>
                <option>Witcher-dice</option>
                <option>Tic-tac-toe</option>
                <option>Black-queen</option>
            </RankingSelect>
            <RankingTable>
                <RankingHeader>
                    <RowHeader>Username</RowHeader>
                    <RowHeader>Game</RowHeader>
                    <RowHeader>Matches won</RowHeader>
                    <RowHeader>Matches lost</RowHeader>
                    <RowHeader>Matches played</RowHeader>
                </RankingHeader>
                {rows.map((row, index) => <RankingRow key={index} stats={row}/>)}
            </RankingTable>
            <PageButtons>
                <PageButton onClick={() => changePage(page-1)}>&lt;</PageButton>
                <PageInput type="number" value={page} onChange={e => changePage(e.target.value)}/>
                <PageButton onClick={() => changePage(page+1)}>&gt;</PageButton>
            </PageButtons>
        </Container>
    );
};
    
export default RankingPage;