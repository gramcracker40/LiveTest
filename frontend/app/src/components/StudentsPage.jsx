import React, { useEffect, useState } from 'react';
import { EasyRequest, defHeaders, instanceURL } from "../api/helpers.js";
import { NavBar } from './coursePage/navBar.jsx';
import { BackButton } from './BackButton.jsx';

export const StudentsPage = () => {
  const [students, setStudents] = useState([]);
  const [filteredStudents, setFilteredStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [studentCourses, setStudentCourses] = useState({});
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        let req = await EasyRequest(`${instanceURL}/users/students/`, defHeaders, "GET");
        if (req.status === 200) {
          setStudents(req.data);
          setFilteredStudents(req.data);
        }
      } catch (error) {
        console.error('Error fetching students', error);
      }
    };

    const fetchCourses = async () => {
      try {
        let req = await EasyRequest(`${instanceURL}/course/`, defHeaders, "GET");
        if (req.status === 200) {
          setCourses(req.data);
        }
      } catch (error) {
        console.error('Error fetching courses', error);
      }
    };

    fetchStudents();
    fetchCourses();
  }, []);

  useEffect(() => {
    const filtered = students.filter(student =>
      student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.email.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredStudents(filtered);
  }, [searchTerm, students]);

  const fetchStudentCourses = async (studentId) => {
    try {
      let req = await EasyRequest(`${instanceURL}/course/student/${studentId}`, defHeaders, "GET");
      if (req.status === 200) {
        setStudentCourses((prev) => ({
          ...prev,
          [studentId]: req.data,
        }));
      }
    } catch (error) {
      console.error('Error fetching student courses', error);
    }
  };

  const handleAddStudentToCourse = async (courseId, studentId) => {
    try {
      let req = await EasyRequest(`${instanceURL}/enrollment/${courseId}/student/${studentId}`, defHeaders, "POST");
      if (req.status === 200) {
        alert('Student added to course successfully');
        fetchStudentCourses(studentId);
      } else {
        alert('Student is already in this course.');
      }
    } catch (error) {
      console.error('Error adding student to course ', error);
      alert('Error adding student to course');
    }
  };

  const handleRemoveStudentFromCourse = async (courseId, studentId) => {
    try {
      let req = await EasyRequest(`${instanceURL}/enrollment/${courseId}/student/${studentId}`, defHeaders, "DELETE");
      if (req.status === 200) {
        alert('Student removed from course successfully');
        fetchStudentCourses(studentId);
      } else {
        alert('Failed to remove student from course');
      }
    } catch (error) {
      console.error('Error removing student from course', error);
      alert('Error removing student from course');
    }
  };

  return (
    <div className="min-h-screen mx-auto w-full bg-cyan-50">
      <NavBar />
      <div className="relative">
        
      </div>
      <div className='sm:px-28 sm:py-8 px-4 py-4'>
        <div className='grid grid-cols-1 gap-x-8 mb-7 p-4 rounded-lg shadow bg-white'>
          <h1 className='text-3xl text-cyan-800 mb-4 font-bold'>
            Students
          </h1>
          <input
            type="text"
            placeholder="Search students..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="mb-4 block w-full rounded-md border-gray-300 shadow-sm focus:border-cyan-500 focus:ring focus:ring-cyan-500 focus:ring-opacity-50"
          />
          <ul role="list" className="divide-y divide-gray-100">
            {filteredStudents.map((student) => (
              <li key={student.email} className="flex flex-col gap-x-6 py-5">
                <div className="flex min-w-0 gap-x-4">
                  <div className="min-w-0 flex-auto">
                    <p className="text-sm font-semibold leading-6 text-gray-900">{student.name}</p>
                    <p className="mt-1 truncate text-xs leading-5 text-gray-500">{student.email}</p>
                  </div>
                </div>
                <div className="flex gap-x-4 mt-4">
                  <button
                    className="text-sm text-cyan-600 hover:text-cyan-800"
                    onClick={() => {
                      setSelectedStudent(student.id);
                      fetchStudentCourses(student.id);
                    }}
                  >
                    Manage Courses
                  </button>
                  {selectedStudent === student.id && (
                    <div className="flex flex-col mt-4">
                      <label className="block text-sm font-medium text-gray-700">Add to Course</label>
                      <select
                        onChange={(e) => handleAddStudentToCourse(e.target.value, student.id)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-cyan-500 focus:ring focus:ring-cyan-500 focus:ring-opacity-50"
                      >
                        <option value="">Select a course</option>
                        {courses.map((course) => (
                          <option key={course.id} value={course.id}>
                            {course.name}
                          </option>
                        ))}
                      </select>
                      <label className="block text-sm font-medium text-gray-700 mt-4">Remove from Course</label>
                      <select
                        onChange={(e) => handleRemoveStudentFromCourse(e.target.value, student.id)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-cyan-500 focus:ring focus:ring-cyan-500 focus:ring-opacity-50"
                      >
                        <option value="">Select a course</option>
                        {studentCourses[student.id] && studentCourses[student.id].map((course) => (
                          <option key={course.id} value={course.id}>
                            {course.name}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
