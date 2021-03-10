import styled from 'styled-components';
import {Link} from 'react-router-dom';
import {FiAlignJustify} from 'react-icons/fi';

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

    @media only screen and (max-width: 768px) {
        font-size: 25px;
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

    @media only screen and (max-width: 768px) {
        font-size: 20px;
        font-weight: bold;
        height: 60px;
        padding: 10px 20px;
        border-bottom: 1.5px solid rgb(50, 50, 50);
        border-top: 1.5px solid rgb(50, 50, 50);
        width: 100%;
        justify-content: center;
    }
`;

export const NavbarLinks = styled.div`
    list-style-type: none;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;

    @media only screen and (max-width: 768px) {
        display: ${props => props.navbarDropdown ? "flex" : "none"};
        flex-direction: column;
        justify-content: start;
        position: absolute;
        width: 100%;
        height: calc(100vh-70px);
        top: 70px;
        background-color: rgb(20, 20, 20);
    }
`;


export const NavbarButton = styled(FiAlignJustify)`
    display: none;
    color: white;
    transition: 0.1s linear;

    &:hover {
        background-color: rgb(70, 70, 70);
    }

    @media only screen and (max-width: 768px) {
        height: 100%;
        width: 50px;
        padding: 0 10px;
        display: block;
        font-size: 25px;
        margin: 0 10px;
    }
`;