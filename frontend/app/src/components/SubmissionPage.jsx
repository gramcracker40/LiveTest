// src/components/SubmissionPage.jsx
import React, { useEffect, useContext, useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { EasyRequest, defHeaders } from '../api/helpers';
import { AuthContext } from '../context/auth';
import { BackButton } from './BackButton';
import badAnswersImage from '../assets/bad_answers.png';
import goodAnswersImage from '../assets/good_answers.png';
import pako from 'pako';
import { TakeScantronPicture } from './TakeScantronPicture';

export const SubmissionPage = () => {
  const { testid } = useParams(); // kept for route parity; we use location.state.test
  const { authDetails } = useContext(AuthContext);
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [gradedImage, setGradedImage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const location = useLocation();
  const test = location.state?.test;
  const navigate = useNavigate();
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
    setImage(file);
    await submitTest(file);
  };

  const submitTest = async (file) => {
    const formData = new FormData();
    formData.append('submission_image', file);
    // student_id is OPTIONAL; only append if teacher provided one or if user is a student
    if (authDetails.type === 'teacher' && selectedStudent) {
      formData.append('student_id', selectedStudent);
    } else if (authDetails.type === 'student' && authDetails.id) {
      formData.append('student_id', String(authDetails.id));
    }
    formData.append('test_id', test.id);

    setIsSubmitting(true);
    setErrorMessage(null);

    const URL = `${instanceURL}/submission/`;
    try {
      const response = await fetch(URL, { method: 'POST', body: formData });
      const req = await response.json();

      setIsSubmitting(false);
      if (response.status === 200) {
        const submissionId = req.submission_id;
        await fetchGradedImage(submissionId);

        // Auto-reset after 3s to allow “next one”
        setTimeout(() => {
          handleNewSubmission();
        }, 3000);
      } else {
        console.error("Error submitting scantron: ", response.status);
        setErrorMessage(`${req.detail}`);
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
      const response = await fetch(gradedImageURL, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authDetails.accessToken}`,
          ...defHeaders,
        },
      });

      if (!response.ok) {
        throw new Error(`Error fetching graded image: ${response.statusText}`);
      }

      const compressedArrayBuffer = await response.arrayBuffer();
      const decompressedData = pako.inflate(new Uint8Array(compressedArrayBuffer));
      const blob = new Blob([decompressedData], { type: 'image/jpeg' });
      const imageObjectURL = URL.createObjectURL(blob);
      setGradedImage(imageObjectURL);
    } catch (error) {
      console.error("Error fetching graded image: ", error);
      setErrorMessage(`Error fetching graded image: ${error.message}`);
    }
  };

  const handleNewSubmission = () => {
    setImage(null);
    setGradedImage(null);
    // keep selectedStudent as-is to streamline bulk grading; clear if you prefer:
    // setSelectedStudent('');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-cyan-100 p-4">
      <div className="absolute top-4 left-4">
        <BackButton className="px-8 py-3 text-sm font-semibold rounded-md shadow-sm bg-cyan-200 text-gray-700 hover:bg-cyan-300" />
      </div>

      <h1 className="text-3xl font-bold mb-4">Submit to Test: {test.name}</h1>

      <div className="flex flex-col items-center mb-6">
        <div className="flex mb-4">
          <div className="flex flex-col items-center mr-4">
            <img src={badAnswersImage} alt="Bad Answers" className="w-64 h-64 object-cover rounded-lg shadow-md" />
            <p className="text-red-500 font-bold mt-2">Bad Answers (Rejected)</p>
          </div>
          <div className="flex flex-col items-center">
            <img src={goodAnswersImage} alt="Good Answers" className="w-64 h-64 object-cover rounded-lg shadow-md" />
            <p className="text-green-500 font-bold mt-2">Good Answers (Accepted)</p>
          </div>
        </div>
      </div>

      {authDetails.type === 'teacher' && (
        <div className="mb-4 w-full max-w-md">
          <label htmlFor="student" className="block text-sm font-medium text-gray-700">Select Student (optional)</label>
          <select
            id="student"
            name="student"
            value={selectedStudent}
            onChange={(e) => setSelectedStudent(e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-cyan-500 focus:border-cyan-500 sm:text-md"
          >
            <option value="">(none)</option>
            {students.map((student) => (
              <option key={student.id} value={student.id}>{student.name}</option>
            ))}
          </select>
          <p className="text-gray-500 text-sm mt-1">
            If left blank, the submission will not be linked to a specific student.
          </p>
        </div>
      )}

      {/* Live capture with sheet detection */}
      {!image && !gradedImage && (
        <div className="w-full max-w-4xl">
          <TakeScantronPicture onSubmit={handleImageSubmit} />
        </div>
      )}

      {/* Fallback “Take Photo” button (optional; kept for devices where webcam lib isn’t available) */}
      {!image && !gradedImage && (
        <button
          onClick={async () => {
            // As a fallback, open the file picker:
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            input.onchange = (e) => {
              const file = e.target.files?.[0];
              if (file) handleImageSubmit(file);
            };
            input.click();
          }}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition duration-300"
        >
          Upload Photo Instead
        </button>
      )}

      {isSubmitting && <p className="text-center text-blue-500 mt-4">Submitting...</p>}
      {errorMessage && <p className="text-center text-red-500 mt-2">{errorMessage}</p>}

      {gradedImage && (
        <div className="text-center mt-8">
          <h2 className="text-2xl font-bold mb-4">Graded Image</h2>
          <img src={gradedImage} alt="Graded" className="max-w-lg rounded-lg shadow-xl mx-auto" />
          <div className="mt-4">
            <button onClick={handleNewSubmission} className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 transition">
              New Submission
            </button>
          </div>
          <p className="text-sm text-gray-600 mt-2">Auto-resetting for next submission…</p>
        </div>
      )}
    </div>
  );
};
