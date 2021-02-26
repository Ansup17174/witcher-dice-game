import {useState, useContext} from 'react';
import {Form, FormField, FormHeader, Input, FormText, FormError, SubmitButton} from './form';
import apiClient from '../apiclient';
import GlobalContext from '../GlobalContext';
import parseErrors from '../errorParser';

const ResetPasswordForm = () => {

    const [email, setEmail] = useState("");
    const [error, setError] = useState({});
    const {NotificationManager} = useContext(GlobalContext);

    const resetPassword = async e => {
        e.preventDefault();
        await apiClient.post("/auth/reset-password", {email: email})
        .then(response => {
            setError({});
            NotificationManager.success("New password sent!", null, 2000);
        })
        .catch(error => {
            setError(parseErrors(error, setError));
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
            <SubmitButton type="submit" value="Reset"/>
        </Form>
    );
};

export default ResetPasswordForm;