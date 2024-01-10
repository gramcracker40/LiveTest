import React, { createContext, useState, useContext } from 'react';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [authDetails, setAuthDetails] = useState({
        accessToken:"",
        isLoggedIn: false,
        type: "",
        id: null, 
        email: "",
        name: ""
    });

    return (
        <AuthContext.Provider value={{ authDetails, setAuthDetails }}>
            {children}
        </AuthContext.Provider>
    );
};
