// src/components/LiveVideoGrader.jsx
import React, { useEffect, useRef, useState, useCallback } from "react";

/**
 * LiveVideoGrader
 * - Opens webcam
 * - Shows flashing red overlay (11.5:8 aspect) to frame the sheet
 * - On "Start Grading", captures the overlay region periodically and POSTs to /submission
 * - On success: stops stream, returns { submissionId } to parent via onGraded
 *
 * Props:
 *   instanceURL: string (e.g., http://host:8000)
 *   test: { id, ... }
 *   authDetails: { type, id, accessToken, ... }
 *   selectedStudent: string | number | ""
 *   onGraded: (submissionId: number) => void
 *   onError: (msg: string) => void
 *   onNoSupport?: () => void   // optional: notify parent when getUserMedia isn't available
 */
export default function LiveVideoGrader({
  instanceURL,
  test,
  authDetails,
  selectedStudent,
  onGraded,
  onError,
  onNoSupport
}) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const rafRef = useRef(null);
  const intervalRef = useRef(null);
  const streamRef = useRef(null);

  const [isStreaming, setIsStreaming] = useState(false);
  const [isGrading, setIsGrading] = useState(false);
  const [flash, setFlash] = useState(false);
  const [overlayRect, setOverlayRect] = useState({ x: 0, y: 0, w: 0, h: 0 });

  // 11.5 : 8 aspect (width : height)
  const TARGET_ASPECT = 11.5 / 8.0;

  const cameraSupported = !!(navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === "function");

  const stopStream = useCallback(() => {
    setIsGrading(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (rafRef.current) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop());
      streamRef.current = null;
    }
    setIsStreaming(false);
  }, []);

  const startStream = useCallback(async () => {
    if (!cameraSupported) {
      onError?.("Live video is not available in this browser. Try Safari on iPhone, over HTTPS, or use the Camera option.");
      onNoSupport?.();
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: "environment" }, // hint; iOS may ignore
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: false
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        await videoRef.current.play(); // works with muted + playsInline
        setIsStreaming(true);
      }
    } catch (err) {
      onError?.(`Could not access camera: ${err.message}`);
      onNoSupport?.();
    }
  }, [cameraSupported, onError, onNoSupport]);

  // compute overlay rectangle whenever the video resizes/plays
  const computeOverlay = useCallback(() => {
    const v = videoRef.current;
    if (!v) return;

    const vw = v.clientWidth || v.videoWidth;
    const vh = v.clientHeight || v.videoHeight;
    if (!vw || !vh) return;

    const boxAspect = TARGET_ASPECT;
    let w = vw;
    let h = Math.round(w / boxAspect);
    if (h > vh) {
      h = vh;
      w = Math.round(h * boxAspect);
    }

    const x = Math.round((vw - w) / 2);
    const y = Math.round((vh - h) / 2);
    setOverlayRect({ x, y, w, h });
  }, []);

  // draw overlay (flashing red) on a canvas layer
  const drawOverlay = useCallback(() => {
    const v = videoRef.current;
    const c = canvasRef.current;
    if (!v || !c) return;
    const ctx = c.getContext("2d");
    const vw = v.clientWidth || v.videoWidth;
    const vh = v.clientHeight || v.videoHeight;
    c.width = vw;
    c.height = vh;

    // clear
    ctx.clearRect(0, 0, vw, vh);

    // darken outside overlay
    ctx.fillStyle = "rgba(0,0,0,0.35)";
    ctx.fillRect(0, 0, vw, vh);
    const { x, y, w, h } = overlayRect;
    ctx.clearRect(x, y, w, h);

    // flashing red border
    const pulse = flash ? 1 : 0;
    const thickness = 4 + (pulse ? 2 : 0);
    ctx.lineWidth = thickness;
    ctx.strokeStyle = "rgba(255,0,0,0.9)";
    ctx.strokeRect(x + thickness / 2, y + thickness / 2, w - thickness, h - thickness);
  }, [overlayRect, flash]);

  // animation loop
  const onFrame = useCallback(() => {
    drawOverlay();
    rafRef.current = requestAnimationFrame(onFrame);
  }, [drawOverlay]);

  // Start grading: begin interval captures focused on overlay rect
  const startGrading = useCallback(() => {
    if (!isStreaming || isGrading) return;
    setIsGrading(true);

    const flashTimer = setInterval(() => setFlash(f => !f), 400);

    // capture interval (every ~1.2s)
    intervalRef.current = setInterval(async () => {
      try {
        const v = videoRef.current;
        if (!v) return;

        const visW = v.clientWidth || v.videoWidth;
        const visH = v.clientHeight || v.videoHeight;
        if (!visW || !visH) return;

        // Draw frame to a buffer canvas
        const buffer = document.createElement("canvas");
        buffer.width = visW;
        buffer.height = visH;
        const bctx = buffer.getContext("2d");
        bctx.drawImage(v, 0, 0, visW, visH);

        // Crop overlay region
        const { x, y, w, h } = overlayRect;
        const crop = document.createElement("canvas");
        crop.width = w;
        crop.height = h;
        const cctx = crop.getContext("2d");
        cctx.drawImage(buffer, x, y, w, h, 0, 0, w, h);

        const blob = await new Promise(resolve => crop.toBlob(resolve, "image/jpeg", 0.8));
        if (!blob) return;

        const fd = new FormData();
        fd.append("submission_image", new File([blob], "frame.jpg", { type: "image/jpeg" }));
        if (authDetails?.type === "teacher" && selectedStudent) {
          fd.append("student_id", String(selectedStudent));
        } else if (authDetails?.type === "student" && authDetails?.id) {
          fd.append("student_id", String(authDetails.id));
        }
        fd.append("test_id", test.id);

        const url = `${instanceURL}/submission/`;
        const resp = await fetch(url, { method: "POST", body: fd });
        const data = await resp.json().catch(() => ({}));

        if (resp.ok && data?.submission_id) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
          clearInterval(flashTimer);
          setIsGrading(false);
          onGraded?.(data.submission_id);
          stopStream();
        } else {
          console.warn("Grading attempt failed:", resp.status, data);
        }
      } catch (err) {
        console.warn("Capture/submit error:", err);
      }
    }, 1200);

    rafRef.current = requestAnimationFrame(onFrame);

    return () => clearInterval(flashTimer);
  }, [
    isStreaming,
    isGrading,
    overlayRect,
    onFrame,
    instanceURL,
    test,
    authDetails,
    selectedStudent,
    onGraded,
    stopStream
  ]);

  // Mount/unmount camera
  useEffect(() => {
    startStream();
    return () => stopStream();
  }, [startStream, stopStream]);

  // Recompute overlay whenever video metadata changes / size changes
  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    const onLoaded = () => {
      computeOverlay();
      drawOverlay();
    };
    v.addEventListener("loadedmetadata", onLoaded);
    window.addEventListener("resize", computeOverlay);
    return () => {
      v.removeEventListener("loadedmetadata", onLoaded);
      window.removeEventListener("resize", computeOverlay);
    };
  }, [computeOverlay, drawOverlay]);

  // Keep drawing overlay as long as we’re streaming
  useEffect(() => {
    if (!isStreaming) return;
    rafRef.current = requestAnimationFrame(onFrame);
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [isStreaming, onFrame]);

  return (
    <div className="w-full">
      <div className="relative w-full max-w-4xl mx-auto aspect-video bg-black rounded-lg overflow-hidden shadow">
        {/* Video */}
        <video
          ref={videoRef}
          playsInline
          muted
          className="w-full h-full object-contain bg-black"
        />
        {/* Overlay Canvas */}
        <canvas
          ref={canvasRef}
          className="absolute inset-0 pointer-events-none"
        />
        {/* Heads-up tip */}
        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 bg-white/80 text-gray-800 text-sm px-3 py-1 rounded">
          Fit the sheet inside the red 11.5×8 box, then press Start Grading
        </div>
      </div>

      <div className="flex gap-3 justify-center mt-4">
        {!isGrading && (
          <button
            onClick={startGrading}
            disabled={!isStreaming}
            className="px-4 py-2 rounded bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-300"
          >
            Start Grading
          </button>
        )}
        {isStreaming && (
          <button
            onClick={stopStream}
            className="px-4 py-2 rounded bg-gray-600 text-white hover:bg-gray-700"
          >
            Stop Video
          </button>
        )}
      </div>
    </div>
  );
}
