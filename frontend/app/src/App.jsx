/*
Landing page for LiveTest
*/
import React from 'react';
import { Link } from 'react-router-dom';

/* <li>
<Link to="/register">Register</Link>
</li> */
const App = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 px-6 py-24 text-center shadow-2xl">
      <div className="w-full max-w-2xl">
        <h2 className="mx-auto text-cyan-500 text-8xl font-bold tracking-tight">
          LiveTest
        </h2>
        <p className="mt-6 text-lg leading-8 text-gray-300">
          A modern testing solution
        </p>
        <div className="mt-10 flex items-center justify-center gap-x-6">
          <a
            href="/login"
            className="rounded-md bg-cyan-300 px-3.5 py-2.5 text-sm font-semibold
             text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline 
             focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
          >
            Login
          </a>
          <a
            href="/register"
            className="text-sm font-semibold leading-6 text-white"
          >
            Register <span aria-hidden="true">→</span>
          </a>
        </div>
        <div className='mt-10'>
          <a
            href="/about"
            className="rounded-md bg-cyan-200 px-5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
          >
            About
          </a>

        </div>
          

      </div>
    </div>
  );
};

export default App;