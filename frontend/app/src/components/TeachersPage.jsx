import React, { useEffect, useState } from 'react';
import { EasyRequest, defHeaders, instanceURL } from "../api/helpers.js";
import { NavBar } from './coursePage/navBar.jsx';
import { BackButton } from './BackButton.jsx';

export const TeachersPage = () => {
  const [teachers, setTeachers] = useState([]);
  const [teacherCourses, setTeacherCourses] = useState({});

  useEffect(() => {
    const fetchTeachers = async () => {
      try {
        let req = await EasyRequest(`${instanceURL}/users/teachers/`, defHeaders, "GET");
        if (req.status === 200) {
          setTeachers(req.data);
        }
      } catch (error) {
        console.error('Error fetching teachers', error);
      }
    };

    fetchTeachers();
  }, []);

  useEffect(() => {
    const fetchCoursesForAllTeachers = async () => {
      try {
        const coursesPromises = teachers.map(async (teacher) => {
          let req = await EasyRequest(`${instanceURL}/course/teacher/${teacher.id}`, defHeaders, "GET");
          if (req.status === 200) {
            return { teacherId: teacher.id, courses: req.data };
          } else {
            return { teacherId: teacher.id, courses: [] };
          }
        });

        const coursesResults = await Promise.all(coursesPromises);
        const coursesMap = coursesResults.reduce((acc, { teacherId, courses }) => {
          acc[teacherId] = courses;
          return acc;
        }, {});

        setTeacherCourses(coursesMap);
      } catch (error) {
        console.error('Error fetching courses for teachers', error);
      }
    };

    if (teachers.length > 0) {
      fetchCoursesForAllTeachers();
    }
  }, [teachers]);

  return (
    <div className="min-h-screen mx-auto w-full bg-cyan-50">
      <NavBar />
      <div className="relative">
        
      </div>
      <div className='sm:px-28 sm:py-8 px-4 py-4'>
        <div className='grid grid-cols-1 gap-x-8 mb-7 p-4 rounded-lg shadow bg-white'>
          <h1 className='text-3xl text-cyan-800 mb-4 font-bold'>
            Teachers
          </h1>
          <ul role="list" className="divide-y divide-gray-100">
            {teachers.map((teacher) => (
              <li key={teacher.email} className="flex flex-col gap-x-6 py-5">
                <div className="flex min-w-0 gap-x-4">
                  <div className="min-w-0 flex-auto">
                    <p className="text-sm font-semibold leading-6 text-gray-900">{teacher.name}</p>
                    <p className="mt-1 truncate text-xs leading-5 text-gray-500">{teacher.email}</p>
                    {teacherCourses[teacher.id] && teacherCourses[teacher.id].map((course) => (
                      <p key={course.id} className="text-sm text-gray-700">{course.name}</p>
                    ))}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
