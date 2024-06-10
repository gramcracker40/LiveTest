// CoursePage.jsx
import React, { useEffect, useState, useContext } from 'react';
import { EasyRequest, defHeaders, instanceURL } from "../../api/helpers.js";
import { AuthContext } from '../../context/auth.jsx';
import { NavBar } from './navBar.jsx';
import { useNavigate } from 'react-router-dom';

export const CoursePage = () => {
  const [courses, setCourses] = useState([]);
  const [teacherNames, setTeacherNames] = useState({});
  const [tests, setTests] = useState([]);
  const [upcomingTests, setUpcomingTests] = useState([]);
  const { authDetails } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!authDetails.isLoggedIn) {
      navigate("/");
      return;
    }

    const courseURL = instanceURL + `/course/${authDetails.type}/${authDetails.id}`;

    const fetchCourses = async () => {
      try {
        let req = await EasyRequest(courseURL, defHeaders, "GET");
        if (req.status === 200) {
          const fetchedCourses = req.data.map(course => ({
            ...course,
            tests: course.tests || [], // Ensure tests is an array
          }));
          setCourses(fetchedCourses);
          fetchTeacherNames(fetchedCourses);
        }
      } catch (error) {
        console.error('Error fetching courses', error);
      }
    };

    fetchCourses();
  }, [authDetails, navigate]);

  useEffect(() => {
    const allTests = courses.flatMap(course => course.tests || []);
    setTests(allTests);
  }, [courses]);

  useEffect(() => {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const oneWeekLater = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 7);
  
    const filteredTests = tests.filter(test => {
      const testStart = new Date(test.start_t);
      const testEnd = new Date(test.end_t);
  
      return (testStart >= today && testStart <= oneWeekLater) || (now >= testStart && now <= testEnd);
    }).sort((a, b) => new Date(a.start_t) - new Date(b.start_t));
  
    setUpcomingTests(filteredTests);
  }, [tests]);
  

  const fetchTeacherNames = async (courses) => {
    const teacherIds = [...new Set(courses.map(course => course.teacher_id))];
    const fetchedTeacherNames = {};

    await Promise.all(
      teacherIds.map(async (teacherId) => {
        try {
          const req = await EasyRequest(`${instanceURL}/users/teachers/${teacherId}`, defHeaders, "GET");
          if (req.status === 200) {
            fetchedTeacherNames[teacherId] = req.data.name;
          }
        } catch (error) {
          console.error('Error fetching teacher details', error);
          fetchedTeacherNames[teacherId] = 'Unknown';
        }
      })
    );

    setTeacherNames(fetchedTeacherNames);
  };

  const handleDateFormatting = (start, end) => {
    const testStart = new Date(start);
    const testEnd = new Date(end);
    const now = new Date();

    if (now >= testStart && now <= testEnd) {
      return "LIVE";
    } else if (testStart.toDateString() === now.toDateString()) {
      return `Today at ${testStart.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })}`;
    } else {
      const day = String(testStart.getDate());
      const month = String(testStart.getMonth() + 1);
      const year = String(testStart.getFullYear()).slice(2);
      return `${month}-${day}-${year}`;
    }
  };

  const handleNavigate = (path, state) => {
    navigate(path, { state });
  };

  return (
    <div className="min-h-screen mx-auto w-full bg-cyan-50">
      <NavBar />
      <div className='sm:px-28 sm:py-8 px-4 py-4'>
        <div className='grid grid-cols-1 gap-x-8 mb-7 p-4 rounded-lg shadow bg-white'>
        <h1 className='text-3xl text-cyan-800 mb-4 font-bold'>Upcoming Tests</h1>
        <ul>
          {upcomingTests.map((test, index) => (
            <li key={index} className='text-lg text-gray-700 flex justify-between'>
              <span>{test.name}</span>
              {handleDateFormatting(test.start_t, test.end_t) === "LIVE" ? (
                <>
                  {(authDetails.type === 'student' || authDetails.type === 'teacher') && (
                    <a
                      onClick={() => handleNavigate(`/submission/${test.id}`, { test })}
                      className="text-md cursor-pointer text-cyan-500 hover:text-cyan-700"
                    >
                      LIVE
                    </a>
                  )}
                </>
              ) : (
                <span>{handleDateFormatting(test.start_t, test.end_t)}</span>
              )}
            </li>
          ))}
        </ul>

        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-8">
          {courses.map((course, index) => (
            <React.Fragment key={course.id}>
              <div className="mb-8 p-4 bg-white rounded-lg shadow transform transition duration-300 hover:text-cyan-700 hover:scale-105 hover:cursor-pointer"
                   onClick={() => handleNavigate(`/course/${course.id}`)}>
                <div className={`Course-${index} mb-4`}>
                  <span className="text-xl font-semibold">{course.name}</span>
                  <div className="text-md font-light">Course Number: {course.course_number}</div>
                  <div className="text-md font-light">Subject: {course.subject}</div>
                  <div className="text-md font-light">Instructor: {teacherNames[course.teacher_id]}</div>
                </div>
                <div className="Tests">
                  {course.tests.length > 0 ? (
                    course.tests.map((test, testIndex) => (
                      <div key={testIndex} className={`Test-${testIndex} flex justify-between`}>
                        <span className="text-md font-light">{test.name}</span>
                        <span className="text-md">{handleDateFormatting(test.start_t)}</span>
                      </div>
                    ))
                  ) : (
                    <div className="text-md">No tests</div>
                  )}
                </div>
              </div>
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
};
