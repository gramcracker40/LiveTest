import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { BackButton } from './BackButton';
import { AuthContext } from '../context/auth';
import { EasyRequest, defHeaders, instanceURL } from '../api/helpers';

export const CreateCoursePage = () => {
    const navigate = useNavigate();
    const [courseName, setCourseName] = useState('');
    const [semester, setSemester] = useState('');
    const [courseNumber, setCourseNumber] = useState('');
    const [section, setSection] = useState('');
    const [year, setYear] = useState('');
    const [subject, setSubject] = useState('');
    const { authDetails, updateAuthDetails } = useContext(AuthContext);

    const handleNavigate = (path) => {
        navigate(path)
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        // Here you would usually call an API to create the course
        // with the state variables as the payload.
        // For now, let's just log the values to the console.
        console.log({ courseName, semester, courseNumber, section, year, subject });
        // navigate to another route after submission if needed
        // navigate('/some-route');

        createCourse();
    };

    useEffect(() => {
        // ------------------------ AUTHENTICATION DETAILS ---------------------------

        // if a user isn't logged in, take them back to the login page
        if (!authDetails.isLoggedIn && authDetails.type != "teacher") {
            navigate("/login")
            return
        }

    }, [authDetails, navigate])

    const createCourse = async () => {
        const body = {
            "name": courseName,
            "semester_season": semester,
            "course_number": courseNumber,
            "section": section,
            "year": year,
            "teacher_id": authDetails.id,
            "subject": subject
        }

        const URL = instanceURL + "/course/"

        try {
            let req = await EasyRequest(URL, defHeaders, "POST", body)

            if (req.status === 200) {
                navigate("/course")
            }
        }
        catch(error) {
            console.error('Error creating course', error);
        }
    }


    return (
        <div className="bg-LogoBg w-full h-screen flex flex-col justify-center px-6 py-12 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-lg">
                <h1 className="font-bold text-6xl text-center mb-4 text-cyan-500">
                    Create Course
                </h1>
                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    <input
                        type="text"
                        required
                        placeholder="Course Name"
                        value={courseName}
                        onChange={(e) => setCourseName(e.target.value)}
                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm"
                    />
                    <div className='grid sm:grid-cols-3 gap-y-6 gap-x-4'>
                        <div>
                            <select
                                required
                                value={semester}
                                onChange={(e) => setSemester(e.target.value)}
                                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm"
                            >
                                <option value="">Select Semester</option>
                                <option value="Fall">Fall</option>
                                <option value="Spring">Spring</option>
                                <option value="Summer I">Summer I</option>
                                <option value="Summer II">Summer II</option>
                            </select>
                        </div>
                        <div>
                            <input
                                type="text"
                                required
                                placeholder="Course Number"
                                value={courseNumber}
                                onChange={(e) => setCourseNumber(e.target.value)}
                                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm"
                            />
                        </div>
                        <div>
                            <input
                                type="text"
                                required
                                placeholder="Section"
                                value={section}
                                onChange={(e) => setSection(e.target.value)}
                                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm"
                            />
                        </div>
                    </div>

                    <div className='grid sm:grid-cols-2 gap-y-6 gap-x-4'>
                        <div>
                            <input
                                type="text"
                                required
                                placeholder="Year"
                                value={year}
                                onChange={(e) => setYear(e.target.value)}
                                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm"
                            />
                        </div>
                        <div>
                            <input
                                type="text"
                                required
                                placeholder="Subject"
                                value={subject}
                                onChange={(e) => setSubject(e.target.value)}
                                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500 sm:text-sm"
                            />
                        </div>
                    </div>
                    <button
                        type="submit"
                        className="flex w-full justify-center rounded-md bg-cyan-500 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-cyan-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500"
                    >
                        Create Course
                    </button>
                </form>
            </div>
            <div className="flex justify-center mt-4">
                < BackButton className="px-8 py-3 text-sm font-semibold rounded-md shadow-sm bg-cyan-200 text-gray-700 hover:bg-cyan-300" />
            </div>
        </div >
    );
};