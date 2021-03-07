import styled from 'styled-components';
import RankingData from './RankingData';

let RankingRow = ({stats, className}) => {
    return (
        <tr className={className}>
            <RankingData>{stats.username}</RankingData>
            <RankingData>{stats.game}</RankingData>
            <RankingData>{stats.matches_won}</RankingData>
            <RankingData>{stats.matches_lost}</RankingData>
            <RankingData>{stats.matches_played}</RankingData>
        </tr>
    );
};

RankingRow = styled(RankingRow)`
    height: 50px;
    border: 2px solid white;
`;

export default RankingRow;