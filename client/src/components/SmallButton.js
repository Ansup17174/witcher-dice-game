import styled from 'styled-components';

const SmallButton = styled.input`
    color: white;
    height: 100%;
    outline: none;
    border: none;
    background-color: ${props => props.color};
    transition: linear 0.25s;
    cursor: pointer;
    padding: 0 20px;
    margin: 10px 0;
    height: 40px;
    font-size: 20px;
    min-width: 150px;

    &:hover {
        background-color: ${props => props.hoverColor};
    }

    @media only screen and (max-width: 768px) {
        min-width: 100px;
    }
`;

export default SmallButton;