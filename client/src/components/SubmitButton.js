import styled from 'styled-components';

const SubmitButton = styled.input`
    color: white;
    background-color: green;
    padding: 20px 60px;
    margin: 10px 0;
    font-size: 20px;
    outline: none;
    border: none;
    cursor: pointer;
    transition: linear 0.25s;

    &:hover {
        background-color: rgb(75, 245, 66);
    }
`;

export default SubmitButton;