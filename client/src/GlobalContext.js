import {createContext, useContext} from 'react';

export const GlobalContext = createContext(null);

const useGlobalContext = () => {
    return useContext(GlobalContext);
};

export default useGlobalContext;