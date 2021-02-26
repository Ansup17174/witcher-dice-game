import {Form, FormField, FormHeader, Input, SubmitButton, FormError, FormText} from './form';
import {useState, useContext} from 'react';
import GlobalContext from '../GlobalContext';
import apiClient from '../apiclient';

const ResendForm = () => {

    const [email, setEmail] = useState("");
    const [error, setError] = useState("");

    const {NotificationManager} = useContext(GlobalContext);

    const reSend = async e => {
        e.preventDefault();
        NotificationManager.info("Sending...", null, 2000);
        await apiClient.post("/auth/resend-verification-email", {email: email})
        .then(response => {
            NotificationManager.success("Verification e-mail sent!", null, 2000);
            setError("");
        })
        .catch(error => {
            setError(error.response.data.detail);
        });
    };

    return (
        <Form onSubmit={reSend}>
            <FormHeader>Re-send verification e-mail</FormHeader>
            <FormField>
                <FormText>E-mail</FormText>
                <Input type="email" required value={email} onChange={e => setEmail(e.target.value)}/>
                <FormError>{error}</FormError>
            </FormField>
            <SubmitButton type="submit" value="Re-send" />
        </Form>
    );
};

export default ResendForm;