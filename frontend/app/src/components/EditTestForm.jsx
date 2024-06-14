import React from 'react';

export const EditTestForm = ({ updatedTestName, setUpdatedTestName, updatedStartDate, setUpdatedStartDate, updatedEndDate, setUpdatedEndDate, handleUpdateTest }) => {
  return (
    <div className="mt-6">
      <input
        type="text"
        value={updatedTestName}
        onChange={(e) => setUpdatedTestName(e.target.value)}
        className="block w-full border-gray-300 rounded-md"
        placeholder="Test Name"
      />
      <input
        type="datetime-local"
        value={updatedStartDate}
        onChange={(e) => setUpdatedStartDate(e.target.value)}
        className="block w-full border-gray-300 rounded-md mt-4"
        placeholder="Start Date"
      />
      <input
        type="datetime-local"
        value={updatedEndDate}
        onChange={(e) => setUpdatedEndDate(e.target.value)}
        className="block w-full border-gray-300 rounded-md mt-4"
        placeholder="End Date"
      />
      <button
        onClick={handleUpdateTest}
        className="block w-full bg-blue-500 text-white rounded-md mt-4 py-2"
      >
        Update Test
      </button>
    </div>
  );
};
