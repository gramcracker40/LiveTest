import React, { useEffect, useRef, useState } from 'react';


export const CameraAccess = () => {
  const openCvURL = 'https://docs.opencv.org/4.7.0/opencv.js';
  const videoRef = useRef(null);
  const imageRef = useRef(null);
  const [hasPhoto, setHasPhoto] = useState(false);
  const [loadedOpenCV, setLoadedOpenCV] = useState(false); 
  const scanner = new jscanify();

  useEffect(() => {
    loadOpenCv(() => {
      navigator.mediaDevices.getUserMedia({ video: { width: 1920, height: 1080 } })
        .then(stream => {
          let video = videoRef.current;
          video.srcObject = stream;
          video.play();
          startProcessing();
        })
        .catch(err => {
          console.error("error:", err);
        });
    });

    // Cleanup on component unmount
    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
      stopProcessing();
    };
  }, []);

  const processInterval = useRef(null);

  const startProcessing = () => {
    processInterval.current = setInterval(() => {
      processVideo();
    }, 75); // Process every 75ms
  };

  const stopProcessing = () => {
    if (processInterval.current) {
      clearInterval(processInterval.current);
    }
  };

  const processVideo = () => {
    let video = videoRef.current;
    let canvas = imageRef.current;

    if (video.readyState === 4) {
      const width = video.videoWidth;
      const height = video.videoHeight;
      canvas.width = width;
      canvas.height = height;

      const frame = captureFrame(video, width, height);
      const highlightedFrame = scanner.highlightPaper(frame); // Assuming it returns an image or canvas

      // Draw the highlighted frame
      canvas.getContext('2d').drawImage(highlightedFrame, 0, 0, width, height);
    }
  };

  const captureFrame = (video, width, height) => {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = width;
    tempCanvas.height = height;
    tempCanvas.getContext('2d').drawImage(video, 0, 0, width, height);
    // You can return either the canvas or its image data based on your processing function's requirement
    return tempCanvas; // Or return tempCanvas.toDataURL() if your function requires an image URL
  };

  const takePhoto = () => {
    let video = videoRef.current;
    if (video && video.readyState === 4) { // Ensure video is ready
      const width = video.videoWidth;
      const height = video.videoHeight;
  
      // Create a temporary canvas to capture the video frame
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = width;
      tempCanvas.height = height;
      tempCanvas.getContext('2d').drawImage(video, 0, 0, width, height);
  
      // Convert the captured frame to an image for processing
      // Process the image, grab the isolated document. 
      const isolatedDoc = new Image();
      isolatedDoc.onload = () => {
        const resultCanvas = scanner.extractPaper(tempCanvas, 600, 1200);
        const canvas = imageRef.current;
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d').drawImage(resultCanvas, 
          0, 0, resultCanvas.width, resultCanvas.height);
  
        setHasPhoto(true);
      };
      isolatedDoc.src = tempCanvas.toDataURL(); // Set the source to the captured image
    } else {
      console.error("Video is not ready");
    }
  };
  

  const loadOpenCv = (onComplete) => {
    const isScriptPresent = !!document.getElementById('open-cv');
    if (isScriptPresent || loadedOpenCV) {
      setLoadedOpenCV(true);
      onComplete();
    } else {
      const script = document.createElement('script');
      script.id = 'open-cv';
      script.src = openCvURL;

      script.onload = function () {
        setTimeout(function () {
          onComplete();
        }, 1000);
        setLoadedOpenCV(true);
      };
      document.body.appendChild(script);
    }
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