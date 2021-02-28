import styled from 'styled-components';

export const Container = styled.div`
    background-color: rgb(50, 50, 50);
    width: 70%;
    text-align: center;
    padding: 50px;
    margin: 40px 0;
`;

export const ColumnContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    align-items: center;
    justify-content: center;
    min-height: 90vh;
`;

export const Row = styled.div`
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: center;
    font-size: 25px;
    margin: 10px 0;
`;
