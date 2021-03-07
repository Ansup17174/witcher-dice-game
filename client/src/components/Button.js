import styled from 'styled-components';

const Button = styled.input`
    color: white;
    background-color: ${props => props.color};
    padding: 20px 60px;
    margin: 20px 0;
    font-size: 20px;
    outline: none;
    border: none;
    cursor: pointer;
    transition: linear 0.25s;

    &:hover {
        background-color: ${props => props.hoverColor};
    }
`;

export default Button;