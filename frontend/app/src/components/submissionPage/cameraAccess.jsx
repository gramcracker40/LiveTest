import React, { useEffect, useRef, useState } from 'react';


export const CameraAccess = () => {
  const openCvURL = 'https://docs.opencv.org/4.7.0/opencv.js';
  const videoRef = useRef(null);
  const imageRef = useRef(null);
  const [hasPhoto, setHasPhoto] = useState(false);
  const [loadedOpenCV, setLoadedOpenCV] = useState(false); 
  const scanner = new jscanify();
  const [capturedImage, setCapturedImage] = useState(null);
  const [testId, setTestId] = useState('');


  // load opencv, get access to video feed, begin highlighting documents. 
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

    // Cleanup
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

    if (video && video.readyState === 4) {
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
        
        setCapturedImage(canvas.toDataURL());
        setHasPhoto(true);
      };
      isolatedDoc.src = tempCanvas.toDataURL(); // Set the source to the captured image
    } else {
      console.error("Video is not ready");
    }
  };

  const handleSubmit = () => {
    console.log("Submit the photo:", capturedImage); 
  }
  

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
      {/* Test ID */}
      <div className="test-id-input mb-4 w-full max-w-sm">
        <label htmlFor="test-id" className="block text-sm text-center font-medium text-gray-700">
          Test ID
        </label>
        <input 
          type="text" 
          id="test-id" 
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          value={testId}
          onChange={(e) => setTestId(e.target.value)}
        />
      </div>

      {/* Video feed with highlighted canvas overlay */}
      <video ref={videoRef} 
      style={{ display: 'none' }}>
      </video>
      <canvas ref={imageRef} 
      className="w-full max-w-lg rounded-lg shadow-xl">
      </canvas>

      <div className="flex space-x-4 my-4">
        <button 
          onClick={takePhoto} 
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-700 transition duration-300"
        >
          Take Photo
        </button>
      </div>

      {hasPhoto && (
        <div className="photo-preview my-4">
          <img src={capturedImage} alt="Captured" className="max-w-lg rounded-lg shadow-xl"/>
          <button 
            onClick={handleSubmit} 
            className="px-4 py-2 mt-4 bg-blue-500 text-white rounded hover:bg-blue-700 transition duration-300"
          >
            Submit
          </button>
        </div>
      )}
    </div>
  );
};

export default CameraAccess;