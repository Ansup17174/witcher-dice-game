import styled from 'styled-components';
import {Link} from 'react-router-dom';

export const Logo = styled(Link)`
    display: flex;
    text-decoration: none;
    align-items: center;
    color: white;
    font-size: 30px;
    font-weight: bold;
    cursor: pointer;
    padding: 0 20px;
    height: 100%;
    transition: linear 0.1s;

    &:hover {
        background-color: rgb(70, 70, 70);
    }
`;

export const NavbarLink = styled(Link)`
    color: white;
    text-decoration: none;
    display: flex;
    align-items: center;
    font-size: 20px;
    cursor: pointer;
    transition: linear 0.1s;
    height: 100%;
    padding: 0 20px;

    &:hover {
        background-color: rgb(70, 70, 70);
    }
`;

export const NavbarLinks = styled.div`
    list-style-type: none;
    display: flex;
    justify-content: center;
    height: 100%;
`;