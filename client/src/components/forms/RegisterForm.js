import {useReducer,  useState} from 'react';
import {Form, FormHeader, FormField, FormError, FormText, Input, FormLink} from './form';
import useGlobalContext from '../../GlobalContext';
import Button from '../Button';
import apiClient from '../../apiclient';
import parseErrors from '../../errorParser';


const RegisterForm = () => {

    const reducer = (state, action) => {
        switch (action.type) {
            case 'username':
                return {...state, username: action.payload};
            case 'email':
                return {...state, email: action.payload};
            case 'password1':
                return {...state, password1: action.payload};
            case 'password2':
                return {...state, password2: action.payload};
            default:
                return state;
        }
    };

    const [formState, dispatch] = useReducer(reducer, {
        username: "",
        email: "",
        password1: "",
        password2: ""
    });
    const [errors, setErrors] = useState({});

    const {username, email, password1, password2} = formState;

    const {NotificationManager} = useGlobalContext();

    const register = async e => {
        e.preventDefault();
        setErrors({});
        NotificationManager.info("Sending...", null, 2000);
        await apiClient.post("/auth/register", formState)
        .then(response => {
            NotificationManager.success(
                "Check your e-mail for confirmation",
                "Registered!",
                2000
            );
        })
        .catch(error => {
            parseErrors(error, setErrors);
        });
    };

    return (
        <Form onSubmit={register}>
            <FormHeader>Register</FormHeader>
            <FormField>
                <FormText>Username</FormText>
                <Input type="text" value={username} required onChange={e => {dispatch({type: 'username', payload: e.target.value})}}/>
                {errors.username && <FormError>{errors.username}</FormError>}
            </FormField>
            <FormField>
                <FormText>E-mail</FormText>
                <Input type="email" value={email} required onChange={e => dispatch({type: 'email', payload: e.target.value})}/>
                {errors.email && <FormError>{errors.email}</FormError>}
            </FormField>
            <FormField>
                <FormText>Password</FormText>
                <Input type="password" value={password1} required onChange={e => dispatch({type: 'password1', payload: e.target.value})}/>
                {errors.password1 && <FormError>{errors.password1}</FormError>}
            </FormField>
            <FormField>
                <FormText>Password again</FormText>
                <Input type="password" value={password2} required onChange={e => dispatch({type: 'password2', payload: e.target.value})}/>
                {errors.password2 && <FormError>{errors.password2}</FormError>}
            </FormField>
            <FormLink to="/resend-verification-email">Re-send activation e-mail</FormLink>
            {errors.detail && <FormError>{errors.detail}</FormError>}
            <Button type="submit" value="Register" color="green" hoverColor="rgb(75, 245, 66)" />
        </Form>
    );
};

export default RegisterForm;