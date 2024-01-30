import React, { useEffect, useState, useContext } from 'react';
import { EasyRequest, defHeaders, instanceURL } from "../../api/helpers.js";
import { AuthContext } from '../../context/auth.jsx';
import { LogoutButton } from '../logoutButton.jsx';
import { useNavigate } from 'react-router-dom'

export const CoursePage = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [tests, setTests] = useState([]);
  const [upcomingTests, setUpcomingTests] = useState([]);
  const { authDetails, updateAuthDetails } = useContext(AuthContext);

  const navigate = useNavigate();

  const handleNavigate = (path, state) => {
    navigate(path, { state })
  }

  useEffect(() => {

    // ------------------------ AUTHENTICATION DETAILS ---------------------------

    // if a user isn't logged in, take them back to the login page
    if (!authDetails.isLoggedIn) {
      navigate("/")
      return
    }
    console.log(`Auth details --> ${JSON.stringify(authDetails)}`)

    // ---------------------------- FETCHING COURSES -----------------------------------

    // Fetch courses if not in cache
    const courseURL = instanceURL + `/course/${authDetails.type}/${authDetails.id}`

    console.log(`courseURL::: ${courseURL}`)

    // API request to get courses for that teacher
    const fetchCourses = async () => {
      try {
        let req = await EasyRequest(courseURL, defHeaders, "GET");
        console.log(`req.data --> ${JSON.stringify(req.data)}`)
        //  THE ACTUAL IF STATEMENT!!!!!
        // if (req.status === 200) {
        //   setCourses(req.data);
        // }
        if (req.status === 200) {
          const fetchedCourses = req.data.map(course => ({
            ...course,
            tests: course.tests || [], // Ensure tests is an array
          }));
          // Add fake tests here
          const coursesWithFakeTests = fetchedCourses.map(course => {
            let test_num = Math.floor(Math.random() * 5);
            let fakeTests = [];
            for (let i = 0; i < test_num; i++) {
              const day = String(Math.floor(Math.random() * 31) + 1).padStart(2, '0')
              fakeTests.push({
                "name": "Name of a Longer Test " + (i + 1),
                "start_t": `2024-01-${day}T10:00:00`,
                "end_t": `2024-01-${day}T20:00:00`
              });
            }
            return { ...course, tests: [...course.tests, ...fakeTests] };
          });
          setCourses(coursesWithFakeTests);
        }
        // Handle other status codes appropriately
      } catch (error) {
        console.error('Error fetching courses', error);
      }
    };

    fetchCourses();

  }, [authDetails, navigate]);

  //  ------------------------- GETTING ALL TESTS -----------------------------------

  useEffect(() => {

    console.log(`These are courses and tests\n${JSON.stringify(courses)}`)

    const allTests = courses.flatMap(course => course.tests || [])

    setTests(allTests); // Flatten all tests from each course

  }, [courses]); // This useEffect depends on the courses state

  //  ------------------------- GETTING UPCOMING TESTS -----------------------------------

  useEffect(() => {
    console.log(`tests: ${JSON.stringify(tests)}`)

    // Calculate upcoming tests only when courses data is updated
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate()); // Today at 12 AM
    const oneWeekLater = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 7);

    const filteredTests = tests.filter(test => {
      const testDate = new Date(test.start_t);
      return testDate >= today && testDate <= oneWeekLater;
    }).sort((a, b) => new Date(a.start_t) - new Date(b.start_t));

    setUpcomingTests(filteredTests);
  }, [tests])

  useEffect(() => {
    console.log(`upcoming tests: ${JSON.stringify(upcomingTests)}`)
  }, [upcomingTests])

  const handleDateFormatting = (start, end) => {
    // console.log(`before end: ${end}`)
    const testStart = new Date(start);
    const testEnd = new Date(end);
    const now = new Date();

    // console.log(`now: ${now}`)
    // console.log(`testStart: ${testStart}`)
    // console.log(`testEnd: ${testEnd}`)

    if (now >= testStart && now <= testEnd) {
      // Test is currently live
      return "LIVE";
    }
    // Check if the test date is the same as today's date
    else if (testStart.toDateString() === now.toDateString()) {
      // Format as "Today at HH:MM AM/PM"
      return `Today at ${testStart.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })}`;
    }
    else {
      // Format as "MM-DD-YY"
      const day = String(testStart.getDate())//.padStart(2, '0');
      const month = String(testStart.getMonth() + 1)//.padStart(2, '0');
      const year = String(testStart.getFullYear()).slice(2);
      return `${month}-${day}-${year}`;
    }
  }

  const handleCourseSelect = (courseId) => {
    setSelectedCourse(courseId);
  };

  // console.log(`Courses::: ${JSON.stringify(courses)}`);
  return (
    // <div className="course-page-container">
    //   <h1 className="text-2xl font-bold">Your Courses</h1>
    //   <div className="courses-list">
    //     {courses.map(course => (
    //       // <CourseCard key={course.id} course={course} /> // Render the CourseCard component
    //       // <div key={course.id} className="course-item">
    //       //   <h2>{course.name}</h2>
    //       //   {/* Additional course details */}
    //       // </div>
    //     ))}
    //     {!courses && <LoadingScreen></LoadingScreen>}
    //   </div>
    // </div>
    // <div className="container mx-auto px-4">
    //   <div className="flex divide-x divide-gray-300">

    //     {/* <div className="w-1/2">
    //       <h1 className="text-2xl font-bold">Your Courses</h1>
    //       <div className="courses-list space-y-4">
    //         {courses.map(course => (
    //           <div
    //             key={course.id}
    //             className="course-item cursor-pointer p-4 hover:bg-gray-100"
    //             onClick={() => handleCourseSelect(course.id)}
    //           >
    //             <h2 className="text-lg font-semibold">{course.name}</h2>

    //           </div>
    //         ))}
    //       </div>
    //     </div> */}
    //     {/* <div className="w-1/2 overflow-auto">
    //       {selectedCourse ? (
    //         tests[selectedCourse] && tests[selectedCourse].length > 0 ? (
    //           <div className="tests-list space-y-4 p-4">
    //             {tests[selectedCourse].map((test, index) => (
    //               <div key={index} className="test-item p-2 border-b border-gray-200">
    //                 {test.name} - {test.date}
    //               </div>
    //             ))}
    //           </div>
    //         ) : (
    //           <p className="p-4">No tests available for this course.</p>
    //         )
    //       ) : (
    //         <p className="p-4">Select a course to view tests.</p>
    //       )}
    //     </div> */}
    //   </div>
    //   < LogoutButton />
    // </div>

    <div className=" min-h-screen mx-auto w-full bg-cyan-50">
      <div className='sm:px-28 sm:py-8 px-4 py-4'>
        <div className='grid grid-cols-1 gap-x-8 mb-7 p-4 rounded-lg shadow bg-white'>
          <h1 className='text-3xl text-cyan-800 mb-4 font-bold'>
            Upcoming Tests
          </h1>
          <ul>
            {upcomingTests.map((test, index) => (
              <li key={index} className='text-lg text-gray-700 flex justify-between'>
                <span>{test.name}</span>
                {handleDateFormatting(test.start_t, test.end_t) === "LIVE" ? (
                  <a 
                    onClick={() => handleNavigate("/submission", { test })} 
                    className="text-md cursor-pointer text-cyan-500 hover:text-cyan-700">
                    LIVE
                  </a>
                ) : (
                  <span>{handleDateFormatting(test.start_t, test.end_t)}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <button 
          className='bg-cyan-950 text-white text-lg rounded-md mb-4 px-4 py-2 hover:ring-1 hover: ring-bg-grey-500 hover:bg-grey-900'
          onClick={() => handleNavigate("/create-course")}
          >
            Create a Course!
          </button>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-8 ">
          {courses.map((course, index) => (
            <React.Fragment key={course.id}>
              <div className="mb-8 p-4 bg-white span rounded-lg shadow">
                <div className={`Course-${index} flex justify-between mb-4`}>
                  <span className="text-xl font-semibold">{course.name}</span>
                  <button
                    className='bg-cyan-500 rounded-lg py-1 px-2 text-white hover:bg-cyan-400 hover:ring-2 hover:ring-cyan-300 hover:border-cyan-300'
                    onClick={() => handleNavigate("/create-test", { courseId: course.id })}
                  >Create Test +</button>
                </div>
                <div className="Tests">
                  {course.tests.length > 0 ? (
                    course.tests.map((test, testIndex) => (
                      <div key={testIndex} className={`Test-${testIndex} flex justify-between`}>
                        <span className="text-md font-light">{test.name}</span>
                        <span className="text-md">{handleDateFormatting(test.start_t)}</span>
                        {/* <span className="text-md">{test.date}</span> */}
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
      <div className="text-center">
        <LogoutButton />
      </div>
    </div>

  );
};
