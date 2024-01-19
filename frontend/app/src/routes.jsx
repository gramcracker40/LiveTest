import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/auth';

import App from './App';
import Register from './components/register';
import Login from './components/login';
import About from './components/about'
import CoursePage from './components/coursePage/coursePage'
import SubmissionPage from './components/submissionPage/submissionPage';

const AppRoutes = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/about" element={<About />} />
          <Route path="/course" element={<CoursePage />} />
          <Route path="/submission" element={<SubmissionPage />} />
        </Routes>
      </Router>
    </AuthProvider>
      
  );
};

export default AppRoutes;
