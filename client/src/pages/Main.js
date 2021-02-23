import styled from 'styled-components';
import LoginForm from '../components/LoginForm';

let Main = () => {
    
    return (
        <LoginForm />
    );
};

Main = styled(Main)`
    display: flex;
    justify-content: center;
`;

export default Main;