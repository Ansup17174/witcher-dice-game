import {Link} from 'react-router-dom';
import styled from 'styled-components';

export const Form = styled.form`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-evenly;
    background-color: rgb(50, 50, 50);
    min-height: 450px;
    width: 30%;
    padding: 50px 0;
`;


export const FormField = styled.div`
    margin: 10px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
`;

export const FormHeader = styled.h1`
    color: white;
    font-family: sans-serif;
    margin: 20px 0;
`;

export const FormLink = styled(Link)`
    color: white;
`;

export const FormText = styled.div`
    color: white;
    text-align: center;
    margin: 10px 0;
`;

export const FormError = styled(FormText)`
    color: red;
    font-weight: bold;
`;

export const Input = styled.input`
    width: 200px;
    height: 30px;
    font-size: 15px;
    padding: 5px;
    background-color: rgb(33, 33, 33);
    outline: none;
    border: none;
    color: white;
    margin: 5px 0px;
`;

export const SubmitButton = styled.input`
    color: white;
    background-color: green;
    padding: 20px 60px;
    margin: 10px 0;
    font-size: 20px;
    outline: none;
    border: none;
    cursor: pointer;
    transition: linear 0.4s;

    &:hover {
        background-color: rgb(75, 245, 66);
    }
`;