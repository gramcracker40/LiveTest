import { useRef, useState, useCallback } from 'react';
import { EasyRequest, loginURL, defHeaders } from "../api/helpers";
import CoursePage from "./coursePage/coursePage";
import logo from "../assets/LiveTestLogo.png"

export default function LoginPage() {
  const usernameRef = useRef('');
  const passwordRef = useRef('');
  const [loginAttempts, setLoginAttempts] = useState(0);
  const [invalidCredentials, setInvalidCredentials] = useState(false);
  const [tooManyAttempts, setTooManyAttemps] = useState(false);
  const [passwordForgotten, setPasswordForgotten] = useState(false);
  const [authDetails, setAuthDetails] = useState({
    isLoggedIn: false,
    accessToken: "",
    refreshToken: "",
    userID: null
  });

  const loginHandler = useCallback(async (event) => {
    event.preventDefault();

    try {
      let body = {
        username: usernameRef.current.value,
        password: passwordRef.current.value
      };

      let req = await EasyRequest(loginURL, defHeaders, "POST", body);
      setLoginAttempts(loginAttempts + 1);
      console.log(req.data)
      console.log(req.status)
      if (req.status === 200) {
        setInvalidCredentials(false);
        
        const authDetails = {
          isLoggedIn: true,
          accessToken: req.data.access_token,
          refreshToken: req.data.refresh_token,
          userID: req.data.user_id
        }
        setAuthDetails(authDetails);
        localStorage.setItem("authDetails", JSON.stringify(authDetails))
      }
      else if (req.status === 401) {
        setInvalidCredentials(true);
      }
      else if (req.status === 500) {
        setInvalidCredentials(false);
      }
    } catch (error) {
      console.log(error);
    }

    if (loginAttempts > 5) {
      setTimeout(() => {
        setTooManyAttemps(true);
      }, 3000)
    }
  });

  function passwordForgottenHandler() {
    setPasswordForgotten(true);
  }

  console.log(`authDetails: ${authDetails.isLoggedIn}`)

  if (authDetails.isLoggedIn) {
    return <CoursePage/>
  } else {
    return (
        <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
          <div className="sm:mx-auto sm:w-full sm:max-w-sm">
            <h1 className="text-5xl text-center mb-4 text-gray-500">
              <span className="text-green-600">
                Green
              </span>
              Watch
            </h1>
            <img
              className="mx-auto h-20 w-auto"
              src={logo}
              alt="Greenwatch"
            />
            <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-700">
              Sign in to your account
            </h2>
          </div>

          <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form className="space-y-6" onSubmit={loginHandler}>
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium leading-6 text-gray-900"
                >
                  Username
                </label>
                <div className="mt-2">
                  <input
                    id="email"
                    ref={usernameRef}
                    name="email"
                    autoComplete="email"
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-green-500 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between">
                  <label
                    htmlFor="password"
                    className="block text-sm font-medium leading-6 text-gray-900"
                  >
                    Password
                  </label>
                  <div className="text-sm" onClick={passwordForgottenHandler}>
                    <p
                      className="font-semibold text-green-600 hover:text-green-500"
                    >
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
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-green-500 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>

              {invalidCredentials && <h2 className="text-red-600">Wrong username/password, please try again</h2>}
              {tooManyAttempts && <h2 className="text-red-600">You have attempted to login more than 5 times, please wait 30 seconds and try again.</h2>}

              <div>
                <button
                  type="submit"
                  className="flex w-full justify-center rounded-md bg-green-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-green-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-green-800"
                >
                  Sign in
                </button>
              </div>
            </form>

            {passwordForgotten && <h2 className="text-red-700">Please contact your instance administrator and notify them of the lockout</h2>}

            {/* <p className="mt-10 text-center text-sm text-gray-500">
                Not a member?{" "}
                <a
                  href="#"
                  className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500"
                >
                  Start a 14 day free trial
                </a>
              </p> */}
          </div>
        </div>
    );
    }
}
