import {Link} from 'react-router-dom';
import styled from 'styled-components';

const NavbarLink = styled(Link)`
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

export default NavbarLink;