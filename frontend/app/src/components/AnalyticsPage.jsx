import React, { useState, useEffect, useContext } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { BackButton } from './BackButton';
import { AuthContext } from '../context/auth';
import { EasyRequest, defHeaders, instanceURL } from '../api/helpers';

export const AnalyticsPage = () => {
    const location = useLocation()

    const test = location.state.test

    const testAvg = 90;
    const myGrade = 70;
    const testHigh = 100;
    const testLow = 50;

    // I want to make a 2 column grid. on the left side will be a histogram of the grades of the whole class.
    // and on the right side will be the standard deviation showing the high, low, avg, and students grade

    return (
        <div className=" min-h-screen mx-auto w-full bg-cyan-50">
            <div className='sm:px-28 sm:py-8 px-4 py-4'>
                <div className='gap-x-8 mb-7 p-4 rounded-lg shadow bg-white'>
                    <h1 className='text-5xl justify-center flex'>
                        {test.name}
                    </h1>
                </div>
            </div>
        </div>
    )
}