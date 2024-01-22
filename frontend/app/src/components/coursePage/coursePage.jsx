import React, { useEffect, useState, useContext } from 'react';
import { EasyRequest, defHeaders, instanceURL } from "../../api/helpers.js";
import { AuthContext } from '../../context/auth.jsx';
import { LogoutButton } from '../logoutButton.jsx';

export const CoursePage = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [tests, setTests] = useState({});
  const { authDetails, setAuthDetails } = useContext(AuthContext);

  useEffect(() => {
    // localStorage.setItem(
    //   "courses": JSON.stringify()
    // )
    console.log(`Auth details --> ${JSON.stringify(authDetails)}`)
    // Fetch courses if not in cache
    const courseURL = authDetails.type === 'teacher'
      ? instanceURL + `/course/teacher/${authDetails.id}`
      : instanceURL + `/course/student/${authDetails.id}`;
    console.log(`courseURL::: ${courseURL}`)
    const fetchCourses = async () => {
      try {
        let req = await EasyRequest(courseURL, defHeaders, "GET");
        console.log(`req.data --> ${JSON.stringify(req.data)}`)
        if (req.status === 200) {
          setCourses(req.data);
          fetchTests(); [1, 2, 3, 4, 5, "beery"]
        }
        // Handle other status codes appropriately
      } catch (error) {
        console.error('Error fetching courses', error);
      }
    };
    const fetchTests = async () => {
      console.log(`${JSON.stringify(courses)}`)
      // try {
      //   let req = await EasyRequest(testURL, defHeaders, "GET");
      //   console.log(`req.data --> ${JSON.stringify(req.data)}`)
      //   if (req.status === 200) {
      //     setCourses(req.data);
      //   }
      //   // Handle other status codes appropriately
      // } catch (error) {
      //   console.error('Error fetching courses', error);
      // }
    };
    fetchCourses();
    
  }, [authDetails]);

  const handleCourseSelect = (courseId) => {
    setSelectedCourse(courseId);
  };

  console.log(`Courses::: ${courses}`);
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
    <div className="container mx-auto px-4">
      <div className="flex divide-x divide-gray-300">
        <div className="w-1/2">
          <h1 className="text-2xl font-bold">Your Courses</h1>
          <div className="courses-list space-y-4">
            {courses.map(course => (
              <div
                key={course.id}
                className="course-item cursor-pointer p-4 hover:bg-gray-100"
                onClick={() => handleCourseSelect(course.id)}
              >
                <h2 className="text-lg font-semibold">{course.name}</h2>
                {/* Additional course details */}
              </div>
            ))}
          </div>
        </div>
        <div className="w-1/2 overflow-auto">
          {/* {selectedCourse ? (
            tests[selectedCourse] && tests[selectedCourse].length > 0 ? (
              <div className="tests-list space-y-4 p-4">
                {tests[selectedCourse].map((test, index) => (
                  <div key={index} className="test-item p-2 border-b border-gray-200">
                    {test.name} - {test.date}
                  </div>
                ))}
              </div>
            ) : (
              <p className="p-4">No tests available for this course.</p>
            )
          ) : (
            <p className="p-4">Select a course to view tests.</p>
          )} */}
        </div>
      </div>
      < LogoutButton />
    </div>
  );
};
