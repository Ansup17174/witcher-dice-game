import {useState, useEffect} from 'react';
import {useHistory} from 'react-router-dom';
import useGlobalContext from '../GlobalContext';
import {Container, Row} from '../components/containers';
import Header from '../components/Header';

const ProfilePage = () => {
    
    const [userProfile, setUserProfile] = useState({
        username: "",
        email: {
            address: ""
        },
        profile: {
            matches_won: 0,
            matches_lost: 0,
            matches_played: 0
        }
    })
    const {userData} = useGlobalContext();
    const history = useHistory();

    useEffect(() => {
        if (!userData.id) history.push("/");
        setUserProfile(userData);
    }, [])

    const calculateWinRatio = number => {
        return Math.round(number * 100) + '%';
    };
    return (
        <Container>
            <Header>Profile</Header>
            <Row><span>Username:</span><span>{userProfile.username}</span></Row>
            <Row><span>E-mail:</span><span>{userProfile.email.address}</span></Row>
            <Row><span>Matches won:</span><span>{userProfile.profile.matches_won}</span></Row>
            <Row><span>Matches lost:</span><span>{userProfile.profile.matches_lost}</span></Row>
            <Row><span>Matches played:</span><span>{userProfile.profile.matches_played}</span></Row>
            <Row><span>Win ratio:</span><span>{calculateWinRatio(userProfile.profile.matches_won / userProfile.profile.matches_played)}</span></Row>
        </Container>
    );
};

export default ProfilePage;