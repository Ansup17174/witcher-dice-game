import {useContext} from 'react';
import GlobalContext from '../GlobalContext';
import {Container, Row} from '../components/containers';
import Header from '../components/Header';

const ProfilePage = () => {
    
    const {userData} = useContext(GlobalContext);
    
    return (
        <Container>
            <Header>Profile</Header>
            <Row><span>Username:</span><span>{userData.username}</span></Row>
            <Row><span>E-mail:</span><span>{userData.email.address}</span></Row>
            <Row><span>Matches won:</span><span>{userData.profile.matches_won}</span></Row>
            <Row><span>Matches lost:</span><span>{userData.profile.matches_lost}</span></Row>
            <Row><span>Matches played:</span><span>{userData.profile.matches_played}</span></Row>
            <Row><span>Win ratio:</span><span>{Math.round(userData.profile.matches_won / userData.profile.matches_played)}</span></Row>
        </Container>
    );
};

export default ProfilePage;