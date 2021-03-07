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
        }
    });
    const {userData} = useGlobalContext();
    const history = useHistory();

    useEffect(() => {
        if (!userData.id) history.push("/");
        setUserProfile(userData);
    }, [])

    // const calculateWinRatio = number => {
    //     return Math.round(number * 100) + '%';
    // };

    return (
        <Container>
            <Header>Profile</Header>
            <Row><span>Username:</span><span>{userProfile.username}</span></Row>
            <Row><span>E-mail:</span><span>{userProfile.email.address}</span></Row>
        </Container>
    );
};

export default ProfilePage;