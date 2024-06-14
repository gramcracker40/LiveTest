import React, { useEffect, useState } from 'react';
import { BarChart, Bar, Label, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { EasyRequest, defHeaders, instanceURL } from '../../api/helpers';

export const QuestionsMissedPercentage = ({ submissions }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (submissions.length > 0) {
      calculateMissedQuestionsPercentage(submissions);
    }
  }, [submissions]);

  const calculateMissedQuestionsPercentage = async (submissions) => {
    const questionStats = {};

    for (const submission of submissions) {
      try {
        const answersURL = `${instanceURL}/submission/etc/answers/${submission.id}`;
        const answersReq = await EasyRequest(answersURL, defHeaders, "GET");

        if (answersReq.status === 200) {
          const answers = answersReq.data.answers;

          Object.keys(answers).forEach(questionId => {
            const answer = answers[questionId];
            if (!questionStats[questionId]) {
              questionStats[questionId] = { total: 0, missed: 0 };
            }
            questionStats[questionId].total += 1;
            if (!answer.correct) {
              questionStats[questionId].missed += 1;
            }
          });
        } else {
          console.error(`Failed to fetch answers for submission ${submission.id}: ${answersReq.statusText}`);
        }
      } catch (error) {
        console.error(`Error fetching answers for submission ${submission.id}:`, error);
      }
    }

    const chartData = Object.keys(questionStats).map(questionId => {
      const stat = questionStats[questionId];
      return {
        question: questionId,
        percentage: parseFloat(((stat.missed / stat.total) * 100).toFixed(2)) // Convert to percentage
      };
    });

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
          <YAxis tickFormatter={(tick) => `${tick}%`} domain={[0, 100]}>
            <Label value="Percentage Missed" angle={-90} position="insideLeft" />
          </YAxis>
          <Tooltip formatter={(value) => `${value}%`} />
          <Bar dataKey="percentage" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
