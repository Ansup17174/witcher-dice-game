import styled from 'styled-components';
import useGlobalContext from '../GlobalContext';
import {NavbarLinks, NavbarLink, Logo, NavbarButton} from './navbars';

let Navbar = ({className, navbarDropdown, setNavbarDropdown}) => {

    const {userData, setUserData, NotificationManager} = useGlobalContext();

    const logout = () => {
        localStorage.removeItem("dice-token");
        setUserData({});
        NotificationManager.success("Succesfully logged out!", null, 2000);
    };

    return (
        <div className={className}>
            <Logo to="/" onClick={() => setNavbarDropdown(false)}>Game center</Logo>
            <NavbarLinks navbarDropdown={navbarDropdown}  onClick={() => setNavbarDropdown(false)}>
                {userData.id && <NavbarLink to="/change-password">Change password</NavbarLink>}
                {userData.id && <NavbarLink to="/profile">Profile</NavbarLink>}
                <NavbarLink to="/ranking">Ranking</NavbarLink>
                <NavbarLink to="/register">Register</NavbarLink>
                {userData.id && <NavbarLink onClick={logout}>Logout</NavbarLink>}
            </NavbarLinks>
            <NavbarButton onClick={() => setNavbarDropdown(!navbarDropdown)}/>
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