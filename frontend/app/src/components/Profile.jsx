import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/auth';
import { EasyRequest, instanceURL, defHeaders } from '../api/helpers';

const Profile = () => {
  const { authDetails } = useContext(AuthContext);
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    password: ''
  });
  const [passwordStrength, setPasswordStrength] = useState('');
  const [updateSuccess, setUpdateSuccess] = useState(false);

  useEffect(() => {
    if (!authDetails.isLoggedIn) {
      return;
    }

    const fetchProfile = async () => {
      try {
        const url = `${instanceURL}/users/${authDetails.type}s/${authDetails.id}`;
        const req = await EasyRequest(url, defHeaders, 'GET');
        if (req.status === 200) {
          setProfile({
            name: req.data.name,
            email: req.data.email,
            password: ''
          });
        }
      } catch (error) {
        console.error('Error fetching profile', error);
      }
    };

    fetchProfile();
  }, [authDetails]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile({ ...profile, [name]: value });

    if (name === 'password') {
      checkPasswordStrength(value);
    }
  };

  const checkPasswordStrength = (password) => {
    let strength = '';
    if (password.length > 8) strength = 'Moderate';
    if (/[A-Z]/.test(password) && password.length > 8) strength = 'Moderate';
    if (/[0-9]/.test(password) && /[!@#$%^&*]/.test(password) && password.length > 8) strength = 'Strong';
    if (password.length <= 8) strength = 'Weak';

    setPasswordStrength(strength);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const updateUrl = `${instanceURL}/users/${authDetails.type}s/${authDetails.id}`;
    try {
      const req = await EasyRequest(updateUrl, defHeaders, 'PATCH', profile);
      if (req.status === 200) {
        setUpdateSuccess(true);
        setTimeout(() => setUpdateSuccess(false), 3000); // Hide the success message after 3 seconds
      } else {
        console.error('Error updating profile', req);
      }
    } catch (error) {
      console.error('Error updating profile', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-6">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">
            Name
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="name"
              id="name"
              value={profile.name}
              onChange={handleChange}
              placeholder={profile.name}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email
          </label>
          <div className="mt-1">
            <input
              type="email"
              name="email"
              id="email"
              value={profile.email}
              onChange={handleChange}
              placeholder={profile.email}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
        </div>
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
            Password
          </label>
          <div className="mt-1">
            <input
              type="password"
              name="password"
              id="password"
              value={profile.password}
              onChange={handleChange}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
          {passwordStrength && (
            <p className={`mt-1 text-sm ${passwordStrength === 'Strong' ? 'text-green-600' : passwordStrength === 'Moderate' ? 'text-yellow-600' : 'text-red-600'}`}>
              Password Strength: {passwordStrength}
            </p>
          )}
        </div>
      </div>
      <div className="flex justify-center mt-6">
        <button
          type="submit"
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Save
        </button>
        
      </div>
      {updateSuccess && (
        <div className="mt-4 text-green-600">
          Profile updated successfully!
        </div>
      )}
    </form>
  );
};

export default Profile;
