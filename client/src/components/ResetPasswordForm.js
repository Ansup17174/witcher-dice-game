import {useState, useContext} from 'react';
import {Form, FormField, FormHeader, Input, FormText, FormError} from './form';
import Button from '../components/Button';
import apiClient from '../apiclient';
import GlobalContext from '../GlobalContext';
import parseErrors from '../errorParser';

const ResetPasswordForm = () => {

    const [email, setEmail] = useState("");
    const [error, setError] = useState({});
    const {NotificationManager} = useContext(GlobalContext);

    const resetPassword = async e => {
        e.preventDefault();
        NotificationManager.info("Sending...", null, 2000);
        await apiClient.post("/auth/reset-password", {email: email})
        .then(response => {
            setError({});
            NotificationManager.success("New password sent!", null, 2000);
        })
        .catch(error => {
            parseErrors(error, setError);
        });
    };

    return (
        <Form onSubmit={resetPassword}>
            <FormHeader>Reset password</FormHeader>
            <FormField>
                <FormText>E-mail</FormText>
                <Input type="email" required value={email} onChange={e => setEmail(e.target.value)}/>
                {error.detail && <FormError>{error.detail}</FormError>}
            </FormField>
            <Button type="submit" value="Reset" color="green" hoverColor="rgb(75, 245, 66)"/>
        </Form>
    );
};

export default ResetPasswordForm;