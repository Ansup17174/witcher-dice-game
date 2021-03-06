import styled from 'styled-components';

const RankingSelect = styled.select`
    margin-top: 30px;
    width: 300px;
    height: 40px;
    background-color: rgb(33, 33, 33);
    color: white;
    outline: none;
    border: none;
    font-size: 20px;
    padding: 0 20px;

    @media only screen and (max-width: 768px) {
        width: 140px;
        font-size: 15px;
    }
`;

export default RankingSelect;