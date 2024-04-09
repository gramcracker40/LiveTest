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
  const { authDetails, updateAuthDetails } = useContext(AuthContext);

  const testAvg = 90;
  const myGrade = 82.4356;
  const testHigh = 100;
  const testLow = 50;

  useEffect(() => {
    course.tests.length > 0 ? setAreTests(true) : setAreTests(false);
  }, []);

  // Array of student grades
  const grades = [
    84, 81, 75, 92, 67, 73, 84, 86, 80, 83, 89, 72, 86, 79, 73, 76, 81, 68, 83,
    84, 81, 76, 68, 76, 75, 83, 83, 85, 85, 77, 82, 88, 76, 89, 78, 77, 90, 87,
    78, 83, 100,
  ];

  // Histogram buckets
  const buckets = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];

  // Function to count the grades in each bucket
  const histogramData = buckets.map((bucket, index, array) => {
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
        {areTests && selectedTest && authDetails.type === "student" ? (
          <Analytics
            histogramData={histogramData}
            grade={myGrade}
            testAvg={testAvg}
            testHigh={testHigh}
            testLow={testLow}
          />
        ) : areTests && selectedTest && authDetails.type === "teacher" ? (
          <Analytics
            histogramData={histogramData}
            grade={testAvg}
            testAvg={testAvg}
            testHigh={testHigh}
            testLow={testLow}
          />
        ) : areTests && !selectedTest ? (
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

  const { authDetails, updateAuthDetails } = useContext(AuthContext);

  const testAvg = props.testAvg;
  const grade = props.grade;
  const testHigh = props.testHigh;
  const testLow = props.testLow;

  const histogramData = props.histogramData;

  return (
    <>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-8 ">
        <HistogramChart histogramData={histogramData} />
        <PieChartGrade
          grade={grade}
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
            {course.students.map((student, studentIndex) => (
              <li
                key={studentIndex}
                className={`Test-${studentIndex} flex justify-between my-2`}
              >
                <span className="text-md font-light">{student.name}</span>
                <span className="text-md">
                  {Math.round(Math.random() * 10000) / 100}
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
