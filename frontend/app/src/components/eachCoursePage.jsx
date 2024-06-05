import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Disclosure } from '@headlessui/react';
import { Bars3Icon, BellIcon, XMarkIcon } from '@heroicons/react/24/outline';

const EachCoursePage = () => {
  const { course_id } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [students, setStudents] = useState([]);
  const [tests, setTests] = useState([]);

  useEffect(() => {
    // Fetch course data
    fetch(`/api/courses/${course_id}`)
      .then(response => response.json())
      .then(data => {
        setCourse(data);
        setStudents(data.students);
        setTests(data.tests);
      });
  }, [course_id]);

  const addStudent = (studentId) => {
    fetch(`/enrollment/${course_id}/student/${studentId}`, { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        setStudents(prev => [...prev, data]);
      });
  };

  const removeStudent = (studentId) => {
    fetch(`/enrollment/${course_id}/student/${studentId}`, { method: 'DELETE' })
      .then(() => {
        setStudents(prev => prev.filter(student => student.id !== studentId));
      });
  };

  const handleTestClick = (testId) => {
    navigate(`/analytics/${testId}`);
  };

  return (
    <div className="border-b border-gray-200 bg-white px-4 py-5 sm:px-6">
      <div className="-ml-4 -mt-2 flex flex-wrap items-center justify-between sm:flex-nowrap">
        <div className="ml-4 mt-2">
          <h3 className="text-base font-semibold leading-6 text-gray-900">{course?.name}</h3>
        </div>
        <div className="ml-4 mt-2 flex-shrink-0">
          <button
            type="button"
            className="relative inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            onClick={() => addStudent(prompt('Enter student ID'))}
          >
            Add Student
          </button>
        </div>
      </div>
      <div className="mt-6">
        <h4 className="text-lg font-semibold leading-6 text-gray-900">Students</h4>
        <ul role="list" className="divide-y divide-gray-100">
          {students.map((student) => (
            <li key={student.id} className="flex justify-between gap-x-6 py-5">
              <div className="flex min-w-0 gap-x-4">
                <img className="h-12 w-12 flex-none rounded-full bg-gray-50" src={`https://api.adorable.io/avatars/285/${student.id}.png`} alt="" />
                <div className="min-w-0 flex-auto">
                  <p className="text-sm font-semibold leading-6 text-gray-900">{student.name}</p>
                </div>
              </div>
              <div className="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
                <button
                  type="button"
                  className="text-sm font-semibold text-red-600 hover:text-red-500"
                  onClick={() => removeStudent(student.id)}
                >
                  Remove
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>
      <div className="mt-6">
        <h4 className="text-lg font-semibold leading-6 text-gray-900">Tests</h4>
        <ul role="list" className="divide-y divide-gray-100">
          {tests.map((test) => (
            <li key={test.id} className="cursor-pointer p-4 border border-gray-200 rounded-lg" onClick={() => handleTestClick(test.id)}>
              <h5 className="text-xl font-semibold">{test.name}</h5>
              <p className="text-gray-600">Start: {new Date(test.start_t).toLocaleString()}</p>
              <p className="text-gray-600">End: {new Date(test.end_t).toLocaleString()}</p>
              <p className="text-gray-600">Questions: {test.num_questions}</p>
              <p className="text-gray-600">Choices: {test.num_choices}</p>
              <p className="text-gray-600">Course ID: {test.course_id}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default EachCoursePage;
