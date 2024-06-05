import React, { useEffect, useState } from 'react';
import { EasyRequest, defHeaders, instanceURL } from "../../api/helpers.js";
import { NavBar } from './navBar.jsx';

export const TeachersPage = () => {
  const [teachers, setTeachers] = useState([]);

  useEffect(() => {
    const fetchTeachers = async () => {
      try {
        let req = await EasyRequest(`${instanceURL}/users/teachers/`, defHeaders, "GET");
        if (req.status === 200) {
          setTeachers(req.data);
        }
      } catch (error) {
        console.error('Error fetching teachers', error);
      }
    };

    fetchTeachers();
  }, []);

  return (
    <div className="min-h-screen mx-auto w-full bg-cyan-50">
      <NavBar />
      <div className='sm:px-28 sm:py-8 px-4 py-4'>
        <div className='grid grid-cols-1 gap-x-8 mb-7 p-4 rounded-lg shadow bg-white'>
          <h1 className='text-3xl text-cyan-800 mb-4 font-bold'>
            Teachers
          </h1>
          <ul role="list" className="divide-y divide-gray-100">
            {teachers.map((teacher) => (
              <li key={teacher.email} className="flex justify-between gap-x-6 py-5">
                <div className="flex min-w-0 gap-x-4">
                  <img className="h-12 w-12 flex-none rounded-full bg-gray-50" src={teacher.imageUrl} alt="" />
                  <div className="min-w-0 flex-auto">
                    <p className="text-sm font-semibold leading-6 text-gray-900">{teacher.name}</p>
                    <p className="mt-1 truncate text-xs leading-5 text-gray-500">{teacher.email}</p>
                  </div>
                </div>
                <div className="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
                  <p className="text-sm leading-6 text-gray-900">{teacher.role}</p>
                  {teacher.lastSeen ? (
                    <p className="mt-1 text-xs leading-5 text-gray-500">
                      Last seen <time dateTime={teacher.lastSeenDateTime}>{teacher.lastSeen}</time>
                    </p>
                  ) : (
                    <div className="mt-1 flex items-center gap-x-1.5">
                      <div className="flex-none rounded-full bg-emerald-500/20 p-1">
                        <div className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                      </div>
                      <p className="text-xs leading-5 text-gray-500">Online</p>
                    </div>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
