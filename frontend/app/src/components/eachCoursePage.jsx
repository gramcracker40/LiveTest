import React, { useState, useEffect, useContext } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { BackButton } from "./BackButton";
import { AuthContext } from "../context/auth";
import { EasyRequest, defHeaders, instanceURL } from "../api/helpers";
import {
  Popover,
  PopoverButton,
  PopoverGroup,
  PopoverPanel,
  Transition,
} from "@headlessui/react";
import { ChevronDownIcon, Bars3Icon } from "@heroicons/react/24/outline";
import QRCode from "qrcode.react";
import pako from 'pako';

export const EachCoursePage = () => {
  const { id } = useParams();
  const [course, setCourse] = useState(null);
  const [teacherName, setTeacherName] = useState("");
  const { authDetails } = useContext(AuthContext);
  const navigate = useNavigate();
  const [editMode, setEditMode] = useState(false);
  const [updatedCourseName, setUpdatedCourseName] = useState("");
  const [updatedSubject, setUpdatedSubject] = useState("");
  const [showStudentSubmissions, setShowStudentSubmissions] = useState(false);
  const [studentSubmissions, setStudentSubmissions] = useState([]);
  const [isDeleteCourseConfirmOpen, setIsDeleteCourseConfirmOpen] = useState(false);
  const [isDeleteStudentConfirmOpen, setIsDeleteStudentConfirmOpen] = useState(false);
  const [showQRCode, setShowQRCode] = useState(false);
  const [studentToRemove, setStudentToRemove] = useState(null);
  const [submissionImages, setSubmissionImages] = useState([]);
  const [selectedStudentName, setSelectedStudentName] = useState("");

  useEffect(() => {
    if (!authDetails.isLoggedIn) {
      navigate("/");
      return;
    }

    const fetchCourse = async () => {
      try {
        const courseURL = `${instanceURL}/course/${id}`;
        let req = await EasyRequest(courseURL, defHeaders, "GET");

        if (req.status === 200) {
          setCourse(req.data);
          setUpdatedCourseName(req.data.name);
          setUpdatedSubject(req.data.subject);
          fetchTeacherName(req.data.teacher_id);
        }
      } catch (error) {
        console.error("Error fetching course", error);
      }
    };

    const fetchTeacherName = async (teacherId) => {
      try {
        const teacherURL = `${instanceURL}/users/teachers/${teacherId}`;
        let req = await EasyRequest(teacherURL, defHeaders, "GET");

        if (req.status === 200) {
          setTeacherName(req.data.name);
        }
      } catch (error) {
        console.error("Error fetching teacher name", error);
        setTeacherName("Unknown");
      }
    };

    fetchCourse();
  }, [authDetails, navigate, id]);

  const handleTestClick = (test) => {
    navigate(`/test/${test.id}`, { state: { test } });
  };

  const handleDateFormatting = (start, end) => {
    const testStart = new Date(start);
    const testEnd = new Date(end);
    const now = new Date();

    if (now >= testStart && now <= testEnd) {
      return "LIVE";
    } else if (testStart.toDateString() === now.toDateString()) {
      return `Today at ${testStart.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      })}`;
    } else {
      const day = String(testStart.getDate());
      const month = String(testStart.getMonth() + 1);
      const year = String(testStart.getFullYear()).slice(2);
      return `${month}-${day}-${year}`;
    }
  };

  const handleDeleteCourse = async () => {
    try {
      const deleteURL = `${instanceURL}/course/${id}`;
      let req = await EasyRequest(deleteURL, defHeaders, "DELETE");

      if (req.status === 200) {
        navigate("/courses");
      }
    } catch (error) {
      console.error("Error deleting course", error);
    }
  };

  const handleUpdateCourse = async () => {
    const updateData = {
      name: updatedCourseName,
      subject: updatedSubject,
    };

    try {
      const updateURL = `${instanceURL}/course/${course.id}`;
      let req = await EasyRequest(updateURL, defHeaders, "PATCH", updateData);

      if (req.status === 200) {
        setCourse({ ...course, name: updatedCourseName, subject: updatedSubject });
        setEditMode(false);
      }
    } catch (error) {
      console.error("Error updating course", error);
    }
  };

  const handleRemoveStudent = (studentId) => {
    setStudentToRemove(studentId);
    setIsDeleteStudentConfirmOpen(true);
  };

  const confirmRemoveStudent = async () => {
    try {
      const deleteURL = `${instanceURL}/enrollment/${id}/student/${studentToRemove}`;
      let req = await EasyRequest(deleteURL, defHeaders, "DELETE");

      if (req.status === 200) {
        setCourse((prevCourse) => ({
          ...prevCourse,
          students: prevCourse.students.filter((student) => student.id !== studentToRemove),
        }));
        setIsDeleteStudentConfirmOpen(false);
      }
    } catch (error) {
      console.error("Error removing student", error);
    }
  };

  const handleShowSubmissions = async (studentId, studentName) => {
    try {
      const submissionsURL = `${instanceURL}/submission/student/${studentId}`;
      let req = await EasyRequest(submissionsURL, defHeaders, "GET");
      setSelectedStudentName(studentName);
  
      if (req.status === 200) {
        const submissions = req.data;
        setStudentSubmissions(submissions);
        setShowStudentSubmissions(true);
  
        const images = await Promise.all(
          submissions.map(async (submission) => {
            const gradedImageURL = `${instanceURL}/submission/image/graded/${submission.id}`;
            const originalImageURL = `${instanceURL}/submission/image/original/${submission.id}`;
            const [gradedImageRes, originalImageRes] = await Promise.all([
              fetch(gradedImageURL),
              fetch(originalImageURL),
            ]);
  
            if (!gradedImageRes.ok || !originalImageRes.ok) {
              throw new Error('Failed to fetch images');
            }
  
            const [gradedImageArrayBuffer, originalImageArrayBuffer] = await Promise.all([
              gradedImageRes.arrayBuffer(),
              originalImageRes.arrayBuffer(),
            ]);
  
            const gradedImageData = pako.inflate(new Uint8Array(gradedImageArrayBuffer));
            const originalImageData = pako.inflate(new Uint8Array(originalImageArrayBuffer));
  
            const gradedImageBlob = new Blob([gradedImageData], { type: 'image/jpeg' });
            const originalImageBlob = new Blob([originalImageData], { type: 'image/jpeg' });
  
            return {
              id: submission.id,
              gradedImage: URL.createObjectURL(gradedImageBlob),
              originalImage: URL.createObjectURL(originalImageBlob),
              grade: submission.grade,
              testName: submission.test_name,
            };
          })
        );
  
        setSubmissionImages(images);
      } else {
        console.error(`Failed to fetch submissions: ${req.statusText}`);
      }
    } catch (error) {
      console.error("Error fetching student submissions", error);
    }
  };

  const handleAddTest = () => {
    navigate("/create-test", { state: { courseId: course.id } });
  };

  const generateQRCodeURL = () => {
    const { protocol, hostname, port } = window.location;
    const instanceURL = `${protocol}//${hostname}${port ? `:${port}` : ''}`;
    return `${instanceURL}/login?courseId=${id}`;
  };

  return (
    <div className="min-h-screen mx-auto w-full bg-cyan-50">
      <header className="bg-white">
        <nav className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
          <div className="flex items-center gap-x-12">
            <BackButton className="px-8 py-3 text-sm font-semibold rounded-md shadow-sm bg-cyan-200 text-gray-700 hover:bg-cyan-300" />
          </div>
          <div className="flex lg:hidden">
            <Popover className="relative">
              <PopoverButton className="inline-flex items-center justify-center p-2 text-gray-700">
                <Bars3Icon className="h-6 w-6" aria-hidden="true" />
              </PopoverButton>
              <Transition
                enter="transition ease-out duration-200"
                enterFrom="opacity-0 translate-y-1"
                enterTo="opacity-100 translate-y-0"
                leave="transition ease-in duration-150"
                leaveFrom="opacity-100 translate-y-0"
                leaveTo="opacity-0 translate-y-1"
              >
                <PopoverPanel className="absolute right-0 z-10 mt-3 w-48 max-w-md overflow-hidden rounded-3xl bg-white shadow-lg ring-1 ring-gray-900/5">
                  <div className="p-4">
                    <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                      <button
                        onClick={() => setEditMode(true)}
                        className="w-full text-left"
                      >
                        Edit Course
                      </button>
                    </div>
                    <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                      <button
                        onClick={() => setIsDeleteCourseConfirmOpen(true)}
                        className="w-full text-left"
                      >
                        Delete Course
                      </button>
                    </div>
                  </div>
                </PopoverPanel>
              </Transition>
            </Popover>
          </div>
          <PopoverGroup className="hidden lg:flex lg:gap-x-12">
            <Popover className="relative">
              <PopoverButton className="flex items-center gap-x-1 text-sm font-semibold leading-6 text-gray-900">
                Course Options
                <ChevronDownIcon className="h-5 w-5 flex-none text-gray-400" aria-hidden="true" />
              </PopoverButton>

              <Transition
                enter="transition ease-out duration-200"
                enterFrom="opacity-0 translate-y-1"
                enterTo="opacity-100 translate-y-0"
                leave="transition ease-in duration-150"
                leaveFrom="opacity-100 translate-y-0"
                leaveTo="opacity-0 translate-y-1"
              >
                <PopoverPanel className="absolute z-10 mt-3 w-48 max-w-md overflow-hidden rounded-3xl bg-white shadow-lg ring-1 ring-gray-900/5">
                  <div className="p-4">
                    <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                      <button
                        onClick={() => setEditMode(true)}
                        className="w-full text-left"
                      >
                        Edit Course
                      </button>
                    </div>
                    <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                      <button
                        onClick={() => setIsDeleteCourseConfirmOpen(true)}
                        className="w-full text-left"
                      >
                        Delete Course
                      </button>
                    </div>
                  </div>
                </PopoverPanel>
              </Transition>
            </Popover>
          </PopoverGroup>
        </nav>
      </header>
      <div className="sm:px-28 sm:py-8 px-4 py-4">
        {course ? (
          <>
            <h1 className="text-3xl text-center text-cyan-800 mb-4 font-bold">{course.name}</h1>
            <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
              <div className="grid grid-cols-2 gap-x-4">
                <p className="text-lg font-medium text-gray-900">Instructor:</p>
                <p className="text-lg text-gray-700 text-right">{teacherName}</p>
              </div>
              <div className="grid grid-cols-2 gap-x-4">
                <p className="text-md text-gray-700">Course Number:</p>
                <p className="text-md text-gray-700 text-right">{course.course_number}</p>
              </div>
              <div className="grid grid-cols-2 gap-x-4">
                <p className="text-md text-gray-700">Subject:</p>
                <p className="text-md text-gray-700 text-right">{course.subject}</p>
              </div>
              <div className="grid grid-cols-2 gap-x-4">
                <p className="text-md text-gray-700">Semester:</p>
                <p className="text-md text-gray-700 text-right">{course.semester_season} {course.year}</p>
              </div>
              <div className="grid grid-cols-2 gap-x-4">
                <p className="text-md text-gray-700">Section:</p>
                <p className="text-md text-gray-700 text-right">{course.section}</p>
              </div>
              <div className="grid grid-cols-2 gap-x-4">
                <p className="text-md text-gray-700">Course ID:</p>
                <p className="text-md text-gray-700 text-right">{course.id}</p>
              </div>
            </div>

            {editMode && (
              <div className="mb-6">
                <input
                  type="text"
                  className="border rounded px-3 py-2 w-full mb-2"
                  value={updatedCourseName}
                  onChange={(e) => setUpdatedCourseName(e.target.value)}
                  placeholder="Course Name"
                />
                <input
                  type="text"
                  className="border rounded px-3 py-2 w-full mb-2"
                  value={updatedSubject}
                  onChange={(e) => setUpdatedSubject(e.target.value)}
                  placeholder="Subject"
                />
                <button
                  className="px-4 py-2 bg-cyan-500 text-white rounded"
                  onClick={handleUpdateCourse}
                >
                  Save Changes
                </button>
              </div>
            )}

            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl text-cyan-700 font-semibold">Tests</h2>
              <h2 className="text-2xl text-cyan-700 font-semibold">{course.tests.length}</h2>
            </div>
            {course.tests.length > 0 ? (
              <div>
                <ul className="space-y-4">
                  {course.tests.map((test) => (
                    <li
                      key={test.id}
                      onClick={() => handleTestClick(test)}
                      className="p-4 rounded shadow bg-white flex justify-between items-center cursor-pointer hover:bg-gray-100"
                    >
                      <div>
                        <p className="font-medium text-gray-900">{test.name}</p>
                        <p className="text-gray-500">{handleDateFormatting(test.start_t, test.end_t)}</p>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
              <p className="text-gray-500">No tests available</p>
            )}
            <div className="mt-4">
              <button
                className="px-4 py-2 bg-cyan-500 text-white rounded"
                onClick={handleAddTest}
              >
                Create Test
              </button>
            </div>

            <div className="flex justify-between items-center mt-8 mb-4">
              <h2 className="text-2xl text-cyan-700 font-semibold">Students</h2>
              <button
                className="px-4 py-2 bg-cyan-500 text-white rounded"
                onClick={() => setShowQRCode(!showQRCode)}
              >
                Add Students
              </button>
              <h2 className="text-2xl text-cyan-700 font-semibold">{course.students.length}</h2>
            </div>
            {showQRCode && (
              <div className="fixed z-10 inset-0 overflow-y-auto">
                <div className="flex items-center justify-center min-h-screen">
                  <div className="fixed inset-0 bg-black opacity-30" aria-hidden="true"></div>
                  <div className="relative bg-white rounded-lg max-w-2xl mx-auto p-8">
                    <h1 className="text-4xl text-cyan-700 font-semibold pb-12 text-center">Scan to join {course.name}</h1>
                    <QRCode value={generateQRCodeURL()} size={350} />
                    <button
                      className="mt-12 px-8 py-6 text-2xl bg-gray-400 text-white rounded-md"
                      onClick={() => setShowQRCode(false)}
                    >
                      Close
                    </button>
                  </div>
                </div>
              </div>
            )}
            {course.students.length > 0 ? (
              <div>
                <ul className="space-y-4">
                  {course.students.map((student) => (
                    <li
                      key={student.id}
                      className="p-4 rounded shadow bg-white flex justify-between items-center"
                    >
                      <div>
                        <p className="font-medium text-gray-900">{student.name}</p>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          className="px-4 py-2 bg-orange-500 text-white rounded"
                          onClick={() => handleRemoveStudent(student.id)}
                        >
                          Remove
                        </button>
                        <button
                          className="px-4 py-2 bg-cyan-500 text-white rounded"
                          onClick={() => handleShowSubmissions(student.id, student.name)}
                        >
                          Show Submissions
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
              <p className="text-gray-500">No students enrolled</p>
            )}

            {showStudentSubmissions && (
              <div className="fixed z-10 inset-0 overflow-y-auto">
                <div className="flex items-center justify-center min-h-screen">
                  <div className="fixed inset-0 bg-black opacity-30" aria-hidden="true"></div>
                  <div className="relative bg-white rounded-lg max-w-2xl mx-auto p-6">
                    <h2 className="text-2xl font-semibold mb-4">{selectedStudentName}'s Submissions</h2>
                    <ul className="space-y-4">
                      {submissionImages.map((submission) => (
                        <li key={submission.id} className="p-4 rounded shadow bg-white">
                          <h3 className="font-medium text-gray-900">Test Name: {submission.testName}</h3>
                          <p className="text-gray-500">Grade: {submission.grade}</p>
                          <div className="flex space-x-4">
                            <div>
                              <h4 className="font-medium text-gray-700">Graded Image</h4>
                              <img src={submission.gradedImage} alt={`Graded Submission ${submission.id}`} />
                            </div>
                            <div>
                              <h4 className="font-medium text-gray-700">Original Image</h4>
                              <img src={submission.originalImage} alt={`Original Submission ${submission.id}`} />
                            </div>
                          </div>
                        </li>
                      ))}
                    </ul>
                    <button
                      className="mt-4 px-4 py-2 bg-gray-400 text-white rounded-md"
                      onClick={() => setShowStudentSubmissions(false)}
                    >
                      Close
                    </button>
                  </div>
                </div>
              </div>
            )}
          </>
        ) : (
          <p className="text-gray-500">Loading course...</p>
        )}
      </div>

      {isDeleteCourseConfirmOpen && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen">
            <div className="fixed inset-0 bg-black opacity-30" aria-hidden="true"></div>
            <div className="relative bg-white rounded-lg max-w-sm mx-auto p-6">
              <h2 className="text-lg font-semibold">Delete Course</h2>
              <p className="mt-2 text-sm text-gray-600">
                Are you sure you want to remove this course? This will delete all tests, enrollments, and submissions associated with the course.
              </p>
              <div className="mt-4 flex justify-end space-x-4">
                <button
                  onClick={() => setIsDeleteCourseConfirmOpen(false)}
                  className="px-4 py-2 bg-gray-400 text-white rounded-md"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDeleteCourse}
                  className="px-4 py-2 bg-red-600 text-white rounded-md"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {isDeleteStudentConfirmOpen && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen">
            <div className="fixed inset-0 bg-black opacity-30" aria-hidden="true"></div>
            <div className="relative bg-white rounded-lg max-w-sm mx-auto p-6">
              <h2 className="text-lg font-semibold">Remove Student</h2>
              <p className="mt-2 text-sm text-gray-600">
                Are you sure you want to remove this student? This action cannot be undone and will remove all submissions for this student.
              </p>
              <div className="mt-4 flex justify-end space-x-4">
                <button
                  onClick={() => setIsDeleteStudentConfirmOpen(false)}
                  className="px-4 py-2 bg-gray-400 text-white rounded-md"
                >
                  Cancel
                </button>
                <button
                  onClick={confirmRemoveStudent}
                  className="px-4 py-2 bg-red-600 text-white rounded-md"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
