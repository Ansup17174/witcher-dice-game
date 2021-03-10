import styled from 'styled-components';

export const MainContainer = styled.div`
    display: flex;
    justify-content: center;
    min-height: calc(100vh - 70px);
    align-items: center;
`;


export const Container = styled.div`
    background-color: rgb(50, 50, 50);
    width: 70%;
    text-align: center;
    padding: 50px;
    margin: 40px 0;

    @media only screen and (max-width: 768px) {
        padding: 25px;
    }
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
    margin: 30px 0;

    @media only screen and (max-width: 1450px) {
        flex-direction: column;
        margin: 20px 0;
    }
`;


export const ImagesRow = styled.div`
    width: 100%;
    display: flex;
    justify-content: space-around;
    align-items: center;
`;