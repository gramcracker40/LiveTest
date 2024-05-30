import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/auth";
import { LandingPage } from "./components/LandingPage";
import { RegisterPage } from "./components/RegisterPage";
import { LoginPage } from "./components/LoginPage";
import { AboutPage } from "./components/AboutPage";
import { CoursePage } from "./components/coursePage/coursePage";
import { SubmissionPage } from "./components/submissionPage/submissionPage";
import { CreateTestPage } from "./components/CreateTestPage";
import { CreateCoursePage } from "./components/CreateCoursePage";
import { AnalyticsPage } from "./components/AnalyticsPage";
import { ResetPassword} from "./components/ResetPassword";

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
          <Route path="/course/analytics" element={<AnalyticsPage />} />
          <Route path="/submission" element={<SubmissionPage />} />
          <Route path="/create-test" element={<CreateTestPage />} />
          <Route path="/create-course" element={<CreateCoursePage />} />
          <Route path="/reset-password" element={<ResetPassword />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};
