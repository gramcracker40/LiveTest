import { useRef, useState, useCallback, useContext } from 'react';
import { EasyRequest, defHeaders, loginURL } from "../api/helpers.js";
import CoursePage from "./coursePage/coursePage";
import logo from "../assets/LiveTestLogo.png"
import { AuthContext } from '../context/auth';

export default function LoginPage() {
  const usernameRef = useRef('');
  const passwordRef = useRef('');
  let [loginAttempts, setLoginAttempts] = useState(0);
  const [invalidCredentials, setInvalidCredentials] = useState(false);
  const [tooManyAttempts, setTooManyAttemps] = useState(false);
  const [passwordForgotten, setPasswordForgotten] = useState(false);
  const { authDetails, setAuthDetails } = useContext(AuthContext);

  // login to instance
  const loginHandler = useCallback(async (event) => {
    event.preventDefault();

    try {
      let body = {
        email: usernameRef.current.value,
        password: passwordRef.current.value
      };

      let req = await EasyRequest(loginURL, defHeaders, "POST", body);
      setLoginAttempts(loginAttempts++);
      console.log(req)
      console.log(req.data)

      console.log(req.status)
      console.log(loginAttempts)
      if (req.status === 200) {
        setInvalidCredentials(false);
        
        setAuthDetails({
          accessToken: req.data.access_token,
          isLoggedIn: true,
          type: req.data.type,
          id: req.data.id, 
          email: req.data.email,
          name: req.data.name
        })
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
    setPasswordForgotten(prevState => !prevState);
  }

  console.log(`authDetails: ${authDetails}`)

  if (authDetails.isLoggedIn) {
    return <CoursePage/>
  } else {
    return (
        <div className="bg-LogoBg w-full h-screen flex flex-col justify-center px-6 py-12 lg:px-8">
          <div className="sm:mx-auto sm:w-full sm:max-w-sm">
            <h1 className="font-bold text-8xl text-center mb-4 text-cyan-500">
              LiveTest
            </h1>
            <img
              className="mx-auto h-52 w-auto"
              src={logo}
              alt="LiveTestLogo"
            />
            <h2 className="mt-10 text-center text-xl font-bold leading-9 tracking-tight text-gray-700">
              Sign in to your student/teacher account
            </h2>
          </div>

          <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form className="space-y-6" onSubmit={loginHandler}>
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium leading-6 text-gray-900"
                >
                  Email
                </label>
                <div className="mt-2">
                  <input
                    id="email"
                    ref={usernameRef}
                    name="email"
                    autoComplete="email"
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm sm:leading-6"
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
                      className="font-semibold text-cyan-500 hover:text-cyan-300"
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
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>
              
              {invalidCredentials && <h2 className="text-red-600">Wrong username/password, please try again</h2>}
              {tooManyAttempts && <h2 className="text-red-600">You have attempted to login more than 5 times, please wait 30 seconds and try again.</h2>}

              <div>
                <button
                  type="submit"
                  className="flex w-full justify-center rounded-md bg-cyan-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:text-cyan-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:text-cyan-700"
                  href="/login/"
                >
                  Sign in
                </button>
              </div>
            </form>

            {passwordForgotten && <h2 className="text-red-700">Please contact your instance administrator and notify them of the lockout</h2>}

            { <p className="mt-10 text-center text-sm text-gray-500">
                Not a member?{" "}
                <a
                  href="#" // TODO: create link to registration page and backend configured for such offer
                  className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500"
                >
                  Start a 14 day free trial
                </a>
              </p> }
          </div>
        </div>
    );
    }
}
