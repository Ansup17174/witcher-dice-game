import styled from 'styled-components';

export const ChatArea = styled.div`
    background-color: rgb(30, 30, 30);
    height: 200px;
    margin: 20px 0;
    text-align: left;
    padding: 10px;
    word-wrap: break-word;
    overflow-y: auto;
`;

export const ChatInput = styled.input`
    width: 100%;
    height: 40px;
    font-size: 15px;
    padding: 5px;
    background-color: rgb(33, 33, 33);
    outline: none;
    border: none;
    color: white;
    margin: 5px 20px 5px 0;
`;

export const ChatSubmit = styled.div`
    display: flex;
    align-items: center;
    color: white;
    background-color: green;
    height: 40px;
    padding: 0 20px;
    font-size: 20px;
    cursor: pointer;
    transition: linear 0.25s;

    &:hover {
        background-color: rgb(75, 245, 66);
    }
`;

export const GameButtons = styled.div`
    display: flex;
    width: 100%;
    justify-content: space-around;
    align-items: center;
    font-size: 25px;
    margin: 10px 0;
`;

export const GameDices = styled.div`
    display: flex;
    width: 100%;
    justify-content: space-evenly;
    align-items: center;
    margin: 50px 0;
`;

export const GameSpace = styled.div`
    height: 25px;
`;

export const GameContainer = styled.div`
    margin: 20px 0;
    width: 100%;
`;

export const GameText = styled.h3`
    color: white;
`;

export const DiceImage = styled.img`
    padding: 10px;
    width: 68px;
    height: 68px;
    transition: linear 0.1s;
    cursor: pointer;
    border-radius: 10%;
    ${props => props.selected ? "background-color: rgb(240, 240, 240) !important;" : null}

    &:hover {
        background-color: rgb(180, 180, 180);
    }
`;
