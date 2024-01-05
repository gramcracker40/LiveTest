// CoursePage.jsx
import React from 'react';

const CoursePage = ({ userRole }) => {
  // Placeholder data (replace with real data)
  const courses = [
    { id: 1, title: 'Introduction to Mathematics' },
    { id: 2, title: 'History of Science' },
    { id: 3, title: 'Programming 101' },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-4xl font-bold mb-6">My Courses</h1>
      
      {userRole === 'student' ? (
        <StudentCourses courses={courses} />
      ) : (
        <TeacherCourses courses={courses} />
      )}
    </div>
  );
};

// StudentCourses component
const StudentCourses = ({ courses }) => {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Enrolled Courses</h2>
      {courses.length > 0 ? (
        <ul className="list-disc list-inside">
          {courses.map((course) => (
            <li key={course.id} className="mb-2">{course.title}</li>
          ))}
        </ul>
      ) : (
        <p>No courses enrolled yet.</p>
      )}
    </div>
  );
};

// TeacherCourses component
const TeacherCourses = ({ courses }) => {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Teaching Courses</h2>
      {courses.length > 0 ? (
        <ul className="list-disc list-inside">
          {courses.map((course) => (
            <li key={course.id} className="mb-2">{course.title}</li>
          ))}
        </ul>
      ) : (
        <p>No courses being taught yet.</p>
      )}
    </div>
  );
};

export default CoursePage;
