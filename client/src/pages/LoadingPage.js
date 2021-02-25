import styled from 'styled-components';

const LoadingPage = styled.div`
    position: fixed;
    color: white;
    display: flex;
    font-size: 50px;
    align-items: center;
    justify-content: center;
    width: 100vw;
    height: 100vh;
    background-color: rgb(30, 30, 30);
    overflow-y: hidden;
    transition: linear 0.2s;
    z-index: ${props => props.loading ? "1" : "-1"};
    opacity: ${props => props.loading ? "1" : "0"};
`;

export default LoadingPage;