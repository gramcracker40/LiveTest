import React, { useEffect, useContext, useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { EasyRequest, defHeaders } from '../api/helpers';
import { AuthContext } from '../context/auth';
import { BackButton } from './BackButton';
import { usePhotoGallery } from '../hooks/usePhotoGallery';

export const SubmissionPage = () => {
  const { testid } = useParams();
  const { authDetails } = useContext(AuthContext);
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [gradedImage, setGradedImage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [studentError, setStudentError] = useState(false);
  const location = useLocation();
  const test = location.state?.test;
  const navigate = useNavigate();
  const { takePhoto } = usePhotoGallery();
  const [image, setImage] = useState(null);

  const instanceURL = `${window.location.protocol}//${window.location.hostname}:8000`;

  useEffect(() => {
    if (!authDetails.isLoggedIn) {
      navigate("/");
      return;
    }
    if (authDetails.type === 'teacher') {
      fetchStudents();
    }
  }, [authDetails, navigate]);

  const fetchStudents = async () => {
    try {
      const studentsURL = `${instanceURL}/test/students/${test.id}`;
      let req = await EasyRequest(studentsURL, defHeaders, "GET");
      if (req.status === 200) {
        setStudents(req.data);
      }
    } catch (error) {
      console.error("Error fetching students", error);
    }
  };

  const handleImageSubmit = async (file) => {
    console.log("Image to submit: ", file);
    setImage(file);
    await submitTest(file);
  };

  const submitTest = async (file) => {
    const formData = new FormData();
    formData.append('submission_image', file);
    formData.append('student_id', authDetails.type === 'teacher' ? selectedStudent : authDetails.id);
    formData.append('test_id', test.id);

    setIsSubmitting(true);
    setErrorMessage(null);

    const URL = `${instanceURL}/submission/`;
    try {
      let response = await fetch(URL, {
        method: 'POST',
        body: formData,
      });

      let req = await response.json();

      setIsSubmitting(false);
      if (response.status === 200) {
        const submissionId = req.submission_id;
        fetchGradedImage(submissionId);
      } else {
        console.error("Error submitting scantron: ", response.status);
        setErrorMessage(`Error: ${response.status}`);
        setImage(null);
      }
    } catch (error) {
      console.error("API error", error);
      setErrorMessage(`API error: ${error.message}`);
      setIsSubmitting(false);
    }
  };

  const fetchGradedImage = async (submissionId) => {
    const gradedImageURL = `${instanceURL}/submission/image/graded/${submissionId}`;
    try {
      let req = await EasyRequest(gradedImageURL, defHeaders, "GET");
      if (req.status === 200) {
        setGradedImage(req.data.image_url); // assuming the response contains the image URL
      } else {
        console.error("Error fetching graded image: ", req.status);
        setErrorMessage(`Error fetching graded image: ${req.status}`);
      }
    } catch (error) {
      console.error("API error", error);
      setErrorMessage(`API error: ${error.message}`);
    }
  };

  const handlePhotoSubmit = async () => {
    if (authDetails.type === 'teacher' && !selectedStudent) {
      setStudentError(true);
      return;
    }
    setStudentError(false);
    const photo = await takePhoto();
    if (photo) {
      const file = await fetch(photo.webPath)
        .then(res => res.blob())
        .then(blob => new File([blob], "submission.jpg", { type: "image/jpeg" }));
      handleImageSubmit(file);
    }
  };

  const handleNewSubmission = () => {
    setImage(null);
    setGradedImage(null);
    setSelectedStudent(null);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-cyan-100 p-4">
      <div className="absolute top-4 left-4">
        <BackButton className="px-8 py-3 text-sm font-semibold rounded-md shadow-sm bg-cyan-200 text-gray-700 hover:bg-cyan-300"></BackButton>
      </div>
      <h1 className="text-3xl font-bold mb-4">Submit to Test: {test.name}</h1>
      {authDetails.type === 'teacher' && (
        <div className="mb-4">
          <label htmlFor="student" className="block text-sm font-medium text-gray-700">Select Student</label>
          <select
            id="student"
            name="student"
            value={selectedStudent}
            onChange={(e) => setSelectedStudent(e.target.value)}
            className={`mt-1 block w-full border ${studentError ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:ring-cyan-500 focus:border-cyan-500 sm:text-md`}
          >
            <option value="">Select a student</option>
            {students.map((student) => (
              <option key={student.id} value={student.id}>{student.name}</option>
            ))}
          </select>
          {studentError && <p className="text-red-500 text-sm mt-1">Please select a student</p>}
        </div>
      )}
      {!image ? (
        <button onClick={handlePhotoSubmit} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition duration-300">
          Take Photo
        </button>
      ) : (
        <>
          <img src={URL.createObjectURL(image)} alt="Captured" className="max-w-lg rounded-lg shadow-xl" />
          <div className="flex space-x-4 my-4">
            <button onClick={() => setImage(null)} className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-700 transition duration-300">
              Retake Photo
            </button>
            <button onClick={handlePhotoSubmit} className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-700 transition duration-300">
              Submit
            </button>
          </div>
        </>
      )}
      {isSubmitting && <p className="text-center text-blue-500">Submitting...</p>}
      {errorMessage && <p className="text-center text-red-500">{errorMessage}</p>}
      {gradedImage && (
        <div className="text-center mt-8">
          <h2 className="text-2xl font-bold mb-4">Graded Image</h2>
          <img src={gradedImage} alt="Graded" className="max-w-lg rounded-lg shadow-xl" />
          <button onClick={handleNewSubmission} className="mt-4 px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-700 transition duration-300">
            New Submission
          </button>
        </div>
      )}
    </div>
  );
};
