import styled from 'styled-components';
import {useContext} from 'react';
import GlobalContext from '../GlobalContext';
import {NavbarLinks, NavbarLink, Logo} from './navbars';

let Navbar = ({className}) => {

    const {userData, setUserData, NotificationManager} = useContext(GlobalContext);

    const logout = () => {
        localStorage.removeItem("dice-token");
        setUserData({});
        NotificationManager.success("Succesfully logged out!", null, 2000);
    };

    return (
        <div className={className}>
            <Logo to="/">Game center</Logo>
            <NavbarLinks>
                {userData.id && <NavbarLink to="/change-password">Change password</NavbarLink>}
                {userData.id && <NavbarLink to="/profile">Profile</NavbarLink>}
                <NavbarLink to="/ranking"></NavbarLink>
                <NavbarLink to="/register">Register</NavbarLink>
                {userData.id && <NavbarLink onClick={logout}>Logout</NavbarLink>}
            </NavbarLinks>
        </div>
    );
};

Navbar = styled(Navbar)`
    height: 70px;
    color: black;
    background-color: rgb(40, 40, 40);
    display: flex;
    align-items: center;
    justify-content: space-around;
    box-shadow: 0 0 2px 0;
`;

export default Navbar;