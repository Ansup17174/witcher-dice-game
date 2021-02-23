import {useState, useContext} from 'react';
import Input from './Input';
import SubmitButton from './SubmitButton';
import Form from './Form';
import FormHeader from './FormHeader';
import FormField from './FormField';
import FormError from './FormError';
import GlobalContext from '../GlobalContext';


let LoginForm = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(false);

    return (
        <Form>
            <FormHeader>Login</FormHeader>
                <FormField>
                    <Input type="text" placeholder="Username"/>
                </FormField>
                <FormField>
                    <Input type="password" placeholder="Password"/>
                </FormField>
                {error && <FormError>Unable to login with given credentials</FormError>}
            <SubmitButton type="submit" value="Login"/>
        </Form>
    );
};



export default LoginForm;