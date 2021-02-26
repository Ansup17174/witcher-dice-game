import styled from 'styled-components';

const BlueButton = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    background-color: rgb(52, 134, 235);
    transition: linear 0.25s;
    cursor: pointer;
    padding: 0 20px;
    height: 40px;
    font-size: 20px;

    &:hover {
        background-color: rgb(52, 192, 235);
    }
`;

export default BlueButton;