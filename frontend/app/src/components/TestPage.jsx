import React, { useState, useEffect, useContext } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { BackButton } from "./BackButton";
import { AuthContext } from "../context/auth";
import { EasyRequest, defHeaders, instanceURL } from "../api/helpers";
import {
  BarChart,
  Bar,
  Label,
  XAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import {
  Dialog,
  DialogPanel,
  Popover,
  PopoverButton,
  PopoverGroup,
  PopoverPanel,
  Transition,
} from "@headlessui/react";
import { Bars3Icon, XMarkIcon, ChevronDownIcon } from "@heroicons/react/24/outline";

function formatDateTime(datetime) {
  const date = new Date(datetime);
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return date.toLocaleString(undefined, options);
}

export const TestPage = () => {
  const { id } = useParams();
  const [test, setTest] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [grades, setGrades] = useState([]);
  const [testHigh, setTestHigh] = useState(0);
  const [testLow, setTestLow] = useState(0);
  const [testAvg, setTestAvg] = useState(0);
  const { authDetails } = useContext(AuthContext);
  const navigate = useNavigate();

  const [editMode, setEditMode] = useState(false);
  const [updatedTestName, setUpdatedTestName] = useState("");
  const [updatedStartDate, setUpdatedStartDate] = useState("");
  const [updatedEndDate, setUpdatedEndDate] = useState("");

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
    const interval = setInterval(fetchTestData, 20000);

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
    try {
      const deleteURL = `${instanceURL}/submission/${submissionId}`;
      let req = await EasyRequest(deleteURL, defHeaders, "DELETE");

      if (req.status === 200) {
        setSubmissions((prevSubmissions) =>
          prevSubmissions.filter((submission) => submission.id !== submissionId)
        );
        processGrades(submissions.filter((submission) => submission.id !== submissionId));
      }
    } catch (error) {
      console.error("Error deleting submission", error);
    }
  };

  const handleDownload = async (type) => {
    const url = `${instanceURL}/test/image/${type}/${id}/`;
    window.open(url, "_blank");
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

  const buckets = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
  const histogramData = buckets.map((bucket, index, array) => {
    const bucketCount = grades.filter(
      (grade) =>
        grade >= bucket &&
        (index === array.length - 1 || grade < array[index + 1])
    ).length;

    return {
      grade: `${bucket}`,
      count: bucketCount,
    };
  });

  return (
    <div className="min-h-screen mx-auto w-full bg-cyan-50">
      <header className="bg-white">
        <nav className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
          <div className="flex items-center gap-x-12">
            <BackButton className="px-8 py-3 text-sm font-semibold rounded-md shadow-sm bg-cyan-200 text-gray-700 hover:bg-cyan-300" />
          </div>
          <PopoverGroup className="hidden lg:flex lg:gap-x-12">
            <Popover className="relative">
              <PopoverButton className="flex items-center gap-x-1 text-sm font-semibold leading-6 text-gray-900">
                Test Options
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
                        Edit Test
                      </button>
                    </div>
                    <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                      <button
                        onClick={handleDeleteTest}
                        className="w-full text-left"
                      >
                        Delete Test
                      </button>
                    </div>
                    <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                      <button
                        onClick={() => handleDownload("blank")}
                        className="w-full text-left"
                      >
                        Download Blank Answer Sheet
                      </button>
                    </div>
                    <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                      <button
                        onClick={() => handleDownload("key")}
                        className="w-full text-left"
                      >
                        Download Key Answer Sheet
                      </button>
                    </div>
                  </div>
                </PopoverPanel>
              </Transition>
            </Popover>
          </PopoverGroup>
          <div className="lg:hidden">
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
                        Edit Test
                      </button>
                    </div>
                    <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                      <button
                        onClick={handleDeleteTest}
                        className="w-full text-left"
                      >
                        Delete Test
                      </button>
                    </div>
                    <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                      <button
                        onClick={() => handleDownload("blank")}
                        className="w-full text-left"
                      >
                        Download Blank Answer Sheet
                      </button>
                    </div>
                    <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                      <button
                        onClick={() => handleDownload("key")}
                        className="w-full text-left"
                      >
                        Download Key Answer Sheet
                      </button>
                    </div>
                  </div>
                </PopoverPanel>
              </Transition>
            </Popover>
          </div>
        </nav>
      </header>

      {test && (
        <div className="mx-auto max-w-7xl px-6 lg:px-8 mt-4">
          <div className={`px-4 py-2 rounded-md text-white text-center ${handleDateFormatting(test.start_t, test.end_t) === 'LIVE' ? 'bg-green-500' : handleDateFormatting(test.start_t, test.end_t) === 'IN WAIT' ? 'bg-yellow-500' : 'bg-gray-500'}`}>
            {handleDateFormatting(test.start_t, test.end_t)}
          </div>
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
            <div className="mt-6">
              <input
                type="text"
                value={updatedTestName}
                onChange={(e) => setUpdatedTestName(e.target.value)}
                className="block w-full border-gray-300 rounded-md"
                placeholder="Test Name"
              />
              <input
                type="datetime-local"
                value={updatedStartDate}
                onChange={(e) => setUpdatedStartDate(e.target.value)}
                className="block w-full border-gray-300 rounded-md mt-4"
                placeholder="Start Date"
              />
              <input
                type="datetime-local"
                value={updatedEndDate}
                onChange={(e) => setUpdatedEndDate(e.target.value)}
                className="block w-full border-gray-300 rounded-md mt-4"
                placeholder="End Date"
              />
              <button
                onClick={handleUpdateTest}
                className="block w-full bg-blue-500 text-white rounded-md mt-4 py-2"
              >
                Update Test
              </button>
            </div>
          )}
          
          <div className="mt-6"> 
            <h2 className="text-xl font-semibold">Grade Distribution</h2>
            <div className="mt-6">
              <div className="flex justify-between mt-4">
                <div className="text-left">
                  <p className="font-semibold">Low</p>
                  <p>{testLow}</p>
                </div>

                <div className="text-center">
                  <p className="font-semibold">Average</p>
                  <p>{testAvg}</p>
                </div>

                <div className="text-right">
                  <p className="font-semibold">High</p>
                  <p>{testHigh}</p>
                </div>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={histogramData}>
                <XAxis dataKey="grade">
                  <Label value="Grades" offset={0} position="insideBottom" />
                </XAxis>
                <Tooltip />
                <Bar dataKey="count" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
            <div className="mt-6">
            <h2 className="text-xl font-semibold">Submissions</h2>
            <ul>
              {submissions.map((submission) => (
                <li key={submission.id} className="mt-2">
                  {submission.name} - {submission.grade}
                  <button
                    onClick={() => handleDeleteSubmission(submission.id)}
                    className="ml-4 text-red-500"
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          </div>
          </div>
        </div>
      </div>
    </div>
  );
};
