import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/auth.jsx';

export const LogoutButton = () => {

  const { updateAuthDetails } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    // Reset authDetails to default state
    updateAuthDetails({
      accessToken: "",
      isLoggedIn: false,
      type: "",
      id: null,
      email: "",
      name: ""
    });
    // Navigate to the login page
    navigate("/");
  };

  return (
      <button onClick={handleLogout} className="logout-button-styles">
        Logout
      </button>
  );
};
