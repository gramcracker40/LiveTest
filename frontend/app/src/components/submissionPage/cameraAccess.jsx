import React, { useEffect, useRef, useState } from 'react';


export const CameraAccess = () => {
  const videoRef = useRef(null);
  const imageRef = useRef(null);
  const [hasPhoto, setHasPhoto] = useState(false);
  const scanner = new jscanify();

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: { width: 1920, height: 1080 } })
      .then(stream => {
        let video = videoRef.current;
        video.srcObject = stream;
        video.play();
      })
      .catch(err => {
        console.error("error:", err);
      });
  });

  const takePhoto = () => {
    const width = videoRef.current.clientWidth;
    const height = videoRef.current.clientHeight;
    let video = videoRef.current;
    let canvas = imageRef.current;
    
    const isolatedDoc = document.createElement('img');
    isolatedDoc.src = imageRef.src; 

    isolatedDoc.onload = function () {
      const resultCanvas = scanner.extractPaper(isolatedDoc, 386, 500);
      const highlightedCanvas = scanner.highlightPaper(newImg);


    };


    canvas.width = width;
    canvas.height = height;
    canvas.getContext('2d').drawImage(video, 0, 0, width, height);
    setHasPhoto(true);
  };

  return (
    <div className="camera flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <video 
        ref={videoRef} 
        className="w-full max-w-lg rounded-lg shadow-xl"
      ></video>

      <div className="flex space-x-4 my-4">
        
        <button 
          onClick={takePhoto} 
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-700 transition duration-300"
        >
          Take Photo
        </button>
      </div>

      <canvas 
        ref={imageRef} 
        style={{ display: hasPhoto ? 'block' : 'none' }} 
        className="w-full max-w-lg rounded-lg shadow-xl"
      ></canvas>
    </div>
  );
};

export default CameraAccess;