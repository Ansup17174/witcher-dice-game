import styled from 'styled-components';

const PageButton = styled.div`
    background-color: green;
    transition: 0.1s linear;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    margin: 0 30px;
    font-weight: bold;
    font-size: 20px;
    cursor: pointer;

    &:hover {
        background-color: rgb(75, 245, 66);
    }

    @media only screen and (max-width: 768px) {
        margin: 0 10px;
    }
`;

export default PageButton;