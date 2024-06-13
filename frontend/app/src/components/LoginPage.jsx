import { useRef, useState, useCallback, useContext, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { EasyRequest, defHeaders, instanceURL } from "../api/helpers.js";
import logo from "../assets/LiveTestLogo.png";
import { AuthContext } from '../context/auth.jsx';

export const LoginPage = () => {
  const usernameRef = useRef('');
  const passwordRef = useRef('');
  const [loginAttempts, setLoginAttempts] = useState(0);
  const [invalidCredentials, setInvalidCredentials] = useState(false);
  const [tooManyAttempts, setTooManyAttemps] = useState(false);
  const [passwordForgotten, setPasswordForgotten] = useState(false);
  const { authDetails, updateAuthDetails } = useContext(AuthContext);

  const navigate = useNavigate();

  // Function to handle navigation
  const handleNavigate = (path) => () => {
    navigate(path);
  };

  // login to instance
  const loginHandler = useCallback(async (event) => {
    event.preventDefault();

    try {
      let body = {
        email: usernameRef.current.value,
        password: passwordRef.current.value
      };

      let req = await EasyRequest(`${instanceURL}/auth/login`, defHeaders, "POST", body);

      // ----------------- FOR DEBUGGING ---------------------
      console.log(req);
      console.log(req.data);

      console.log(`${req.status}`);
      console.log(loginAttempts);
      // -------------------------------------------------------
      // invalid credentials
      if (req.data.status_code === 404 || req.data.status_code === 401) {
        setInvalidCredentials(true);
      }
      else if (req.status === 200 && req.data.access_token) {
        setInvalidCredentials(false);

        updateAuthDetails({
          accessToken: req.data.access_token,
          isLoggedIn: true,
          type: req.data.type,
          id: req.data.id, 
          email: req.data.email,
          name: req.data.name
        });
        navigate("/course");
      }
      // Not connecting to database
      else if (req.data.status_code === 500) {
        setInvalidCredentials(false);
      }

      setLoginAttempts(prevAttempts => prevAttempts + 1);

      if (loginAttempts >= 5) {
        setTooManyAttemps(true);
        setTimeout(() => setTooManyAttemps(false), 30000); // 30 seconds lockout
      }

    } catch (error) {
      console.log(error);
    }
  }, [loginAttempts, updateAuthDetails, navigate]);

  useEffect(() => {
    if (authDetails.isLoggedIn) {
      console.log("useEffect for login");
      navigate("/course");
    }
  }, [authDetails, navigate]);

  function passwordForgottenHandler() {
    setPasswordForgotten(prevState => !prevState);
  }

  console.log(`authDetails: ${JSON.stringify(authDetails)}`);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-LogoBg px-6 py-12 lg:px-8">
      <div className="text-center">
        <h1 className="font-bold text-8xl text-cyan-500">LiveTest</h1>
        <img className="mx-auto h-40 w-auto" src={logo} alt="LiveTestLogo" />
      </div>
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-lg shadow-md">
        <div className="text-center">
          <h2 className="text-center text-2xl font-bold text-gray-700">
            Log in as a teacher or student
          </h2>
        </div>

        <form className="space-y-6" onSubmit={loginHandler}>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-900">
              Email
            </label>
            <div className="mt-2">
              <input
                id="email"
                type="email"
                required
                ref={usernameRef}
                name="email"
                autoComplete="email"
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm sm:leading-6"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between">
              <label htmlFor="password" className="block text-sm font-medium text-gray-900">
                Password
              </label>
              <div className="text-sm" onClick={passwordForgottenHandler}>
                <p className="font-semibold text-cyan-500 hover:text-cyan-300 cursor-pointer">
                  Forgot password?
                </p>
              </div>
            </div>
            <div className="mt-2">
              <input
                id="password"
                name="password"
                ref={passwordRef}
                type="password"
                autoComplete="current-password"
                required
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm sm:leading-6"
              />
            </div>
          </div>
          
          {invalidCredentials && <p className="text-red-600 mt-2">Wrong username/password, please try again</p>}
          {tooManyAttempts && <p className="text-red-600 mt-2">You have attempted to login more than 5 times, please wait 30 seconds and try again.</p>}
          
          <div className="text-center text-sm text-gray-500">
            <p>
              Don't have an account?{" "}
              <a
                href="/register"
                className="font-semibold leading-6 text-cyan-500 hover:text-cyan-300"
              >
                Register here
              </a>
            </p>
          </div>

          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-cyan-500 hover:bg-cyan-600 transition-colors duration-200 ease-in-out px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:text-cyan-700"
            >
              Sign in
            </button>
          </div>
        </form>

        {passwordForgotten && <h2 className="text-red-700 mt-4 text-center">Please contact your instance administrator and notify them of the lockout</h2>}
      </div>
    </div>
  );
}
