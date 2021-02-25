import {useState, useContext} from 'react';
import {Form, FormHeader, FormField, FormError, FormText, Input, FormLink, SubmitButton} from './form';
import GlobalContext from '../GlobalContext';
import apiClient from '../apiclient';


const LoginForm = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(false);
    const {getUserData, NotificationManager} = useContext(GlobalContext);

    const login = async e => {
        e.preventDefault();
        await apiClient.post("/auth/login", {username, password})
        .then(response => {
            localStorage.setItem("dice-token", response.data.access_token);
            getUserData();
            setError(false);
            NotificationManager.success(`Succesfully logged in as ${response.data.username}`, "Logged in", 2000);
        })
        .catch(error => {
            setError(true);
        });
    };

    return (
        <Form onSubmit={login}>
            <FormHeader>Login</FormHeader>
                <FormField>
                    <FormText>Username</FormText>
                    <Input type="text" required value={username} onChange={e => setUsername(e.target.value)}/>
                </FormField>
                <FormField>
                    <FormText>Password</FormText>
                    <Input type="password" required value={password} onChange={e => setPassword(e.target.value)}/>
                </FormField>
                <FormLink to="/register">Dont have an account?</FormLink>
                {error && <FormError>Unable to login with given credentials</FormError>}
            <SubmitButton type="submit" value="Login"/>
        </Form>
    );
};



export default LoginForm;