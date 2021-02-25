import {useParams} from 'react-router-dom';
import {useState, useEffect} from 'react';
import Container from '../components/Container';
import Header from '../components/Header';
import FormLink from '../components/form/FormLink';
import apiClient from '../apiclient';


const ConfirmEmail = () => {
    const [isConfirmed, setIsConfirmed] = useState(false);
    const {user_id, token} = useParams();

    useEffect(() => {
        apiClient.get(`/auth/confirm-email/${user_id}/${token}`)
        .then(response => {
            setIsConfirmed(true);
        });
    }, []);

    return (
        <Container>
            {isConfirmed ? <Header>E-mail confirmed succesfully</Header> :
            <Header>Invalid confirmation link</Header>}
            <FormLink to="/">Go to main page</FormLink>
        </Container>
    );
};

export default ConfirmEmail;