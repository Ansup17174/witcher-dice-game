import styled from 'styled-components';
import {useContext} from 'react';
import GlobalContext from '../../GlobalContext';
import NavbarLinks from './NavbarLinks';
import NavbarLink from './NavbarLink';
import Logo from './Logo';

let Navbar = ({className}) => {

    const {userData, setUserData, NotificationManager} = useContext(GlobalContext);

    const logout = () => {
        localStorage.removeItem("dice-token");
        setUserData({});
        NotificationManager.success("Succesfully logged out!", null, 2000);
    };

    return (
        <div className={className}>
            <Logo to="/">Dice game</Logo>
            <NavbarLinks>
                <NavbarLink to="/register">Register</NavbarLink>
                <NavbarLink onClick={logout}>Logout</NavbarLink>
            </NavbarLinks>
        </div>
    );

};

Navbar = styled(Navbar)`
    height: 10vh;
    color: black;
    background-color: rgb(40, 40, 40);
    display: flex;
    align-items: center;
    justify-content: space-around;
    box-shadow: 0 0 2px 0;
`;

export default Navbar;