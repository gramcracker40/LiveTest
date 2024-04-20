import React, { useState, useEffect, useContext, PureComponent } from "react";
import { useNavigate, useLocation } from "react-router-dom";
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
  PieChart,
  Pie,
} from "recharts";

export const AnalyticsPage = () => {
  const location = useLocation();
  const course = location.state.course;

  const [selectedTest, setSelectedTest] = useState();
  const [areTests, setAreTests] = useState(false);
  const [testSubmissions, setTestSubmissions] = useState([]);
  const [areSubmissions, setAreSubmissions] = useState(false);
  const [myGrade, setMyGrade] = useState(null);
  const { authDetails, updateAuthDetails } = useContext(AuthContext);

  const navigate = useNavigate();

  useEffect(() => {

    // ------------------------ AUTHENTICATION DETAILS ---------------------------

    // if a user isn't logged in, take them back to the login page
    if (!authDetails.isLoggedIn) {
      navigate("/")
      return
    }

    console.log(course)

    // make sure the course has tests
    course.tests.length > 0 ? setAreTests(true) : setAreTests(false);

  }, []);

  useEffect(() => {
    if(!areTests) {
      setAreSubmissions(false)
    }
  }, [areTests])

  useEffect(() => {
    console.log(testSubmissions)
    if(testSubmissions.length === 0) {
      setAreSubmissions(false);
    }
    else {
      setAreSubmissions(true);
    }
  }, [testSubmissions])

  useEffect(() => {
    console.log("student g ", myGrade)
  }, [myGrade])

  useEffect(() => {
    console.log(selectedTest)

    const fetchTestInfo = async () => {

      const testSubmissionsURL = instanceURL + `/submission/test/${selectedTest.id}`
      const studentTestSubmissionURL = instanceURL + `/submission/${selectedTest.id}/${authDetails.id}`

      try {
        let req = await EasyRequest(testSubmissionsURL, defHeaders, "GET")

        if (req.status === 200) {
          // get the submissions and set them to the testSubmissions
          setAreSubmissions(true);
          let submissions = []
          req.data.map((submission) => {
            submissions.push(submission)
          })
          setTestSubmissions(submissions);
        }
        else if(req.status === 404) {
          // there are no test submissions
          setAreSubmissions(false);
        }
        
      } catch (error) {
        console.error('Error fetching courses', error);
      }

      // if a student is logged in we want to keep track of their grade
      if (authDetails.type === 'student') {
        try {
          let req = await EasyRequest(studentTestSubmissionURL, defHeaders, "GET")
        if (req.status === 200) {
          console.log("success")
          setMyGrade(req.data.grade)
        }
        
        
      } catch (error) {
        console.error('Error fetching student grade', error);
        }
      }
    }

    fetchTestInfo();

  }, [selectedTest])

  const handleTestSelection = (test) => {
    setSelectedTest(test);
  };

  const handleDateFormatting = (start, end) => {
    const testStart = new Date(start);
    const testEnd = new Date(end);
    const now = new Date();

    if (now >= testStart && now <= testEnd) {
      // Test is currently live
      return "LIVE";
    }
    // Check if the test date is the same as today's date
    else if (testStart.toDateString() === now.toDateString()) {
      // Format as "Today at HH:MM AM/PM"
      return `Today at ${testStart.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      })}`;
    } else {
      // Format as "MM-DD-YY"
      const day = String(testStart.getDate()); //.padStart(2, '0');
      const month = String(testStart.getMonth() + 1); //.padStart(2, '0');
      const year = String(testStart.getFullYear()).slice(2);
      return `${month}-${day}-${year}`;
    }
  };

  return (
    <div className=" min-h-screen mx-auto w-full bg-cyan-50">
      <div className="sm:px-20 sm:py-8 px-4 py-4">
        <div className="gap-x-8 mb-7 p-8 rounded-2xl shadow bg-white">
          <h1 className="mb-8 text-5xl justify-center flex">{course.name}</h1>
          <div className="Tests">
            {course.tests.map((test, testIndex) => (
              <div
                key={testIndex}
                className={`Test-${testIndex} flex justify-between transform transition duration-300 hover:text-cyan-700 hover:scale-105  hover:cursor-pointer`}
                onClick={() => {
                  handleTestSelection(test);
                }}
              >
                <span className="text-md font-light">{test.name}</span>
                <span className="text-md">
                  {handleDateFormatting(test.start_t)}
                </span>
              </div>
            ))}
          </div>
        </div>
        {myGrade && selectedTest && authDetails.type === "student" ? (
          < Analytics submissions={testSubmissions} myGrade={myGrade}/>

        ) : !myGrade && selectedTest && authDetails.type === "student" ? (
          <span className="flex justify-center text-xl">
            You have not submitted a test
          </span>
        ) : areSubmissions && selectedTest && authDetails.type === "teacher" ? (
          < Analytics submissions={testSubmissions} />
        ) : !areSubmissions && selectedTest ? (
          <span className="flex justify-center text-xl">
            This test has no submissions
          </span>
        ): areTests && !selectedTest ? (
          <span className="flex justify-center text-xl">
            Please select a test
          </span>
        ) : (
          <span className="flex justify-center text-xl">
            This course has no tests
          </span>
        )}
        <div className="flex justify-center mt-4">
          <BackButton
            route="/course"
            className="px-8 py-3 text-sm font-semibold rounded-md shadow-sm bg-cyan-200 text-gray-700 hover:bg-cyan-300"
          />
        </div>
      </div>
    </div>
  );
};

export const Analytics = (props) => {
  const location = useLocation();
  const course = location.state.course;

  const [grades, setGrades] = useState([])
  const [testHigh, setTestHigh] = useState(0);
  const [testLow, setTestLow] = useState(0);
  const [testAvg, setTestAvg] = useState(0);
  const [myGrade, setMyGrade] = useState(0);
  const [testSubmissions, setTestSubmissions] = useState([])
  const { authDetails, updateAuthDetails } = useContext(AuthContext);

  useEffect(() => {
    setTestSubmissions(props.submissions)
  }, [])

  useEffect(() => {
    if(authDetails.type === 'teacher') {
      console.log("i ran: ", testAvg)
      setMyGrade(testAvg)
    }
    else if(authDetails.type === 'student') {
      setMyGrade(props.myGrade)
    }
  }, [testAvg])

  const crunchNumbers = () => {
    // setTestSubmissions(props.submissions)
    let sum = 0;
    let low = 101
    let high = -1
    let grades = []
    testSubmissions.map((submission) => {
      grades.push(submission.grade)
      sum += submission.grade;
      if (submission.grade > high) {
        high = submission.grade
      }
      if (submission.grade < low) {
        low = submission.grade
      }
    })
    setGrades(grades)
    setTestLow(Math.round(low * 100) / 100)
    setTestHigh(Math.round(high * 100) / 100)
    setTestAvg(Math.round((sum / testSubmissions.length) * 100) / 100)
    if(authDetails.type === 'teacher') {
      console.log("i ran: ", testAvg)
      setMyGrade(testAvg)
    }
    else if(authDetails.type === 'student') {
      setMyGrade(props.myGrade)
    }
  }
  
  useEffect(() => {
    crunchNumbers()
    console.log(myGrade)
  }, [testSubmissions])
  

  // Histogram buckets
  const buckets = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];

  // Function to count the grades in each bucket
  let histogramData = buckets.map((bucket, index, array) => {
    const bucketCount = grades.filter(
      (grade) =>
        grade >= bucket &&
        (index === array.length - 1 || grade < array[index + 1]),
    ).length;

    return {
      grade: `${bucket}`,
      count: bucketCount,
    };
  });

  return (
    <>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-8 ">
        <HistogramChart histogramData={histogramData} />
        <PieChartGrade
          grade={myGrade}
          testAvg={testAvg}
          testHigh={testHigh}
          testLow={testLow}
          authType={authDetails.type}
        />
      </div>
      {authDetails.type === "teacher" && (
        <div className=" px-12 py-4 rounded-lg shadow bg-white">
          <span className="flex justify-center my-4 text-lg underline">
            Student Test Grades
          </span>
          <ul>
            {testSubmissions.map((submission, submissionIndex) => (
              <li
                key={submissionIndex}
                className={`Test-${submissionIndex} flex justify-between my-2`}
              >
                <span className="text-md font-light">{submission.student_name}</span>
                <span className="text-md">
                  {Math.round(submission.grade * 100) / 100}
                </span>{" "}
                {/* THIS IS WHERE THE STUDENT GRADE WILL GO */}
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
};

export const HistogramChart = ({ histogramData }) => {
  return (
    <div className="mb-8 p-4 bg-white rounded-lg shadow">
      <span className="flex justify-center text-lg">Class Grades</span>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={histogramData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <XAxis dataKey="grade" />
          {/* <YAxis /> */}
          <Tooltip />
          <Bar dataKey="count" fill="#0097A7" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export const PieChartGrade = ({
  grade,
  testAvg,
  testHigh,
  testLow,
  authType,
}) => {
  let label = "NaN";

  if (authType === "student") {
    label = "My Grade";
  } else if (authType === "teacher") {
    label = "Test Avg";
  }

  // Colors for each type of grade. Green for >= 70. Yellow for >= 60. Red for everything else.
  const COLORS = ["#13CD34", "#FFE800", "#EF2424"];

  const pieData = [{ name: "grade", value: grade }];

  return (
    <div className="mb-8 p-4 bg-white rounded-lg shadow grid grid-cols-2">
      <div>
        <span className="justify-center flex text-lg">{label}</span>
        <div className="flex items-center justify-center h-5/6">
          <PieChart width={200} height={200}>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              innerRadius={65}
              outerRadius={80}
              fill={
                grade >= 70 ? COLORS[0] : grade >= 60 ? COLORS[1] : COLORS[2]
              }
              title="My grade"
              dataKey="value"
              startAngle={90} // Starting angle
              endAngle={-360 * (grade / 100.0) + 90} // End angle, this is where you control the fill amount
            >
              <Label
                value={Math.round(100 * grade) / 100}
                position="center"
                className="text-black text-5xl justify-center "
              />
            </Pie>
          </PieChart>
        </div>
      </div>
      <div className="grid grid-rows-3 ml-3">
        <div className="border-cyan-700 border rounded-3xl mb-2">
          <div className="flex flex-col m-3">
            <span className="self-start">Average</span>
            <span className="flex-grow flex items-center justify-center text-3xl">
              {testAvg}
            </span>
          </div>
        </div>
        <div className=" border-cyan-700 border rounded-3xl mb-2">
          <div className="flex flex-col m-3">
            <span className="self-start">High</span>
            <span className="flex-grow flex items-center justify-center text-3xl">
              {testHigh}
            </span>
          </div>
        </div>
        <div className=" border-cyan-700 border rounded-3xl mb-1">
          <div className="flex flex-col m-3">
            <span className="self-start">Low</span>
            <span className="flex items-center justify-center text-4xl">
              {testLow}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
