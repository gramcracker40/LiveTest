// src/components/SubmissionPage.jsx
import React, { useEffect, useContext, useState, useRef } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { EasyRequest, defHeaders } from '../api/helpers';
import { AuthContext } from '../context/auth';
import { BackButton } from './BackButton';
import badAnswersImage from '../assets/bad_answers.png';
import goodAnswersImage from '../assets/good_answers.png';
import pako from 'pako';
import { TakeScantronPicture } from './TakeScantronPicture';
import LiveVideoGrader from './LiveVideoGrader';

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

  // Choice-first UX
  // selectedMode: null | 'camera' | 'video'
  const mediaSupported = !!(navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === "function");
  const [selectedMode, setSelectedMode] = useState(null);

  // Video mode & confirmation flow state
  const [awaitingConfirm, setAwaitingConfirm] = useState(false);
  const [lastSubmissionId, setLastSubmissionId] = useState(null);
  const [videoKey, setVideoKey] = useState(0); // force-remount LiveVideoGrader to restart camera

  const gradedURLRef = useRef(null);
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

  const openCameraPicker = () => {
    // iPhone hint: capture="environment" opens rear camera in Safari
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.capture = 'environment';
    input.onchange = (e) => {
      const file = e.target.files?.[0];
      if (file) handleImageSubmit(file);
    };
    input.click();
  };

  const submitTest = async (file) => {
    const formData = new FormData();
    formData.append('submission_image', file);
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
        setLastSubmissionId(submissionId);
        setAwaitingConfirm(true); // stay until user confirms, like video flow
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
      if (gradedURLRef.current) URL.revokeObjectURL(gradedURLRef.current);
      gradedURLRef.current = imageObjectURL;
      setGradedImage(imageObjectURL);
    } catch (error) {
      console.error("Error fetching graded image: ", error);
      setErrorMessage(`Error fetching graded image: ${error.message}`);
    }
  };

  // Called by LiveVideoGrader when a submission was graded successfully
  const handleVideoGraded = async (submissionId) => {
    setLastSubmissionId(submissionId);
    await fetchGradedImage(submissionId);
    setAwaitingConfirm(true);
  };

  const confirmAndContinue = (confirmed) => {
    setAwaitingConfirm(false);
    // Optionally handle "reject" (delete submission) here if you want
    handleNewSubmission();
    // If we’re in video mode, remount to resume camera
    if (selectedMode === 'video') {
      setVideoKey(k => k + 1);
    }
  };

  const handleNewSubmission = () => {
    setImage(null);
    if (gradedURLRef.current) {
      URL.revokeObjectURL(gradedURLRef.current);
      gradedURLRef.current = null;
    }
    setGradedImage(null);
    setLastSubmissionId(null);
  };

  // Cleanup object URL on unmount
  useEffect(() => {
    return () => {
      if (gradedURLRef.current) URL.revokeObjectURL(gradedURLRef.current);
    };
  }, []);

  // Handle LiveVideoGrader calling onNoSupport (e.g., iPhone embedded webview, non-HTTPS)
  const handleNoVideoSupport = () => {
    setSelectedMode('camera');
    setErrorMessage("Live video is not available; switched to Camera mode. You can still take a photo to grade.");
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

      {/* CHOICE-FIRST CARD — show only when no method chosen and not showing a graded result */}
      {!selectedMode && !gradedImage && (
        <div className="w-full max-w-3xl bg-white rounded-xl shadow p-6">
          <h2 className="text-xl font-semibold mb-3">How would you like to submit?</h2>
          <p className="text-sm text-gray-600 mb-4">
            On iPhone, “Open Camera” launches the rear camera. “Video Feed” requires Safari/WebKit and HTTPS.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <button
              onClick={() => {
                setSelectedMode('camera');
                // immediately open the picker for convenience
                openCameraPicker();
              }}
              className="w-full px-4 py-3 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
            >
              Open Camera (Photo/Upload)
            </button>
            <button
              onClick={() => {
                if (!mediaSupported) {
                  setErrorMessage("Live video not supported here. Try Safari on iPhone, or use the Camera option.");
                  setSelectedMode('camera');
                  // optionally auto-open camera
                  openCameraPicker();
                } else {
                  setSelectedMode('video');
                  // LiveVideoGrader will request permission after mount
                }
              }}
              className="w-full px-4 py-3 rounded-lg bg-green-600 text-white hover:bg-green-700"
            >
              Use Live Video Feed
            </button>
          </div>
        </div>
      )}

      {/* VIDEO MODE — only when selected and not currently showing graded output */}
      {selectedMode === 'video' && !gradedImage && (
        <div className="w-full max-w-4xl mt-4" key={videoKey}>
          <LiveVideoGrader
            instanceURL={instanceURL}
            test={test}
            authDetails={authDetails}
            selectedStudent={selectedStudent}
            onGraded={handleVideoGraded}
            onError={(msg) => setErrorMessage(msg)}
            onNoSupport={handleNoVideoSupport}
          />
          <div className="text-center mt-3">
            <button
              className="text-sm underline text-gray-700 hover:text-gray-900"
              onClick={() => setSelectedMode('camera')}
            >
              Change method: Use Camera instead
            </button>
          </div>
        </div>
      )}

      {/* CAMERA/UPLOAD MODE — either chosen explicitly, or fallback from video */}
      {selectedMode === 'camera' && !gradedImage && (
        <div className="w-full max-w-4xl mt-4">
          {/* If you prefer your existing component, keep it; otherwise just show a button that opens the picker */}
          <TakeScantronPicture onSubmit={handleImageSubmit} />
          <div className="text-center mt-3 flex items-center justify-center gap-3">
            <button
              onClick={openCameraPicker}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Open Camera/Upload
            </button>
            {mediaSupported && (
              <button
                className="text-sm underline text-gray-700 hover:text-gray-900"
                onClick={() => setSelectedMode('video')}
              >
                Change method: Use Video Feed instead
              </button>
            )}
          </div>
        </div>
      )}

      {isSubmitting && <p className="text-center text-blue-500 mt-4">Submitting...</p>}
      {errorMessage && <p className="text-center text-red-500 mt-2">{errorMessage}</p>}

      {/* GRADED RESULT + CONFIRMATION (both modes) */}
      {gradedImage && (
        <div className="text-center mt-8">
          <h2 className="text-2xl font-bold mb-4">Graded Image</h2>
          <img src={gradedImage} alt="Graded" className="max-w-lg rounded-lg shadow-xl mx-auto" />
          <div className="mt-4 flex gap-3 justify-center">
            <button
              onClick={() => confirmAndContinue(true)}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
            >
              Looks Good — Save & Continue
            </button>
            <button
              onClick={() => confirmAndContinue(false)}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
            >
              Retake
            </button>
          </div>
          {awaitingConfirm && (
            <p className="text-sm text-gray-600 mt-2">
              Confirm the graded result to {selectedMode === 'video' ? 'resume the video feed' : 'submit another photo'}.
            </p>
          )}
        </div>
      )}
    </div>
  );
};
