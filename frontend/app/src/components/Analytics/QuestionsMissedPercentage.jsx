// ./Analytics/QuestionsMissedPercentage.jsx
import React, { useEffect, useState } from 'react';
import { BarChart, Bar, Label, XAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { EasyRequest, defHeaders, instanceURL } from '../../api/helpers';

export const QuestionsMissedPercentage = ({ submissions }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    console.log("useEffect called with submissions:", submissions);
    if (submissions && submissions.length > 0) {
      console.log("Fetching answers for each submission...");
      fetchAnswersForSubmissions(submissions);
    } else {
      console.log("No submissions available to process.");
    }
  }, [submissions]);

  const fetchAnswersForSubmissions = async (submissions) => {
    try {
      const allAnswers = await Promise.all(submissions.map(async (submission) => {
        const answersURL = `${instanceURL}/submission/etc/answers/${submission.id}`;
        const answersReq = await EasyRequest(answersURL, defHeaders, "GET");
        if (answersReq.status === 200) {
          console.log(`Fetched answers for submission ${submission.id}:`, answersReq.data.answers);
          return answersReq.data.answers;
        } else {
          console.error(`Failed to fetch answers for submission ${submission.id}:`, answersReq.statusText);
          return null;
        }
      }));
      console.log("All fetched answers:", allAnswers);
      calculateMissedQuestionsPercentage(allAnswers.filter(Boolean));
    } catch (error) {
      console.error("Error fetching answers for submissions:", error);
    }
  };

  const calculateMissedQuestionsPercentage = (answersList) => {
    const questionStats = {};
    console.log("Starting calculation for answersList:", answersList);

    answersList.forEach((answers, index) => {
      console.log(`Processing answers for submission ${index + 1}:`, answers);
      Object.keys(answers).forEach(questionId => {
        const answer = answers[questionId];
        console.log(`Processing question ${questionId}:`, answer);
        if (!questionStats[questionId]) {
          questionStats[questionId] = { total: 0, missed: 0 };
        }
        questionStats[questionId].total += 1;
        if (!answer.correct) {
          questionStats[questionId].missed += 1;
        }
      });
    });

    const chartData = Object.keys(questionStats).map(questionId => {
      const stat = questionStats[questionId];
      const percentage = (stat.missed / stat.total) * 100;
      console.log(`Question ${questionId}: ${stat.missed} missed out of ${stat.total}, percentage: ${percentage}%`);
      return {
        question: questionId,
        percentage: percentage
      };
    });

    console.log("Final chart data:", chartData);
    setData(chartData);
  };

  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold">Most Missed Questions</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <XAxis dataKey="question">
            <Label value="Questions" offset={0} position="insideBottom" />
          </XAxis>
          <Tooltip />
          <Bar dataKey="percentage" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
