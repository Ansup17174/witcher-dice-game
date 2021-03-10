import {Link} from 'react-router-dom';
import styled from 'styled-components';

export const Form = styled.form`
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    justify-content: space-evenly;
    background-color: rgb(50, 50, 50);
    min-height: 300px;
    width: 30%;
    padding: 50px 0;
    margin: 50px 0;

    @media only screen and (max-width: 768px) {
        width: 70%;
    }
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

    @media only screen and (max-width: 768px) {
        font-size: 25px;
    }
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
    padding: 0 5px;
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

    @media only screen and (max-width: 768px) {
        width: 70%;
    }
`;