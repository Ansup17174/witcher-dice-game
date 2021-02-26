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