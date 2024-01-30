import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { BackButton } from './BackButton';

export const CreateTestPage = () => {
    const [testDetails, setTestDetails] = useState({
        name: '',
        startTime: '',
        endTime: '',
        numberOfQuestions: '',
        answerKey: null
    });

    const navigate = useNavigate();
    const handleNavigate = (path) => {
        navigate(path)
    }

    const location = useLocation();
    const { courseId } = location.state || {};

    const handleInputChange = (e) => {
        setTestDetails({ ...testDetails, [e.target.name]: e.target.value });
    };

    const handleFileChange = (e) => {
        // Assuming only the first file is relevant
        const file = e.target.files[0];
        if (file) {
            // Additional checks can be added for file type
            setTestDetails({ ...testDetails, answerKey: file });
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Validate input data
        if (new Date(testDetails.endTime) <= new Date(testDetails.startTime)) {
            alert("End time must be after start time.");
            return;
        }
        // Submit logic here
        console.log(testDetails);
        navigate("/course"); // Navigate to the next route after submission
    };

      useEffect(() => {
        console.log(`course ID: ${courseId}`)
      }, [navigate])

    return (
        <div className="bg-LogoBg w-full h-screen flex flex-col justify-center px-6 py-12 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <h1 className="text-center text-6xl font-bold text-cyan-500">Create Test</h1>
                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700">Test Name</label>
                        <input
                            id="name"
                            name="name"
                            type="text"
                            required
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-cyan-500 focus:border-cyan-500 sm:text-md"
                            value={testDetails.name}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
                        <div>
                            <label htmlFor="startTime" className="block text-sm font-medium text-gray-700">Start Time</label>
                            <input
                                id="startTime"
                                name="startTime"
                                type="datetime-local"
                                required
                                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-cyan-500 focus:border-cyan-500 sm:text-md"
                                value={testDetails.startTime}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="endTime" className="block text-sm font-medium text-gray-700">End Time</label>
                            <input
                                id="endTime"
                                name="endTime"
                                type="datetime-local"
                                required
                                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-cyan-500 focus:border-cyan-500 sm:text-md"
                                value={testDetails.endTime}
                                onChange={handleInputChange}
                            />
                        </div>
                    </div>
                    <div>
                        <label htmlFor="numberOfQuestions" className="block text-sm font-medium text-gray-700">Number of Questions</label>
                        <input
                            id="numberOfQuestions"
                            name="numberOfQuestions"
                            type="number"
                            required
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-cyan-500 focus:border-cyan-500 sm:text-md"
                            value={testDetails.numberOfQuestions}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div>
                        <label htmlFor="answerKey" className="block text-sm font-medium text-gray-700">Answer Key</label>
                        <input
                            id="answerKey"
                            name="answerKey"
                            type="file"
                            required
                            accept="image/jpeg"
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-cyan-500 focus:border-cyan-500 sm:text-sm"
                            onChange={handleFileChange}
                        />
                    </div>
                    <div>
                        <button
                            type="submit"
                            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-cyan-600 hover:bg-cyan-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500"
                        >
                            Create Test
                        </button>
                    </div>
                    <div className="flex justify-center mt-4">
                        < BackButton className="px-8 py-3 text-sm font-semibold rounded-md shadow-sm bg-cyan-200 text-gray-700 hover:bg-cyan-300" />
                    </div>
                </form>
            </div>
        </div>
    );
};
