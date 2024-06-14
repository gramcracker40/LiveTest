import React from 'react';
import { BarChart, Bar, Label, XAxis, Tooltip, ResponsiveContainer } from "recharts";

export const GradeDistribution = ({ testLow, testHigh, testAvg, grades }) => {
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
    </div>
  );
};
