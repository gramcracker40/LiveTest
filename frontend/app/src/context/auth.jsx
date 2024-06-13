import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [authDetails, setAuthDetails] = useState({
        accessToken: "",
        isLoggedIn: false,
        type: "",
        id: null, 
        email: "",
        name: ""
    });

    useEffect(() => {
        // Load auth details from localStorage on initial load
        const storedAuthDetails = localStorage.getItem('authDetails');
        if (storedAuthDetails) {
            setAuthDetails(JSON.parse(storedAuthDetails));
        }
    }, []);

    // Update both state and localStorage when authDetails changes
    const updateAuthDetails = (newAuthDetails) => {
        setAuthDetails(newAuthDetails);
        localStorage.setItem('authDetails', JSON.stringify(newAuthDetails));
    };

    return (
        <AuthContext.Provider value={{ authDetails, updateAuthDetails }}>
            {children}
        </AuthContext.Provider>
    );
};
