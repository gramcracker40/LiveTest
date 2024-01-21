<<<<<<< HEAD
=======
// import React from "react";
>>>>>>> f2bd9bd65ecc134a74c2614e19ba0bce2be76c37
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/auth";

import { LandingPage } from "./components/LandingPage";
import { RegisterPage } from "./components/RegisterPage";
import { LoginPage } from "./components/LoginPage";
import { AboutPage } from "./components/AboutPage";
<<<<<<< HEAD
import { CoursePage } from "./components/CoursePage/CoursePage";
=======
import { CoursePage } from "./components/coursePage/coursePage";
>>>>>>> f2bd9bd65ecc134a74c2614e19ba0bce2be76c37
import { SubmissionPage } from "./components/submissionPage/submissionPage";

export const AppRoutes = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/course" element={<CoursePage />} />
          <Route path="/submission" element={<SubmissionPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};
