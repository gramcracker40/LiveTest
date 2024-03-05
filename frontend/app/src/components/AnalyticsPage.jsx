import React, { useState, useEffect, useContext } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { BackButton } from './BackButton';
import { AuthContext } from '../context/auth';
import { EasyRequest, defHeaders, instanceURL } from '../api/helpers';

export const AnalyticsPage = () => {
    const location = useLocation()

    const test = location.state.test

    return (
        <div>
            Your test: {JSON.stringify(test)}
        </div>
    )
}