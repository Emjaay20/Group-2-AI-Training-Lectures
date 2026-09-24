# Lab: Screen privacy / shoulder-surfing monitor

File: `3.screenPrivacy.py`.

## Purpose
Classroom demo of visual privacy: if someone behind or beside the operator appears to be watching the screen, warn and obscure the display.

## Pipeline
1. YOLO pose model on the webcam.
2. People in frame with body keypoints (COCO: nose, eyes, …).
3. Heuristic roles:
   - **Primary Operator** = largest, most centered person.
   - Everyone else = **Bystander**.
4. Gaze proxy: if a bystander’s face keypoints look frontal to the camera, treat them as looking at the screen. This is a cheap geometric hint, not medical-grade eye tracking.
5. If that condition holds for several frames (debounce so the UI does not flicker):
   - blur the screen content,
   - draw a lock banner,
   - optional text-to-speech alert (`pyttsx3`, background thread),
   - optional OS lock — **disabled by default** so a demo cannot lock the lecturer out.
6. Unlock after enough clear frames. Quit with `q`.

## Key design choices to teach
- Confidence thresholds on keypoints.
- Frontalness ratio for “looking this way.”
- Frame counts for lock and unlock.
- Threading so TTS does not freeze OpenCV.

## Teaching points
- This is policy on top of perception: detect people → interpret role → apply a rule.
- False positives will happen (someone walking past). Debounce exists for that.
- Classroom use on a consented demo camera. It is not a licence for covert filming.

## What not to invent
Do not add hidden recording, face databases, or remote notification stacks. The lab is local, visible, and reversible.
