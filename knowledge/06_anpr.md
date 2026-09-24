# Lab: License plate access control (ANPR)

File: `4.licencePlate.py`.

## Purpose
Demo a vehicle gate: see a vehicle, read a plate, compare to an allow-list, show GRANTED or DENIED.

## Pipeline
1. Tkinter prompt: camera `0` or an IP MJPEG URL. Cancel → default `0`.
2. Custom `MjpegStream` for cheap IP cams — parse multipart JPEG by hand because OpenCV/FFmpeg often times out or desyncs.
3. YOLO nano detect (`yolo26n.pt`) for vehicle classes: car, truck, bus, motorcycle.
4. Inside the vehicle box, OpenCV looks for a plate-like rectangle:
   - Canny edges → contours → quadrilaterals,
   - aspect ratio about 2.0–6.0,
   - width at least ~15% of the vehicle box.
5. EasyOCR on that crop, every N frames (`OCR_EVERY_N_FRAMES = 10`) to save CPU.
6. Clean text: alphanumeric, uppercase.
7. Compare to `AUTHORIZED_PLATES`. Class seed set: `ABC1234`, `NDC2026`.
8. Dashboard: live feed + boxes, plate thumbnail, read text, green GRANTED / red DENIED, pipeline status, FPS.
9. Keys: `a` temporarily authorises the current read (demo only), `q` quits.

## Teaching points
- This is a **pipeline**, not one model. Detect ≠ read ≠ decide.
- OCR is the fragile step (angle, blur, light, dirty plate). That is why the UI shows crop + raw text.
- Allow-list is the policy layer. Changing the set changes the system without retraining YOLO.
- Real facilities need logging, anti-spoofing, and human override. This lab is a teaching gate.

## Typical questions
- Why OCR only every 10 frames?
- How do I add a plate properly (not just the demo `a` key)?
- Why MJPEG parser instead of `cv2.VideoCapture(url)`?
