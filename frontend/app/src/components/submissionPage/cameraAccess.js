import React, { useRef, useState } from 'react';

const CameraAccess = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [hasPhoto, setHasPhoto] = useState(false);

  const getVideo = () => {
    navigator.mediaDevices.getUserMedia({ video: { width: 1920, height: 1080 } })
      .then(stream => {
        let video = videoRef.current;
        video.srcObject = stream;
        video.play();
      })
      .catch(err => {
        console.error("error:", err);
      });
  };

  const takePhoto = () => {
    const width = videoRef.current.clientWidth;
    const height = videoRef.current.clientHeight;
    let video = videoRef.current;
    let canvas = canvasRef.current;
    
    canvas.width = width;
    canvas.height = height;
    canvas.getContext('2d').drawImage(video, 0, 0, width, height);
    setHasPhoto(true);
  };

  return (
    <div className="camera">
      <video ref={videoRef}></video>
      <button onClick={getVideo}>Get Video</button>
      <button onClick={takePhoto}>Take Photo</button>
      <canvas ref={canvasRef} style={{ display: hasPhoto ? 'block' : 'none' }}></canvas>
    </div>
  );
};

export default CameraAccess;