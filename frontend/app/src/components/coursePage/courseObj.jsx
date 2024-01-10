// CourseObj.jsx
import React from "react";
import "../../index.css";

function CourseObj({ name, instructor, students, duration }) {
  return (
    <div className="divide-y border-solid border-2 border-gray-300 divide-gray-300 overflow-hidden rounded-lg shadow">
      <div className="px-4 py-5 sm:px-6">
        <h2>{name}</h2>
        <p>Instructor: {instructor}</p>
      </div>
      <div className="px-4 py-5 sm:p-6">
        <p>Students: {students}</p>
        <p>Duration: {duration} weeks</p>
      </div>
    </div>
  );
}

export default CourseObj;
