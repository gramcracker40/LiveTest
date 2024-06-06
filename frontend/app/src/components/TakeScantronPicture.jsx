import React, { useRef, useState, useEffect } from 'react';
import Webcam from 'react-webcam';

export const TakeScantronPicture = ({ onSubmit }) => {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  const [image, setImage] = useState(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [detectionTimeout, setDetectionTimeout] = useState(null);

  useEffect(() => {
    if (webcamRef.current && canvasRef.current) {
      drawAlignmentBox();
    }
  }, []);

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);
  };

  const drawAlignmentBox = () => {
    if (webcamRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      const videoWidth = webcamRef.current.video.videoWidth;
      const videoHeight = webcamRef.current.video.videoHeight;

      canvasRef.current.width = videoWidth;
      canvasRef.current.height = videoHeight;

      const aspectRatio = 4.25 / 11;
      let boxHeight = videoHeight * 0.9;
      let boxWidth = boxHeight * aspectRatio;

      if (boxWidth > videoWidth) {
        boxWidth = videoWidth * 0.9;
        boxHeight = boxWidth / aspectRatio;
      }

      const x = (videoWidth - boxWidth) / 2;
      const y = (videoHeight - boxHeight) / 2;

      context.clearRect(0, 0, videoWidth, videoHeight);
      context.beginPath();
      context.rect(x, y, boxWidth, boxHeight);
      context.strokeStyle = 'cyan';
      context.lineWidth = 4;
      context.stroke();
    }
  };

  const detectDocument = () => {
    setIsDetecting(true);
    if (detectionTimeout) clearTimeout(detectionTimeout);
    setDetectionTimeout(setTimeout(() => {
      capture();
      setIsDetecting(false);
    }, 3000));
  };

  const handlePhotoSubmit = () => {
    if (onSubmit && typeof onSubmit === 'function') {
      onSubmit(image.split('base64,')[1]); // Pass the base64 encoded image to the callback
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-cyan-100 p-4">
      <h1 className="text-3xl font-bold mb-4">Align your Scantron within the box</h1>
      {!image ? (
        <div className="relative">
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            onUserMedia={() => drawAlignmentBox()}
            videoConstraints={{
              width: 640,
              height: 480,
              facingMode: "user"
            }}
            className="w-full"
            onDetected={detectDocument}
          />
          <canvas ref={canvasRef} className="absolute top-0 left-0" />
          <button onClick={capture} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition duration-300">
            Take Photo
          </button>
        </div>
      ) : (
        <>
          <img src={image} alt="Captured" className="max-w-lg rounded-lg shadow-xl" />
          <div className="flex space-x-4 my-4">
            <button onClick={() => setImage(null)} className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-700 transition duration-300">
              Retake Photo
            </button>
            <button onClick={handlePhotoSubmit} className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-700 transition duration-300">
              Submit
            </button>
          </div>
        </>
      )}
    </div>
  );
};
