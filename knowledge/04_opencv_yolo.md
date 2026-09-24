# Labs: OpenCV camera and YOLO

Files: `openCVTest.py`, `yoloTest.py`, `yoloDetection.py`, `yoloSegModelDetect.py`.

## OpenCV lab
- Open default webcam (`0`) or an IP camera URL.
- Resize toward 640×480.
- Loop: read frame → show window → press `q` to quit.
- Release capture and destroy windows.

This is the “we have pixels” baseline. Everything later is inference on those frames.

## YOLO detection
- Ultralytics `YOLO("yolo26n.pt")` (nano detect checkpoint used in class).
- Read frames from webcam or IP stream (class examples include `http://192.168.0.5:81/stream`).
- `model(frame, stream=True)` then `result.plot()` to draw boxes + class labels.
- Window title in one script: “Segmentation + Class Labels” even when running detect — naming drifted; teach the *task* not the window string.

## YOLO segmentation
- Same loop with `yolo26n-seg.pt`.
- Masks + labels instead of boxes only.
- Same quit key `q`.

## Teaching points
- Nano weights are for laptops and live FPS, not max accuracy.
- IP cameras fail for boring reasons: wrong URL, codec, timeout. One later lab even parsed MJPEG by hand.
- Detection answers “what / where.” Segmentation answers “which pixels.”
- Always design an escape key and cleanup. Demo machines get stuck windows.

## Typical questions
- Webcam index 0 vs 1.
- Why is FPS low?
- Detect vs segment vs pose (pose is the privacy lab).
