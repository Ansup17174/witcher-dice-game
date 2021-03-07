import styled from 'styled-components';

const PageButton = styled.div`
    background-color: green;
    transition: 0.1s linear;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    margin: 0 50px;
    font-weight: bold;
    font-size: 20px;
    cursor: pointer;
    

    &:hover {
        background-color: rgb(75, 245, 66);
    }
`;

export default PageButton;