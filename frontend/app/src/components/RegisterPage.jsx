import React, { useRef, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import logo from '../assets/LiveTestLogo.png';
import { EasyRequest, defHeaders, instanceURL } from '../api/helpers';
import { BackButton } from './BackButton';

export const RegisterPage = () => {
  const nameRef = useRef('');
  const emailRef = useRef('');
  const passwordRef = useRef('');
  const confirmPasswordRef = useRef('');
  const [emailExists, setEmailExists] = useState(false);
  const [userRole, setUserRole] = useState('');
  const [formError, setFormError] = useState('');
  const [registrationError, setRegistrationError] = useState(false);
  const [passwordMismatchError, setPasswordMismatchError] = useState(false);
  const navigate = useNavigate();

  const handleRoleSelect = (role) => {
    setUserRole(role);
  };

  const handleNavigate = (path) => {
    navigate(path);
  };

  const registerHandler = (event) => {
    event.preventDefault();

    const password = passwordRef.current.value;
    const confirmPassword = confirmPasswordRef.current.value;

    if (password !== confirmPassword) {
      setPasswordMismatchError(true);
      setFormError('Passwords do not match, please try again');
      return;
    }

    if (!userRole) {
      setFormError("Please select either 'Teacher' or 'Student'");
      return;
    }

    setFormError('');
    setPasswordMismatchError(false);
    registerUser();
  };

  const registerUser = async () => {
    let userURL = instanceURL + '/users/';

    if (userRole === 'Teacher') {
      userURL += 'teachers/';
    } else if (userRole === 'Student') {
      userURL += 'students/';
    } else {
      return;
    }

    const body = {
      name: nameRef.current.value,
      email: emailRef.current.value,
      password: passwordRef.current.value,
    };

    try {
      const req = await EasyRequest(userURL, defHeaders, 'POST', body);
      if (req.status === 200) {
        navigate('/login');
      } else if (req.status === 400 && req.data.message === 'Email already exists') {
        setFormError('Email already exists. Please use a different email.');
        setEmailExists(true);
      } else {
        setRegistrationError(true);
      }
    } catch (error) {
      console.error('Error creating user', error);
      setRegistrationError(true);
    }
  };

  return (
    <div className="bg-LogoBg w-full min-h-screen flex flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md lg:max-w-lg xl:max-w-xl">
        <h1 className="font-bold text-center mb-4 text-cyan-500 text-6xl lg:text-8xl">
          LiveTest
        </h1>
        <img className="mx-auto h-52 w-auto" src={logo} alt="LiveTestLogo" />
        <h2 className="mt-10 text-center text-xl font-bold leading-9 tracking-tight text-gray-700">
          Register for an account
        </h2>
      </div>

      <div className="mt-4 sm:mx-auto sm:w-full sm:max-w-sm">
        <form className="space-y-6" onSubmit={registerHandler}>
          <div className="flex items-center space-x-4 justify-center">
            <label
              className={`px-8 py-4 text-sm font-semibold rounded-md shadow-sm cursor-pointer ${userRole === 'Teacher' ? 'bg-cyan-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
              onClick={() => handleRoleSelect('Teacher')}
            >
              Teacher
            </label>
            <label
              className={`px-8 py-4 text-sm font-semibold rounded-md shadow-sm cursor-pointer ${userRole === 'Student' ? 'bg-cyan-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
              onClick={() => handleRoleSelect('Student')}
            >
              Student
            </label>
          </div>
          <div>
            <label htmlFor="name" className="block text-sm font-medium leading-6 text-gray-900">
              Name
            </label>
            <div className="mt-2">
              <input
                id="name"
                ref={nameRef}
                name="name"
                required
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm sm:leading-6"
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
              Email
            </label>
            <div className="mt-2">
              <input
                id="email"
                ref={emailRef}
                name="email"
                type="email"
                required
                autoComplete="email"
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm sm:leading-6"
              />
            </div>
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium leading-6 text-gray-900">
              Password
            </label>
            <div className="mt-2">
              <input
                id="password"
                ref={passwordRef}
                name="password"
                type="password"
                required
                autoComplete="new-password"
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm sm:leading-6"
              />
            </div>
          </div>

          <div>
            <label htmlFor="confirm-password" className="block text-sm font-medium leading-6 text-gray-900">
              Confirm Password
            </label>
            <div className="mt-2">
              <input
                id="confirm-password"
                ref={confirmPasswordRef}
                name="confirmPassword"
                type="password"
                required
                autoComplete="new-password"
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm sm:leading-6"
              />
            </div>
            {formError && <h2 className="text-red-600">{formError}</h2>}
          </div>

          {registrationError && (
            <h2 className="text-red-600">
              Email already exists. <Link to="/reset-password" className="underline text-cyan-500">Reset Password</Link>
            </h2>
          )}

          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-cyan-500 hover:bg-cyan-600 transition-colors duration-300 ease-in-out px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:text-cyan-700"
            >
              Register
            </button>
          </div>
        </form>
        <div className="flex justify-center mt-4">
          <BackButton route="/" className="px-8 py-3 text-sm font-semibold rounded-md shadow-sm bg-cyan-200 text-gray-700 hover:bg-cyan-300" />
        </div>
      </div>
    </div>
  );
};
