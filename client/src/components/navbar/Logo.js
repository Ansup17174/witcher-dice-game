import styled from 'styled-components';
import {Link} from 'react-router-dom';

const Logo = styled(Link)`
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

export default Logo;