// SubmissionPage.jsx
import React, { useEffect, useContext, useState, useRef } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { EasyRequest, instanceURL, defHeaders } from '../api/helpers';
import { AuthContext } from '../context/auth';
import Webcam from 'react-webcam';

export const SubmissionPage = () => {
  const { testid } = useParams();
  const { authDetails } = useContext(AuthContext);
  const [capturedImage, setCapturedImage] = useState(null);
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const location = useLocation();
  const test = location.state.test; // Change here to correctly access the test state
  const navigate = useNavigate();
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  const [image, setImage] = useState(null);

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
      const studentsURL = `${instanceURL}/course/${test.course_id}/students`;
      let req = await EasyRequest(studentsURL, defHeaders, "GET");
      if (req.status === 200) {
        setStudents(req.data);
      }
    } catch (error) {
      console.error("Error fetching students", error);
    }
  };

  const handleImageSubmit = (base64Image) => {
    setCapturedImage(base64Image);
    submitTest(base64Image);
  };

  const submitTest = async (image) => {
    const body = {
      "submission_photo": image,
      "student_id": authDetails.type === 'teacher' ? selectedStudent : authDetails.id,
      "test_id": test.id
    };

    setIsSubmitting(true);

    const URL = instanceURL + "/submission/";
    try {
      let req = await EasyRequest(URL, defHeaders, "POST", body);
      setIsSubmitting(false);
      if (req.status === 200) {
        navigate("/course");
      } else {
        console.error("Error submitting scantron: ", req.status);
        setCapturedImage(null);
      }
    } catch (error) {
      console.error("API error", error);
      setIsSubmitting(false);
    }
  };

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);
  };

  const drawAlignmentBox = () => {
    if (webcamRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      const videoWidth = webcamRef.current.video.videoWidth;
      const videoHeight = webcamRef.current.video.videoHeight;

      canvasRef.current.width = videoWidth;
      canvasRef.current.height = videoHeight;

      const aspectRatio = 4.25 / 11;
      let boxHeight = videoHeight * 0.9;
      let boxWidth = boxHeight * aspectRatio;

      if (boxWidth > videoWidth) {
        boxWidth = videoWidth * 0.9;
        boxHeight = boxWidth / aspectRatio;
      }

      const x = (videoWidth - boxWidth) / 2;
      const y = (videoHeight - boxHeight) / 2;

      context.clearRect(0, 0, videoWidth, videoHeight);
      context.beginPath();
      context.rect(x, y, boxWidth, boxHeight);
      context.strokeStyle = 'cyan';
      context.lineWidth = 4;
      context.stroke();
    }
  };

  const handlePhotoSubmit = () => {
    if (capturedImage) {
      handleImageSubmit(capturedImage.split('base64,')[1]);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-cyan-100 p-4">
      <div className="absolute top-4 left-4">
        <button onClick={() => navigate(-1)} className="px-4 py-2 bg-gray-400 text-white rounded">Back</button>
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
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-cyan-500 focus:border-cyan-500 sm:text-md"
          >
            <option value="">Select a student</option>
            {students.map((student) => (
              <option key={student.id} value={student.id}>{student.name}</option>
            ))}
          </select>
        </div>
      )}
      {!image ? (
        <div className="relative">
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            onUserMedia={() => drawAlignmentBox()}
            videoConstraints={{
              width: 640,
              height: 480,
              facingMode: "user"
            }}
            className="w-full"
          />
          <canvas ref={canvasRef} className="absolute top-0 left-0" />
          <button onClick={capture} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition duration-300">
            Take Photo
          </button>
        </div>
      ) : (
        <>
          <img src={image} alt="Captured" className="max-w-lg rounded-lg shadow-xl" />
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
    </div>
  );
};
