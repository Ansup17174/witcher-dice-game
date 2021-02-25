import {useState, useContext} from 'react';
import {useHistory} from 'react-router-dom';
import {Form, FormError, FormField, FormHeader, FormText, Input, SubmitButton} from '../components/form';
import GlobalContext from '../GlobalContext';
import apiClient from '../apiclient';
import parseErrors from '../errorParser';

const ChangePasswordPage = () => {

    const [oldPassword, setOldPassword] = useState("");
    const [newPassword1, setNewPassword1] = useState("");
    const [newPassword2, setNewPassword2] = useState("");
    const [errors, setErrors] = useState("");
    const history = useHistory();
    const {NotificationManager} = useContext(GlobalContext);

    const changePassword = async e => {
        e.preventDefault();
        const data = {
            old_password: oldPassword,
            new_password1: newPassword1,
            new_password2: newPassword2
        };
        const token = localStorage.getItem('dice-token');
        await apiClient.post(
            "/auth/change-password",
            data,
            {withCredentials: true, headers: {"Authorization": `Bearer ${token}`}})
            .then(response => {
                NotificationManager.success("Password changed!", null, 2000);
                setErrors("");
            })
            .catch(error => {
                if (error.response.status === 401) {
                    NotificationManager.error("You're not logged in", null, 2000);
                    history.push("/login");
                } else {
                    parseErrors(error, setErrors);
                }
            });
    };

    return (
        <Form onSubmit={changePassword}>
            <FormHeader>Change password</FormHeader>
            <FormField>
                <FormText>Old password</FormText>
                <Input type="password" value={oldPassword} onChange={e => setOldPassword(e.target.value)}/>
                {errors.detail && <FormError>{errors.detail}</FormError>}
            </FormField>
            <FormField>
                <FormText>New password</FormText>
                <Input type="password" value={newPassword1} onChange={e => setNewPassword1(e.target.value)}/>
                {errors.new_password1 && <FormError>{errors.new_password1}</FormError>}
            </FormField>
            <FormField>
                <FormText>New password again</FormText>
                <Input type="password" value={newPassword2} onChange={e => setNewPassword2(e.target.value)}/>
                {errors.new_password2 && <FormError>{errors.new_password2}</FormError>}
            </FormField>
            <SubmitButton type="submit" value="Change password"/>
        </Form>
    );
};

export default ChangePasswordPage;