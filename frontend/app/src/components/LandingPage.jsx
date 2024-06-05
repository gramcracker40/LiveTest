import { useContext, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { AuthContext } from '../context/auth.jsx';

export const LandingPage = () => {
  let navigate = useNavigate();

  const { authDetails, updateAuthDetails } = useContext(AuthContext);

  // Function to handle navigation
  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 px-6 py-24 text-center shadow-2xl">
      <div className="w-full max-w-2xl">
        <h2 className="mx-auto text-cyan-500 text-8xl font-bold tracking-tight">
          LiveTest
        </h2>
        <p className="mt-6 text-lg leading-8 text-gray-300">
          A modern, in-person, testing solution
        </p>
        <div className="mt-10 flex items-center justify-center gap-x-6">
          <button
            onClick={() => handleNavigate("/login")}
            className="rounded-md bg-cyan-300 px-3.5 py-2.5 text-sm font-semibold
                    text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline 
                    focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
          >
            Login
          </button>
          <button
            onClick={() => handleNavigate("/register")}
            className="text-sm font-semibold leading-6 text-white"
          >
            Register <span aria-hidden="true">→</span>
          </button>
        </div>
        <div className="mt-10">
          <button
            onClick={() => handleNavigate("/about")}
            className="rounded-md bg-cyan-200 px-5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
          >
            About
          </button>
        </div>
      </div>
    </div>
  );
};
