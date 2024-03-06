import React, { useState, useEffect, useContext, PureComponent } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { BackButton } from './BackButton';
import { AuthContext } from '../context/auth';
import { EasyRequest, defHeaders, instanceURL } from '../api/helpers';
import { BarChart, Bar, Label, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export const AnalyticsPage = () => {

    const location = useLocation()
    const test = location.state.test

    const testAvg = 90;
    const myGrade = 55;
    const testHigh = 100;
    const testLow = 50;

    // I want to make a 2 column grid. on the left side will be a histogram of the grades of the whole class.
    // and on the right side will be the standard deviation showing the high, low, avg, and students grade

    // Array of student grades
    const grades = [84, 81, 75, 92, 67, 73, 84, 86, 80, 83,
        89, 72, 86, 79, 73, 76, 81, 68, 83, 84,
        81, 76, 68, 76, 75, 83, 83, 85, 85, 77,
        82, 88, 76, 89, 78, 77, 90, 87, 78, 83, 100]


    // Histogram buckets
    const buckets = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];

    // Function to count the grades in each bucket
    const histogramData = buckets.map((bucket, index, array) => {
        const bucketCount = grades.filter(grade =>
            grade >= bucket && (index === array.length - 1 || grade < array[index + 1])
        ).length;

        return {
            grade: `${bucket}`,
            count: bucketCount,
        };
    });

    const pieData = [
        { name: 'grade', value: myGrade },
    ];

    return (
        <div className=" min-h-screen mx-auto w-full bg-cyan-50">
            <div className='sm:px-20 sm:py-8 px-4 py-4'>
                <div className='gap-x-8 mb-7 p-4 rounded-lg shadow bg-white'>
                    <h1 className='text-5xl justify-center flex'>
                        {test.name}
                    </h1>
                </div>
                <Analytics pieData={pieData} histogramData={histogramData} myGrade={myGrade} testAvg={testAvg} testHigh={testHigh} testLow={testLow}  />
            </div>
        </div>


    )
}

export const Analytics = (props) => {

    const testAvg = props.testAvg;
    const myGrade = props.myGrade;
    const testHigh = props.testHigh;
    const testLow = props.testLow;

    const histogramData = props.histogramData;
    const pieData = props.pieData

    // Colors for each type of grade. Green for >= 70. Yellow for >= 60. Red for everything else.
    const COLORS = ['#13CD34', '#FFE800', '#EF2424'];

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-8 ">
            <div className="mb-8 p-4 bg-white rounded-lg shadow">
                <span className='flex justify-center text-lg'>Class Grades</span>
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
                        <Bar dataKey="count" fill="#8884d8" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
            <div className='mb-8 p-4 bg-white rounded-lg shadow grid grid-cols-2'>
                <div>
                    <span className='justify-center flex text-lg'>My Grade</span>
                    <PieChart width={200} height={200} className='justify-center flex'>
                        <Pie
                            data={pieData}
                            cx="50%"
                            cy="50%"
                            innerRadius={65}
                            outerRadius={80}
                            fill={myGrade >= 70 ? COLORS[0] : myGrade >= 60 ? COLORS[1] : COLORS[2]}
                            title="My grade"
                            dataKey="value"
                            startAngle={90} // Starting angle
                            endAngle={(-360 * (myGrade / 100.0)) + 90} // End angle, this is where you control the fill amount
                        >
                            <Label
                                value={Math.round(100 * myGrade) / 100}
                                position="center"
                                className='text-black text-5xl justify-center '
                            />
                        </Pie>
                    </PieChart>
                </div>
                <div className='grid grid-rows-3 ml-3'>
                    <div className='border-cyan-700 border rounded-3xl mb-2'>
                        <div className='flex flex-col m-3'>
                            <span className='self-start'>Average</span>
                            <span className='flex-grow flex items-center justify-center text-3xl'>{testAvg}</span>
                        </div>
                    </div>
                    <div className=' border-cyan-700 border rounded-3xl mb-2'>
                        <div className='flex flex-col m-3'>
                            <span className='self-start'>High</span>
                            <span className='flex-grow flex items-center justify-center text-3xl'>{testHigh}</span>
                        </div>
                    </div>
                    <div className=' border-cyan-700 border rounded-3xl mb-1'>
                        <div className='flex flex-col m-3'>
                            <span className='self-start'>Low</span>
                            <span className='flex items-center justify-center text-4xl'>{testLow}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

