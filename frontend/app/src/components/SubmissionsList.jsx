import React, { useEffect, useState } from 'react';
import { StarIcon } from '@heroicons/react/20/solid';
import pako from 'pako';
import { instanceURL } from '../api/helpers';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

const getStarIcons = (grade) => {
  const stars = [];
  for (let i = 0; i < 5; i++) {
    if (grade >= (i + 1) * 20) {
      stars.push(<StarIcon key={i} className="text-yellow-400 h-5 w-5 flex-shrink-0" aria-hidden="true" />);
    } else if (grade >= (i + 0.75) * 20) {
      stars.push(<StarIcon key={i} className="text-yellow-400 h-5 w-5 flex-shrink-0" aria-hidden="true" style={{ clipPath: 'polygon(0 0, 100% 0, 100% 75%, 0 75%)' }} />);
    } else if (grade >= (i + 0.5) * 20) {
      stars.push(<StarIcon key={i} className="text-yellow-400 h-5 w-5 flex-shrink-0" aria-hidden="true" style={{ clipPath: 'polygon(0 0, 100% 0, 100% 50%, 0 50%)' }} />);
    } else if (grade >= (i + 0.25) * 20) {
      stars.push(<StarIcon key={i} className="text-yellow-400 h-5 w-5 flex-shrink-0" aria-hidden="true" style={{ clipPath: 'polygon(0 0, 100% 0, 100% 25%, 0 25%)' }} />);
    } else {
      stars.push(<StarIcon key={i} className="text-gray-200 h-5 w-5 flex-shrink-0" aria-hidden="true" />);
    }
  }
  return stars;
};

export const SubmissionsList = ({ submissions, onDeleteSubmission }) => {
  const [submissionImages, setSubmissionImages] = useState([]);

  useEffect(() => {
    const fetchSubmissionImages = async () => {
      try {
        const images = await Promise.all(
          submissions.map(async (submission) => {
            const gradedImageURL = `${instanceURL}/submission/image/graded/${submission.id}`;
            const response = await fetch(gradedImageURL);
            if (!response.ok) {
              throw new Error('Failed to fetch image');
            }
            const compressedArrayBuffer = await response.arrayBuffer();
            const decompressedData = pako.inflate(new Uint8Array(compressedArrayBuffer));
            const blob = new Blob([decompressedData], { type: 'image/jpeg' });
            return { ...submission, gradedImage: URL.createObjectURL(blob) };
          })
        );
        setSubmissionImages(images);
      } catch (error) {
        console.error('Error fetching submission images', error);
      }
    };
    fetchSubmissionImages();
  }, [submissions]);

  return (
    <div className="bg-cyan-50">
      <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
        <div className="mt-6 space-y-10 divide-y divide-gray-200 border-b border-t border-gray-200 pb-10">
          {submissionImages.map((submission) => (
            <div key={submission.id} className="pt-10 lg:grid lg:grid-cols-12 lg:gap-x-8 relative bg-white p-4 rounded-lg shadow-lg">
              <button
                className="absolute top-4 right-4 text-red-600 hover:text-red-800"
                onClick={() => {
                  console.log("Delete button clicked for submission id:", submission.id);
                  if (onDeleteSubmission) {
                    onDeleteSubmission(submission.id);
                  } else {
                    console.error("onDeleteSubmission function is not provided");
                  }
                }}
              >
                Delete
              </button>
              <div className="lg:col-span-3">
                <p className="font-medium text-gray-900">{submission.student_name}</p>
                <p className="text-sm text-gray-500">{new Date(submission.submission_time).toLocaleString()}</p>
              </div>
              <div className="lg:col-span-2 flex items-center">
                <div className="flex items-center">{getStarIcons(submission.grade)}</div>
                <p className="ml-3 text-sm text-gray-700">{submission.grade} / 100</p>
              </div>
              <div className="lg:col-span-7">
                <img src={submission.gradedImage} alt={`Graded submission ${submission.id}`} className="rounded-lg shadow-lg" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
