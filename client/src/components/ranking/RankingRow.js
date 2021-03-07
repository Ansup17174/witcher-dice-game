import styled from 'styled-components';

let RankingRow = ({stats, className}) => {
    console.log(stats)
    return (
        <tr className={className}>
            <td>{stats.username}</td>
            <td>{stats.game}</td>
            <td>{stats.matches_won}</td>
            <td>{stats.matches_lost}</td>
            <td>{stats.matches_played}</td>
        </tr>
    );
};

RankingRow = styled(RankingRow)`
    height: 70px;
`;

export default RankingRow;