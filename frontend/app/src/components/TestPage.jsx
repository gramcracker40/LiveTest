import React, { useState, useEffect, useContext } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { AuthContext } from "../context/auth";
import { EasyRequest, defHeaders, instanceURL } from "../api/helpers";
import { TestPageHeader } from "./TestPageHeader";
import { GradeDistribution } from "./Analytics/GradeDistribution";
import { SubmissionsList } from "./SubmissionsList";
import { EditTestForm } from "./EditTestForm";
import { DeleteConfirmation } from "./DeleteConfirmation";
import { QuestionsMissedPercentage } from "./Analytics/QuestionsMissedPercentage"; // Add this line
import { formatDateTime } from "../utils";

export const TestPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { authDetails } = useContext(AuthContext);
  const [test, setTest] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [grades, setGrades] = useState([]);
  const [testHigh, setTestHigh] = useState(0);
  const [testLow, setTestLow] = useState(0);
  const [testAvg, setTestAvg] = useState(0);
  const [editMode, setEditMode] = useState(false);
  const [updatedTestName, setUpdatedTestName] = useState("");
  const [updatedStartDate, setUpdatedStartDate] = useState("");
  const [updatedEndDate, setUpdatedEndDate] = useState("");
  const [isDeleteTestConfirmOpen, setIsDeleteTestConfirmOpen] = useState(false);
  const [isDeleteSubmissionConfirmOpen, setIsDeleteSubmissionConfirmOpen] = useState(false);
  const [submissionToDelete, setSubmissionToDelete] = useState(null);

  useEffect(() => {
    if (!authDetails.isLoggedIn) {
      navigate("/");
      return;
    }

    const fetchTestData = async () => {
      try {
        const testURL = `${instanceURL}/test/${id}`;
        const submissionsURL = `${instanceURL}/submission/test/${id}`;
        let testReq = await EasyRequest(testURL, defHeaders, "GET");
        let submissionsReq = await EasyRequest(submissionsURL, defHeaders, "GET");

        if (testReq.status === 200) {
          setTest(testReq.data);
          setUpdatedTestName(testReq.data.name);
          setUpdatedStartDate(testReq.data.start_t);
          setUpdatedEndDate(testReq.data.end_t);
        }
        if (submissionsReq.status === 200) {
          setSubmissions(submissionsReq.data);
          processGrades(submissionsReq.data);
        }
      } catch (error) {
        console.error("Error fetching test data", error);
      }
    };

    fetchTestData();
    const interval = setInterval(fetchTestData, 180000); // update page every 3 minutes

    return () => clearInterval(interval);
  }, [authDetails, navigate, id]);

  const processGrades = (submissions) => {
    let sum = 0;
    let low = 101;
    let high = -1;
    let grades = submissions.map((submission) => submission.grade);

    grades.forEach((grade) => {
      sum += grade;
      if (grade > high) high = grade;
      if (grade < low) low = grade;
    });

    setGrades(grades);
    setTestLow(Math.round(low * 100) / 100);
    setTestHigh(Math.round(high * 100) / 100);
    setTestAvg(Math.round((sum / grades.length) * 100) / 100);
  };

  const handleDateFormatting = (start, end) => {
    const testStart = new Date(start);
    const testEnd = new Date(end);
    const now = new Date();

    if (now >= testStart && now <= testEnd) {
      return "LIVE";
    } else if (testStart > now) {
      return "IN WAIT";
    } else if (testEnd < now) {
      return "FINALIZED";
    } else {
      const day = String(testStart.getDate());
      const month = String(testStart.getMonth() + 1);
      const year = String(testStart.getFullYear()).slice(2);
      return `${month}-${day}-${year}`;
    }
  };

  const handleDeleteTest = async () => {
    try {
      const deleteURL = `${instanceURL}/test/${id}`;
      let req = await EasyRequest(deleteURL, defHeaders, "DELETE");

      if (req.status === 200) {
        navigate("/course");
      }
    } catch (error) {
      console.error("Error deleting test", error);
    }
  };

  const handleDeleteSubmission = async (submissionId) => {
    setIsDeleteSubmissionConfirmOpen(true);
    setSubmissionToDelete(submissionId);
  };

  const confirmDeleteSubmission = async () => {
    try {
      const deleteURL = `${instanceURL}/submission/${submissionToDelete}`;
      let req = await EasyRequest(deleteURL, defHeaders, "DELETE");

      if (req.status === 200) {
        setSubmissions((prevSubmissions) =>
          prevSubmissions.filter((submission) => submission.id !== submissionToDelete)
        );
        processGrades(submissions.filter((submission) => submission.id !== submissionToDelete));
        setIsDeleteSubmissionConfirmOpen(false);
      }
    } catch (error) {
      console.error("Error deleting submission", error);
    }
  };

  const handleUpdateTest = async () => {
    const updateData = {
      name: updatedTestName,
    };

    if (handleDateFormatting(test.start_t, test.end_t) !== "FINALIZED") {
      updateData.start_t = updatedStartDate;
      updateData.end_t = updatedEndDate;
    }

    try {
      const updateURL = `${instanceURL}/test/${id}`;
      let req = await EasyRequest(updateURL, defHeaders, "PATCH", updateData);

      if (req.status === 200) {
        setTest((prevTest) => ({
          ...prevTest,
          name: updatedTestName,
          start_t: updatedStartDate,
          end_t: updatedEndDate,
        }));
        setEditMode(false);
      }
    } catch (error) {
      console.error("Error updating test", error);
    }
  };

  const handleDownload = async (type) => {
    try {
      const url = `${instanceURL}/test/image/${type}/${id}/`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error('Failed to fetch image');
      }

      const compressedArrayBuffer = await response.arrayBuffer();
      const decompressedData = pako.inflate(new Uint8Array(compressedArrayBuffer));
      const blob = new Blob([decompressedData], { type: 'image/jpeg' });
      const downloadUrl = URL.createObjectURL(blob);

      // Open the image in a new tab
      window.open(downloadUrl, "_blank");

      // Optionally revoke the object URL after a short delay to allow the image to load
      setTimeout(() => {
        URL.revokeObjectURL(downloadUrl);
      }, 10000); // 10 seconds delay
    } catch (error) {
      console.error('Error downloading image', error);
    }
  };

  return (
    <div className="min-h-screen mx-auto w-full bg-cyan-50">
      <TestPageHeader
        handleDateFormatting={handleDateFormatting}
        test={test}
        setEditMode={setEditMode}
        setIsDeleteTestConfirmOpen={setIsDeleteTestConfirmOpen}
        handleDownload={handleDownload}
        id={id}
        navigate={navigate}
      />
      {test && (
        <div className="mx-auto max-w-7xl px-6 lg:px-8 mt-4">
          <div className={`px-4 py-2 rounded-md text-white text-center ${handleDateFormatting(test.start_t, test.end_t) === 'LIVE' ? 'bg-green-500' : handleDateFormatting(test.start_t, test.end_t) === 'IN WAIT' ? 'bg-yellow-500' : 'bg-gray-500'}`}>
            {handleDateFormatting(test.start_t, test.end_t)}
          </div>
          {handleDateFormatting(test.start_t, test.end_t) === 'LIVE' && (
            <div className="mt-4 text-center">
              <button
                onClick={() => navigate(`/submission/${id}`, { state: { test } })}
                className="px-4 py-2 bg-blue-500 text-white rounded-md"
              >
                Create a new submission
              </button>
            </div>
          )}
        </div>
      )}
      <div className="py-10">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">{test && test.name}</h1>
          {test && (
            <div className="mt-6">
              <div className="flex justify-between mt-4">
                <div className="text-left">
                  <p className="font-semibold">Start</p>
                  <p>{formatDateTime(test.start_t)}</p>
                </div>
                <div className="text-right">
                  <p className="font-semibold">End</p>
                  <p>{formatDateTime(test.end_t)}</p>
                </div>
              </div>
            </div>
          )}
          {editMode && (
            <EditTestForm
              updatedTestName={updatedTestName}
              setUpdatedTestName={setUpdatedTestName}
              updatedStartDate={updatedStartDate}
              setUpdatedStartDate={setUpdatedStartDate}
              updatedEndDate={updatedEndDate}
              setUpdatedEndDate={setUpdatedEndDate}
              handleUpdateTest={handleUpdateTest}
            />
          )}
          <GradeDistribution
            testLow={testLow}
            testHigh={testHigh}
            testAvg={testAvg}
            grades={grades}
          />
          <QuestionsMissedPercentage submissions={submissions} />
          <SubmissionsList
            submissions={submissions}
            onDeleteSubmission={handleDeleteSubmission}
          />
        </div>
      </div>
      <DeleteConfirmation
        isOpen={isDeleteTestConfirmOpen}
        onClose={() => setIsDeleteTestConfirmOpen(false)}
        onDelete={handleDeleteTest}
        title="Delete Test"
        message="Are you sure you want to delete this test? This will remove all associated submissions and grades."
      />
      <DeleteConfirmation
        isOpen={isDeleteSubmissionConfirmOpen}
        onClose={() => setIsDeleteSubmissionConfirmOpen(false)}
        onDelete={confirmDeleteSubmission}
        title="Delete Submission"
        message="Are you sure you want to delete this submission? This action cannot be undone."
      />
    </div>
  );
};
