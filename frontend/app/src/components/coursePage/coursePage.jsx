import React, { useEffect, useState, useContext } from 'react';
import { EasyRequest, defHeaders, instanceURL } from "../../api/helpers.js";
import { AuthContext } from '../../context/auth.jsx';

const CoursePage = () => {
  const [courses, setCourses] = useState([]);
  const { authDetails, setAuthDetails } = useContext(AuthContext);

  useEffect(() => {
    console.log(`Auth details --> ${authDetails}`)
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
        }
        // Handle other status codes appropriately
      } catch (error) {
        console.error('Error fetching courses', error);
      }
    };
    fetchCourses();
  }, [authDetails]);

  console.log(`Courses::: ${courses}`);
  return (
    <div className="course-page-container">
      <h1 className="text-2xl font-bold">Your Courses</h1>
      <div className="courses-list">
        {courses && courses.map(course => (
          <div key={course.id} className="course-item">
            <h2>{course.name}</h2>
            {/* Additional course details */}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CoursePage;